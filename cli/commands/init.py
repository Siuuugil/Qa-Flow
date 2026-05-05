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

    # qa.yml 생성 여부 확인
    create_yml = Confirm.ask("\nGitHub Actions qa.yml 파일도 생성할까요?", default=True)

    if create_yml:
        import os
        os.makedirs(".github/workflows", exist_ok=True)
        
        qa_yml_content = """name: QA-Flow

on:
  pull_request:
    branches: ["**"]

jobs:
  qa-scan:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install qa-flow

      - name: Run QA-Flow scan
        id: qa_scan
        env:
          AI_PROVIDER: ${{ secrets.AI_PROVIDER }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
        run: |
          qa-flow scan --mode full --report --provider gemini 2>&1 | tee qa_result.txt
          echo "result<<EOF" >> $GITHUB_OUTPUT
          cat qa_result.txt >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: PR Comment
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const fs = require('fs');
            const raw = fs.readFileSync('qa_result.txt', 'utf8');
            const conventionMatch = raw.match(/컨벤션 체크 실행 중\\.\\.\\.([\s\S]*?)AI 코드 리뷰 실행 중/);
            const aiMatch = raw.match(/AI 코드 리뷰 실행 중\\.\\.\\.([\s\S]*?)리포트 생성 중/);
            const timeMatches = [...raw.matchAll(/report_(\\d{8}_\\d{6})\\.json/g)];
            const timestamp = timeMatches.length > 0 ? timeMatches[timeMatches.length - 1][1] : '-';
            const convention = conventionMatch ? conventionMatch[1].trim() : '결과 없음';
            const aiReview = aiMatch ? aiMatch[1].trim() : '결과 없음';
            const MARKER = '<!-- qa-flow-comment -->';
            const codeBlock = '`' + '`' + '`';
            const body = [MARKER,'## QA-Flow 분석 결과','',`> 분석 시각: \\`${timestamp}\\``,'',' ---','','### 컨벤션 체크',codeBlock + 'text',convention,codeBlock,'','---','','### AI 코드 리뷰','',aiReview,'','---','','<sub>QA-Flow by Siuuugil</sub>'].join('\\n');
            const comments = await github.rest.issues.listComments({issue_number: context.issue.number,owner: context.repo.owner,repo: context.repo.repo});
            const existing = comments.data.find(c => c.body.includes(MARKER));
            if (existing) {await github.rest.issues.updateComment({comment_id: existing.id,owner: context.repo.owner,repo: context.repo.repo,body: body});} else {await github.rest.issues.createComment({issue_number: context.issue.number,owner: context.repo.owner,repo: context.repo.repo,body: body});}
"""

        with open(".github/workflows/qa.yml", "w", encoding="utf-8") as f:
            f.write(qa_yml_content)

        console.print("[green].github/workflows/qa.yml 생성 완료![/green]")
        console.print("[dim]GitHub Secrets에 API 키를 등록하는 것을 잊지 마세요![/dim]")
