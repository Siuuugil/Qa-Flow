import subprocess
from rich.console import Console

console = Console()


class ConventionChecker:
    def check(self) -> str:
        results = []

        if self._has_js_files():
            eslint_result = self._run_eslint()
            results.append(eslint_result)

        if self._has_py_files():
            flake8_result = self._run_flake8()
            results.append(flake8_result)

        if not results:
            return "체크할 파일이 없습니다."

        return "\n".join(results)

    def _get_changed_files(self) -> list:
        import os

        base = os.getenv("GITHUB_BASE_REF")
        if base:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"origin/{base}...HEAD"],
                capture_output=True, text=True, encoding="utf-8"
            )
        else:
            result = subprocess.run(
                ["git", "diff", "HEAD", "--name-only"],
                capture_output=True, text=True, encoding="utf-8"
            )
        return result.stdout.strip().split("\n")

    def _has_js_files(self) -> bool:
        files = self._get_changed_files()
        return any(f.endswith((".js", ".ts", ".jsx", ".tsx")) for f in files)

    def _has_py_files(self) -> bool:
        files = self._get_changed_files()
        return any(f.endswith(".py") for f in files)

    def _run_eslint(self) -> str:
        try:
            result = subprocess.run(
                ["npx", "eslint", "--ext", ".js,.ts,.jsx,.tsx", "."],
                capture_output=True, text=True, encoding="utf-8"
            )
            if result.returncode == 0:
                return "[ESLint] 컨벤션 위반 없음"
            return f"[ESLint] 위반 사항:\n{result.stdout}"
        except FileNotFoundError:
            return "[ESLint] 설치되지 않아 스킵합니다."

    def _run_flake8(self) -> str:
        try:
            result = subprocess.run(
                ["flake8", "--max-line-length=100", "--exclude=dashboard/node_modules,node_modules,.git","."],
                capture_output=True, text=True, encoding="utf-8", errors="replace"
            )
            if result.returncode == 0:
                return "[Flake8] 컨벤션 위반 없음"
            return f"[Flake8] 위반 사항:\n{result.stdout}"
        except FileNotFoundError:
            return "[Flake8] 설치되지 않아 스킵합니다."
