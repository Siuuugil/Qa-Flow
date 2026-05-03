import click
from rich.console import Console
from dotenv import load_dotenv
import os

console = Console()

@click.command()
@click.option("--mode", 
              type=click.Choice(["ai-only", "full"]), 
              default="ai-only",
              help="실행 모드 선택")
@click.option("--report", 
              is_flag=True, 
              default=False,
              help="리포트 파일 생성")
@click.option("--provider",
              type=click.Choice(["claude", "gemini"]),
              default=None,
              help="AI Provider 선택 (기본값: .env 설정 따름)")
def scan(mode, report, provider):
    """코드 분석 실행"""
    
    load_dotenv()

    # provider 결정 (.env 또는 옵션)
    ai_provider = provider or os.getenv("AI_PROVIDER", "claude")
    
    console.print(f"\n[bold cyan]QA-Flow 분석 시작[/bold cyan]")
    console.print(f"모드: [yellow]{mode}[/yellow]")
    console.print(f"AI Provider: [yellow]{ai_provider}[/yellow]")
    console.print(f"리포트 생성: [yellow]{report}[/yellow]\n")

    if mode == "ai-only":
        run_ai_review(ai_provider)
    
    elif mode == "full":
        run_convention_check()
        run_ai_review(ai_provider)
        if report:
            run_report()

def run_ai_review(provider: str):
    """AI 코드 리뷰 실행"""
    console.print("[bold]AI 코드 리뷰 실행 중...[/bold]")
    
    from cli.core.ai_review import AIReview
    reviewer = AIReview(provider=provider)
    result = reviewer.review()
    
    console.print(result)

def run_convention_check():
    """컨벤션 체크 실행"""
    console.print("[bold]컨벤션 체크 실행 중...[/bold]")
    
    from cli.core.convention import ConventionChecker
    checker = ConventionChecker()
    result = checker.check()
    
    console.print(result)

def run_report():
    """리포트 생성"""
    console.print("[bold]리포트 생성 중...[/bold]")
    
    from cli.core.reporter import Reporter
    reporter = Reporter()
    reporter.generate()
    
    console.print("[green]리포트 생성 완료![/green]")