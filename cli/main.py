import os
from collections import OrderedDict
os.environ["PYTHONIOENCODING"] = "utf-8"  # noqa: E402
os.environ["PYTHONUTF8"] = "1"  # noqa: E402

from cli.commands.chat import chat  # noqa: E402
from cli.commands.init import init  # noqa: E402
from cli.commands.scan import scan  # noqa: E402
from cli.commands.tc import tc  # noqa: E402
from cli.commands.jira_cmd import jira  # noqa: E402
import click  # noqa: E402


@click.group(commands=OrderedDict([
    ('init', init),
    ('scan', scan),
    ('chat', chat),
    ('tc', tc),
    ('jira', jira),
    ('s', scan),
    ('c', chat),
    ('t', tc),
    ('j', jira),
]))
@click.version_option(version="0.1.8", prog_name="qa-flow")
def main():
    """QA-Flow: AI 기반 코드 품질 자동화 툴

    \b
    [빠른 시작]
    qa-flow init                              # 초기 설정
    qa-flow scan -F app.py -f qa -r -t -j    # 분석 + TC + Jira 한번에
    qa-flow tc                                # 마지막 리포트로 TC 생성
    qa-flow jira                              # 마지막 TC로 Jira 등록

    \b
    [Focus 옵션 (-f)]
    structure  | 코드 구조 및 의존관계
    convention | 네이밍 규칙 및 코드 스타일
    security   | 보안 취약점
    bug        | 버그 및 예외처리
    qa         | QA 관점 테스트 가능성
    dev        | 개발자 관점 코드 품질
    performance| 성능 문제 및 최적화
    test       | 테스트 케이스 제안
    general    | 종합 리뷰 (기본값)

    \b
    [단축 명령어]
    s = scan, c = chat, t = tc, j = jira
    """
    pass


if __name__ == "__main__":
    main()