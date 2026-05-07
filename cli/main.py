import os
os.environ["PYTHONIOENCODING"] = "utf-8"  # noqa: E402
os.environ["PYTHONUTF8"] = "1"  # noqa: E402

from cli.commands.chat import chat  # noqa: E402
from cli.commands.init import init  # noqa: E402
from cli.commands.scan import scan  # noqa: E402
from cli.commands.tc import tc # noqa: E402
from cli.commands.jira_cmd import jira # noqa: E402
from rich.console import Console  # noqa: E402
import click  # noqa: E402

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
@click.version_option(version="0.1.7", prog_name="qa-flow")
def main():
    """QA-Flow: AI 기반 코드 품질 자동화 툴"""
    pass


main.add_command(init)
main.add_command(scan, name="scan")
main.add_command(scan, name="s")      
main.add_command(chat, name="chat")
main.add_command(chat, name="c")    
main.add_command(tc, name="tc")
main.add_command(tc, name="t")
main.add_command(jira, name="jira")
main.add_command(jira, name="j")  

if __name__ == "__main__":
    main()
