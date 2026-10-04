from pathlib import Path

p = Path('index.html')
s = p.read_text()

urls = [
    'https://assets.cdn.filesafe.space/bF1dT8IAVuvat84LkAVe/media/6ac2de84c478ac5535cbb5c8.png',
    'https://assets.cdn.filesafe.space/bF1dT8IAVuvat84LkAVe/media/6ac2de99195f9172ed72732a.png',
    'https://assets.cdn.filesafe.space/bF1dT8IAVuvat84LkAVe/media/6ac2dea9bbad531ac8b39f7b.png',
]

if all(u in s for u in urls):
    raise SystemExit('proof images already present')

marker = '      <div class="calc-evidence">'
start = s.index('<div class="calc-proof-window"')
end = s.index(marker, start)
block = s[start:end]

first_group_close = '          </div>\n          <div style="display:flex;gap:12px;" aria-hidden="true">'
if first_group_close not in block:
    raise SystemExit('first proof group marker not found')

first_cards = ''.join(
    f'          <div class="calc-proof-card"><img src="{u}" alt="Ignite client result" loading="lazy"></div>\n'
    for u in urls
)
block = block.replace(first_group_close, first_cards + first_group_close, 1)

second_close = '          </div>\n        </div>\n      </div>\n\n'
if second_close not in block:
    raise SystemExit('second proof group close marker not found')

second_cards = ''.join(
    f'          <div class="calc-proof-card"><img src="{u}" alt="" loading="lazy"></div>\n'
    for u in urls
)
block = block.replace(second_close, second_cards + second_close, 1)

s = s[:start] + block + s[end:]
p.write_text(s)
print('added 3 proof images to both carousel tracks')
