import click
import json
import os
from rich.console import Console
from pathlib import Path
from dotenv import load_dotenv

console = Console()


@click.command()
@click.option("--provider", "-p",
              type=click.Choice(["claude", "gemini"]),
              default=None,
              help="AI Provider 선택")
@click.option("--jira", "-j",
              is_flag=True,
              default=False,
              help="TC 생성 후 Jira 등록")
def tc(provider, jira):
    """마지막 리포트 기반 TC 자동 생성"""

    load_dotenv(dotenv_path=Path.cwd() / ".env", encoding="utf-8")

    ai_provider = provider or os.getenv("AI_PROVIDER", "gemini")

    # 가장 최근 리포트 찾기
    report_dir = Path("qa-reports")
    if not report_dir.exists():
        console.print("[red]리포트가 없습니다. 먼저 qa-flow scan --report 를 실행하세요.[/red]")
        return

    reports = sorted(report_dir.glob("*.json"), key=os.path.getmtime, reverse=True)
    if not reports:
        console.print("[red]리포트가 없습니다. 먼저 qa-flow scan --report 를 실행하세요.[/red]")
        return

    latest = reports[0]

    # 확인 질문
    if not click.confirm(f"\n마지막 리포트: [bold]{latest.name}[/bold] 기준으로 TC를 생성하시겠습니까?", default=False):
        console.print("[dim]취소했습니다.[/dim]")
        return

    # 리포트 읽기
    with open(latest, "r", encoding="utf-8") as f:
        report = json.load(f)

    ai_result = report.get("ai_review", "")
    convention_result = report.get("convention_check", "")
    focus = report.get("focus", "general")

    if not ai_result:
        console.print("[red]리포트에 AI 분석 결과가 없습니다.[/red]")
        return

    # 파일명에서 base_name 추출
    # report_scan_qa_20260505_151313.json → scan_qa
    stem = latest.stem  # report_scan_qa_20260505_151313
    parts = stem.split("_")
    # report 제거하고 타임스탬프 제거
    base_name = "_".join(parts[1:-2]) if len(parts) > 3 else focus
    timestamp = "_".join(parts[-2:]) if len(parts) > 2 else None

    from cli.commands.scan import run_tc_generation
    tc_path = run_tc_generation(ai_provider, ai_result, convention_result, upload_jira=jira, timestamp=timestamp, base_name=base_name)

    if tc_path:
        console.print(f"\n[dim]리포트: {latest.name} → TC: {Path(tc_path).name}[/dim]")