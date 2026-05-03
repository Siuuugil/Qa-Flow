import click
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

@click.command()
def init():
    """QA-Flow 초기 설정"""

    console.print("\n[bold cyan]QA-Flow 초기 설정을 시작합니다![/bold cyan]\n")

    console.print("[bold]AI Provider를 선택하세요:[/bold]")
    console.print("  [cyan]1[/cyan] Claude (Anthropic)")
    console.print("  [cyan]2[/cyan] Gemini (Google)")

    provider_choice = Prompt.ask("\n선택", choices=["1", "2"], default="1")
    provider = "claude" if provider_choice == "1" else "gemini"

    console.print(f"\n[green]{provider.upper()}[/green] 선택됨\n")

    if provider == "claude":
        api_key = click.prompt("Anthropic API Key", hide_input=True)
        api_key_name = "ANTHROPIC_API_KEY"
    else:
        api_key = click.prompt("Gemini API Key", hide_input=True)
        api_key_name = "GEMINI_API_KEY"

    github_token = click.prompt("GitHub Token", hide_input=True)
    github_repo = Prompt.ask("GitHub Repo (예: owner/repo-name)")

    use_supabase = Confirm.ask("\nSupabase 연동할까요?", default=True)
    supabase_url = ""
    supabase_key = ""

    if use_supabase:
        supabase_url = Prompt.ask("Supabase URL")
        supabase_key = click.prompt("Supabase Key", hide_input=True)

    env_content = f"""AI_PROVIDER={provider}
{api_key_name}={api_key}
GITHUB_TOKEN={github_token}
GITHUB_REPO={github_repo}
"""

    if use_supabase:
        env_content += f"SUPABASE_URL={supabase_url}\nSUPABASE_KEY={supabase_key}\n"

    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)

    console.print("\n[bold green]설정 완료! .env 파일이 생성됐어요.[/bold green]")
    console.print("[dim]이제 qa-flow scan 명령어를 사용할 수 있어요![/dim]\n")