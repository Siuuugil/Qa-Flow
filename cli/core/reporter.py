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

    def generate(self, ai_result: str = "", convention_result: str = ""):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.report_dir, f"report_{timestamp}.json")

        report = {
            "timestamp": timestamp,
            "ai_review": ai_result,
            "convention_check": convention_result,
        }

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # 터미널에 요약 테이블 출력
        table = Table(title="QA-Flow 리포트 요약")
        table.add_column("항목", style="cyan")
        table.add_column("결과", style="white")

        table.add_row("생성 시각", timestamp)
        table.add_row("AI 리뷰", "완료" if ai_result else "미실행")
        table.add_row("컨벤션 체크", "완료" if convention_result else "미실행")
        table.add_row("저장 경로", report_path)

        console.print(table)