from cli.core.providers.claude import ClaudeProvider
from cli.core.providers.gemini import GeminiProvider

class AIReview:
    def __init__(self, provider: str):
        if provider == "claude":
            self.provider = ClaudeProvider()
        elif provider == "gemini":
            self.provider = GeminiProvider()
        else:
            raise ValueError(f"지원하지 않는 provider: {provider}")

    def review(self) -> str:
        diff = self._get_git_diff()
        if not diff:
            return "변경된 코드가 없습니다."
        return self.provider.review(diff)

    def _get_git_diff(self) -> str:
        import subprocess
        result = subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True,
            text=True
        )
        return result.stdout