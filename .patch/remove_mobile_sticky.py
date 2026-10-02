from pathlib import Path

p = Path('index.html')
s = p.read_text()
marker = '/* REMOVE MOBILE INVESTMENT STICKY BUTTON */'
if marker in s:
    print('sticky button already removed')
    raise SystemExit(0)

css = r'''

/* REMOVE MOBILE INVESTMENT STICKY BUTTON */
@media (max-width:760px){
  #ignite-mobile-invest-jump{display:none!important}
  #ignite-offers-v7 .shell{padding-bottom:max(42px,env(safe-area-inset-bottom))}
}
'''

pos = s.rfind('</style>')
if pos == -1:
    raise SystemExit('No </style> found')
s = s[:pos] + css + '\n' + s[pos:]
p.write_text(s)
print('removed mobile sticky investment button')
