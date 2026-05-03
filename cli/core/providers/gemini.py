import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """당신은 시니어 개발자이자 QA 엔지니어입니다.
코드 변경사항을 분석하여 다음 항목을 검토하세요:

1. 버그 가능성
2. 코드 컨벤션 위반
3. 변수/함수 스코프 문제
4. 전체 구조에서 이 코드의 역할 설명

간결하고 명확하게 한국어로 답변하세요."""

class GeminiProvider:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"

    def review(self, diff: str) -> str:
        if not diff:
            return "분석할 코드 변경사항이 없습니다."
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{SYSTEM_PROMPT}\n\n다음 코드 변경사항을 리뷰해주세요:\n\n{diff}"
            )
            return response.text
        except Exception as e:
            return f"Gemini API 오류: {str(e)}"