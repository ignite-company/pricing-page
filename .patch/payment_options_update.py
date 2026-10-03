from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()
marker = '<!-- PAYMENT OPTIONS UPDATE V1 -->'
if marker in s:
    print('payment options update already applied')
    raise SystemExit(0)

# Systems Care: update optional post-90-day management price.
s = s.replace('$497', '$1,250')

# Remove the visible 3-payment selector.
s, n_buttons = re.subn(
    r'\n\s*<button class="bill-btn" data-term="3pay">\s*3 Payments\s*<span class="save">Lowest Upfront Cost</span>\s*</button>\s*',
    '\n',
    s,
    flags=re.S,
)

# Remove the two legacy 3-pay pricing objects from the JS pricing model.
s, n_foundation = re.subn(
    r"\n\s*'3pay':\s*\{\s*price:'\$650',.*?badge:\s*'3 payments · \$1,950 total'\s*\}\s*",
    '\n',
    s,
    flags=re.S,
)
s, n_growth = re.subn(
    r"\n\s*'3pay':\s*\{\s*price:'\$1,500',.*?badge:\s*'3 payments · \$4,500 total'\s*\}\s*",
    '\n',
    s,
    flags=re.S,
)

# Paid-in-full savings now compare against the only remaining payment plan: 2 payments.
replacements = {
    '$1,950 standard payment-plan total': '$1,700 payment-plan total',
    'Save $450 when paid in full': 'Save $200 when paid in full',
    'Pay in full and save $450': 'Pay in full and save $200',
    '$4,500 standard payment-plan total': '$4,000 payment-plan total',
    'Save $1,000 when paid in full': 'Save $500 when paid in full',
    'Pay in full and save $1,000': 'Pay in full and save $500',
}
for old, new in replacements.items():
    s = s.replace(old, new)

# Remove 3-pay references from the fine print.
s = re.sub(r'\n\s*The three-payment option is \$650 per payment for a total investment of \$1,950\.', '', s)
s = re.sub(r'\n\s*The three-payment option is \$1,500 per payment for a total investment of \$4,500\.', '', s)

# On mobile, the payment selector is now a clean two-column row.
s = re.sub(
    r'(#ignite-offers-v7 \.billing-toggle\{\s*display:grid;\s*)grid-template-columns:repeat\(3,minmax\(0,1fr\)\);',
    r'\1grid-template-columns:repeat(2,minmax(0,1fr));',
    s,
)

# Marker for idempotence and verification.
s = s.replace('</body>', marker + '\n</body>') if '</body>' in s else s + '\n' + marker + '\n'

# Guardrails: the requested presentation must be true in the output.
if '$497' in s:
    raise SystemExit('Legacy Systems Care price still present')
if 'data-term="3pay"' in s:
    raise SystemExit('3-pay selector still present')
if "'3pay':" in s:
    raise SystemExit('3-pay pricing model still present')
if 'three-payment option' in s:
    raise SystemExit('3-pay fine print still present')
if '$1,250' not in s:
    raise SystemExit('New Systems Care price missing')
if n_buttons != 1 or n_foundation != 1 or n_growth != 1:
    raise SystemExit(f'Unexpected match counts: button={n_buttons}, foundation={n_foundation}, growth={n_growth}')

p.write_text(s)
print('payment options updated')
