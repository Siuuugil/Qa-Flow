import os
import anthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeProvider:
    def __init__(self, system_prompt: str = ""):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.system_prompt = system_prompt

    def review(self, diff: str) -> str:
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
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