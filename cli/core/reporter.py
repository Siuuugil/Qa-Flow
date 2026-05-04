import os
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


class Reporter:
    def __init__(self):
        self.report_dir = "qa-reports"
        os.makedirs(self.report_dir, exist_ok=True)

    def generate(self, ai_result: str = "", convention_result: str = "", focus: str = "general", mode: str = "full"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.report_dir, f"report_{timestamp}.json")

        has_violations = bool(convention_result and "위반" in convention_result)

        report = {
            "timestamp": timestamp,
            "ai_review": ai_result,
            "convention_check": convention_result,
            "has_violations": has_violations,
            "focus": focus,
            "mode": mode,
        }

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self._save_to_supabase(ai_result, convention_result, has_violations, focus, mode)

        table = Table(title="QA-Flow 리포트 요약")
        table.add_column("항목", style="cyan")
        table.add_column("결과", style="white")

        table.add_row("생성 시각", timestamp)
        table.add_row("AI 리뷰", "완료" if ai_result else "미실행")
        table.add_row("컨벤션 체크", "완료" if convention_result else "미실행")
        table.add_row("위반 여부", "있음" if has_violations else "없음")
        table.add_row("Focus", focus)
        table.add_row("저장 경로", report_path)

        console.print(table)

    def _save_to_supabase(self, ai_result: str, convention_result: str, has_violations: bool, focus: str = "general", mode: str = "full"):
        try:
            from supabase import create_client
            from dotenv import load_dotenv
            from pathlib import Path

            load_dotenv(dotenv_path=Path.cwd() / ".env", encoding="utf-8")

            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

            if not url or not key:
                console.print("[dim]Supabase 미설정 - 로컬 저장만 수행[/dim]")
                return

            client = create_client(url, key)

            # 로컬 환경에서는 GITHUB_REPOSITORY 없으므로 기본값 설정
            repo = os.getenv("GITHUB_REPOSITORY") or os.getenv("GITHUB_REPO", "unknown")
            provider = os.getenv("AI_PROVIDER", "unknown")

            client.table("reports").insert({
                "repo": repo,
                "branch": os.getenv("GITHUB_HEAD_REF", "local"),
                "provider": provider,
                "focus": focus,
                "mode": mode,
                "ai_review": ai_result,
                "convention_check": convention_result,
                "has_violations": has_violations,
            }).execute()

            console.print("[dim]Supabase 저장 완료[/dim]")

        except Exception as e:
            console.print(f"[dim]Supabase 저장 실패: {str(e)}[/dim]")
