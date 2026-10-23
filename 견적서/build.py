#!/usr/bin/env python3
"""src/app.html 에 vendor/ 의 엑셀 라이브러리를 넣어 배포용 견적서_자동화.html 을 만든다.

배포 파일은 인터넷 없이도 엑셀 받기·불러오기가 된다.
src/app.html 을 고친 뒤에는 이 스크립트를 다시 실행한다:  python3 견적서/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKER = '<!-- @vendor -->'
VENDOR = ['exceljs.min.js', 'jszip.min.js']


def inline_script(name: str) -> str:
    js = (ROOT / 'vendor' / name).read_text(encoding='utf-8')
    # 인라인 <script> 안에서 문서를 깨뜨릴 수 있는 문자열이 없는지 확인
    for bad in ('</script', '<!--'):
        if bad in js.lower():
            raise SystemExit(f'{name}: "{bad}" 가 들어 있어 인라인으로 넣을 수 없어요.')
    return f'<script>/* {name} — 라이선스: vendor/ 폴더 참고 */\n{js}\n</script>'


def main() -> None:
    src = (ROOT / 'src' / 'app.html').read_text(encoding='utf-8')
    if src.count(MARKER) != 1:
        raise SystemExit(f'src/app.html 에 {MARKER} 표시가 정확히 한 번 있어야 해요.')
    out = src.replace(MARKER, '\n'.join(inline_script(n) for n in VENDOR))
    dest = ROOT / '견적서_자동화.html'
    dest.write_text(out, encoding='utf-8')
    print(f'{dest.name} 생성 ({dest.stat().st_size / 1024 / 1024:.2f} MB)')


if __name__ == '__main__':
    main()
