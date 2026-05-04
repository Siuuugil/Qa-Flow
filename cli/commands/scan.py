import click
from rich.console import Console
from dotenv import load_dotenv
from pathlib import Path
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
@click.option("--focus",
              type=click.Choice(["structure",
                                 "convention",
                                 "security",
                                 "bug",
                                 "qa",
                                 "dev",
                                 "performance",
                                 "test",
                                 "general"]),
              default=None,
              help="리뷰 관점 선택")
@click.option("--file",
              default=None,
              help="특정 파일 직접 분석 (git diff 없이)")
def scan(mode, report, provider, focus, file):
    """코드 분석 실행"""

    load_dotenv(dotenv_path=Path.cwd() / ".env", encoding="utf-8")

    ai_provider = provider or os.getenv("AI_PROVIDER", "gemini")

    if file:
        console.print("\n[bold cyan]파일 분석 모드[/bold cyan]")
        console.print(f"파일: [yellow]{file}[/yellow]")
        console.print(f"AI Provider: [yellow]{ai_provider}[/yellow]")
        console.print(f"Focus: [yellow]{focus or 'default'}[/yellow]\n")

        if mode == "full":
            convention_result = run_convention_check_file(file)
            ai_result = run_ai_review_file(ai_provider, focus, file)
            if report:
                run_report(ai_result, convention_result)
        else:
            run_ai_review_file(ai_provider, focus, file)

    else:
        console.print("\n[bold cyan]QA-Flow 분석 시작[/bold cyan]")
        console.print(f"모드: [yellow]{mode}[/yellow]")
        console.print(f"AI Provider: [yellow]{ai_provider}[/yellow]")
        console.print(f"Focus: [yellow]{focus or 'default'}[/yellow]")
        console.print(f"리포트 생성: [yellow]{report}[/yellow]\n")

        if mode == "ai-only":
            run_ai_review(ai_provider, focus)
        elif mode == "full":
            convention_result = run_convention_check()
            ai_result = run_ai_review(ai_provider, focus)
            if report:
                run_report(ai_result, convention_result)


def run_ai_review(provider: str, focus: str = None):
    """AI 코드 리뷰 실행"""
    console.print("[bold]AI 코드 리뷰 실행 중...[/bold]")

    from cli.core.ai_review import AIReview

    with console.status("[bold green]AI가 코드를 분석하고 있습니다..."):
        reviewer = AIReview(provider=provider, focus=focus)
        result = reviewer.review()

    console.print(result)
    return result


def run_ai_review_file(provider: str, focus: str = None, file: str = None):
    """특정 파일 AI 분석"""

    allowed_extensions = (
        ".py", ".java", ".js", ".ts", ".jsx", ".tsx",
        ".go", ".rs", ".kt", ".swift", ".cpp", ".c", ".cs"
    )
    if not file.endswith(allowed_extensions):
        console.print(f"[red]지원하지 않는 파일 형식입니다: {file}[/red]")
        return ""

    try:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        console.print(f"[red]파일을 찾을 수 없습니다: {file}[/red]")
        return ""
    except Exception as e:
        console.print(f"[red]파일 읽기 오류: {str(e)}[/red]")
        return ""

    from cli.core.ai_review import AIReview

    with console.status(f"[bold green]AI가 {file} 을 분석하고 있습니다..."):
        reviewer = AIReview(provider=provider, focus=focus)
        result = reviewer.provider.review(code)

    console.print(result)
    return result


def run_convention_check():
    """컨벤션 체크 실행"""
    console.print("[bold]컨벤션 체크 실행 중...[/bold]")

    from cli.core.convention import ConventionChecker

    checker = ConventionChecker()
    result = checker.check()

    console.print(result)
    return result


def run_convention_check_file(file: str):
    """특정 파일 컨벤션 체크"""
    console.print("[bold]컨벤션 체크 실행 중...[/bold]")

    import subprocess

    result = ""

    if file.endswith((".js", ".ts", ".jsx", ".tsx")):
        try:
            r = subprocess.run(
                ["npx", "eslint", file],
                capture_output=True, text=True
            )
            if r.returncode == 0:
                result = "[ESLint] 컨벤션 위반 없음"
            else:
                result = f"[ESLint] 위반 사항:\n{r.stdout}"
        except FileNotFoundError:
            result = "[ESLint] 설치되지 않아 스킵합니다."

    elif file.endswith(".py"):
        try:
            r = subprocess.run(
                ["flake8", "--max-line-length=100", file],
                capture_output=True, text=True
            )
            if r.returncode == 0:
                result = "[Flake8] 컨벤션 위반 없음"
            else:
                result = f"[Flake8] 위반 사항:\n{r.stdout}"
        except FileNotFoundError:
            result = "[Flake8] 설치되지 않아 스킵합니다."

    elif file.endswith(".java"):
        result = "[Java] 컨벤션 체크는 AI 리뷰로 대체합니다."

    console.print(result)
    return result


def run_report(ai_result: str = "", convention_result: str = ""):
    """리포트 생성"""
    console.print("[bold]리포트 생성 중...[/bold]")

    from cli.core.reporter import Reporter

    reporter = Reporter()
    reporter.generate(ai_result=ai_result, convention_result=convention_result)

    console.print("[green]리포트 생성 완료![/green]")
