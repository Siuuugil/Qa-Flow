import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """당신은 시니어 개발자이자 QA 엔지니어입니다.
코드 변경사항을 분석하여 다음 항목을 검토하세요:

1. 버그 가능성
2. 코드 컨벤션 위반
3. 변수/함수 스코프 문제
4. 전체 구조에서 이 코드의 역할 설명

간결하고 명확하게 한국어로 답변하세요."""

class ClaudeProvider:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        self.client = anthropic.Anthropic(api_key=api_key)

    def review(self, diff: str) -> str:
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"다음 코드 변경사항을 리뷰해주세요:\n\n{diff}"
                }
            ]
        )
        return message.content[0].text
    
    def chat(self, history: list) -> str:
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=self.system_prompt,
                messages=history
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude API 오류: {str(e)}"