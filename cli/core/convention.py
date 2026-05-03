import subprocess
import os
from rich.console import Console

console = Console()

class ConventionChecker:
    def check(self) -> str:
        results = []

        # ESLint 체크 (JS/TS 파일이 있을 때)
        if self._has_js_files():
            eslint_result = self._run_eslint()
            results.append(eslint_result)

        # Python 파일 체크
        if self._has_py_files():
            flake8_result = self._run_flake8()
            results.append(flake8_result)

        if not results:
            return "체크할 파일이 없습니다."

        return "\n".join(results)

    def _has_js_files(self) -> bool:
        result = subprocess.run(
            ["git", "diff", "HEAD", "--name-only"],
            capture_output=True, text=True
        )
        files = result.stdout.strip().split("\n")
        return any(f.endswith((".js", ".ts", ".jsx", ".tsx")) for f in files)

    def _has_py_files(self) -> bool:
        result = subprocess.run(
            ["git", "diff", "HEAD", "--name-only"],
            capture_output=True, text=True
        )
        files = result.stdout.strip().split("\n")
        return any(f.endswith(".py") for f in files)

    def _run_eslint(self) -> str:
        result = subprocess.run(
            ["npx", "eslint", "--ext", ".js,.ts,.jsx,.tsx", "."],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return "[ESLint] 컨벤션 위반 없음"
        return f"[ESLint] 위반 사항:\n{result.stdout}"

    def _run_flake8(self) -> str:
        result = subprocess.run(
            ["flake8", "--max-line-length=100", "."],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return "[Flake8] 컨벤션 위반 없음"
        return f"[Flake8] 위반 사항:\n{result.stdout}"