from pathlib import Path

index = Path('index.html')
css_file = Path('.patch/mobile.css')

s = index.read_text()
css = css_file.read_text()

viewport = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
if 'name="viewport"' not in s and "name='viewport'" not in s:
    s = viewport + s

marker = '/* MOBILE OPTIMIZATION V1 — desktop styles are intentionally untouched */'
if marker not in s:
    if '</style>' not in s:
        raise SystemExit('Could not find closing style tag')
    s = s.replace('</style>', '\n' + css + '\n</style>', 1)

index.write_text(s)
print('mobile optimization applied')
