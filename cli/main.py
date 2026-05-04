from cli.commands.chat import chat
from cli.commands.init import init
from cli.commands.scan import scan
from rich.console import Console
import click

console = Console()


def print_banner():
    console.print("""
[bold cyan]
  ██████╗  █████╗          ███████╗██╗      ██████╗ ██╗    ██╗
 ██╔═══██╗██╔══██╗         ██╔════╝██║     ██╔═══██╗██║    ██║
 ██║   ██║███████║ █████╗  █████╗  ██║     ██║   ██║██║ █╗ ██║
 ██║▄▄ ██║██╔══██║ ╚════╝  ██╔══╝  ██║     ██║   ██║██║███╗██║
 ╚██████╔╝██║  ██║         ██║     ███████╗╚██████╔╝╚███╔███╔╝
  ╚══▀▀═╝ ╚═╝  ╚═╝         ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝
[/bold cyan]""")
    console.print("[dim]AI-powered QA automation CLI[/dim]\n")


@click.group()
@click.version_option(version="0.1.5", prog_name="qa-flow")
def main():
    """QA-Flow: AI 기반 코드 품질 자동화 툴"""
    pass


main.add_command(init)
main.add_command(scan)
main.add_command(chat)

if __name__ == "__main__":
    main()
