import click
import os
from rich.console import Console
from dotenv import load_dotenv
from pathlib import Path

console = Console()


@click.command()
@click.option("--provider",
              type=click.Choice(["claude", "gemini"]),
              default=None,
              help="AI Provider 선택")
def chat(provider):
    """AI와 자유롭게 대화"""

    load_dotenv(dotenv_path=Path.cwd() / ".env", encoding="utf-8")

    ai_provider = provider or os.getenv("AI_PROVIDER", "gemini")

    console.print("\n[bold cyan]QA-Flow Chat[/bold cyan]")
    console.print(f"Provider: [yellow]{ai_provider}[/yellow]")
    console.print("[dim]종료하려면 exit 또는 quit 입력[/dim]\n")

    from cli.core.providers.claude import ClaudeProvider
    from cli.core.providers.gemini import GeminiProvider

    system_prompt = """당신은 QA 엔지니어이자 시니어 개발자입니다.
코드 리뷰, 버그 분석, 테스트 전략, 설계 관련 질문 등 개발과 QA에 관한 모든 질문에 답변하세요.
코드를 붙여넣으면 분석해주고, 질문에는 명확하게 답변하세요.
한국어로 친절하게 답변하세요."""

    if ai_provider == "claude":
        ai = ClaudeProvider(system_prompt=system_prompt)
    else:
        ai = GeminiProvider(system_prompt=system_prompt)

    history = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]종료합니다.[/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            console.print("[dim]종료합니다.[/dim]")
            break

        history.append({"role": "user", "content": user_input})

        console.print("\n[bold cyan]AI:[/bold cyan]")
        result = ai.chat(history)
        console.print(result)
        console.print()

        history.append({"role": "assistant", "content": result})
