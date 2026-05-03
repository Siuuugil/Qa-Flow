import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class GeminiProvider:
    def __init__(self, system_prompt: str = ""):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash-lite"
        self.system_prompt = system_prompt

    def review(self, diff: str) -> str:
        if not diff:
            return "분석할 코드 변경사항이 없습니다."
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{self.system_prompt}\n\n다음 코드 변경사항을 리뷰해주세요:\n\n{diff}"
            )
            return response.text
        except Exception as e:
            return f"Gemini API 오류: {str(e)}"

    def chat(self, history: list) -> str:
        try:
            contents = "\n".join([
                f"{'User' if h['role'] == 'user' else 'AI'}: {h['content']}"
                for h in history
            ])
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{self.system_prompt}\n\n{contents}"
            )
            return response.text
        except Exception as e:
            return f"Gemini API 오류: {str(e)}"