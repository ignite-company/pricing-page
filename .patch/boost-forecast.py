from pathlib import Path

path = Path('index.html')
s = path.read_text()

def replace_once(old, new):
    global s
    if old not in s:
        raise SystemExit('Missing expected text: ' + old[:120])
    s = s.replace(old, new, 1)

replace_once(
    "The forecast below is intentionally more conservative: it is calibrated to Wranglin Wranglers' real campaign of 44 website leads from $1,463.54 in ad spend, 9 closed/completed jobs, and approximately $6,000 collected over 29.27 days.",
    "The forecast below starts with Wranglin Wranglers' real campaign of 44 website leads from $1,463.54 in ad spend, then applies a modeled 20% optimization uplift to lead volume. That uplift is a planning assumption, not a historical guarantee."
)

replace_once(
    "Revenue from projected paid-lead jobs plus modeled follow-up and reactivation recoveries. Recovery matures conservatively from 5% of initially unclosed leads by 90 days, to 8% by 6 months and 10% by 12 months.",
    "Revenue from projected paid-lead jobs plus modeled follow-up and reactivation recoveries. The model includes a 20% optimization uplift to lead volume and assumes 10% of initially unclosed leads are recovered by 90 days, 13% by 6 months, and 15% by 12 months."
)

replace_once(
    '<span class="calc-kicker">90-day net impact</span>',
    '<span class="calc-kicker">Profit after ad spend</span>'
)
replace_once(
    "Projected gross profit after advertising and the total implementation investment.",
    "Projected gross profit remaining after advertising spend."
)
replace_once(
    "Modeled from the leads that do not close initially: 5% recovered by 90 days, 8% cumulatively by 6 months, and 10% cumulatively by 12 months. This is a planning assumption, not guaranteed revenue.",
    "Modeled from the leads that do not close initially: 10% recovered by 90 days, 13% cumulatively by 6 months, and 15% cumulatively by 12 months. This is a planning assumption, not guaranteed revenue."
)
replace_once(
    "Same budget + performance, with recovery maturing from 5% to 8% to 10%",
    "Same budget + performance, with recovery maturing from 10% to 13% to 15%"
)

replace_once(
    "  var FOUNDATION_FEE = 1500;\n",
    "  var FOUNDATION_FEE = 1500;\n  var SYSTEM_UPLIFT = 1.20;\n"
)

replace_once(
    "    // 5% by 90 days, 8% by 6 months, 10% by 12 months.\n    if(days <= 0) return 0;\n    if(days <= 90) return .05 * (days / 90);\n    if(days <= 180) return .05 + (.03 * ((days - 90) / 90));\n    if(days <= 365) return .08 + (.02 * ((days - 180) / 185));\n    return .10;",
    "    // 10% by 90 days, 13% by 6 months, 15% by 12 months.\n    if(days <= 0) return 0;\n    if(days <= 90) return .10 * (days / 90);\n    if(days <= 180) return .10 + (.03 * ((days - 90) / 90));\n    if(days <= 365) return .13 + (.02 * ((days - 180) / 185));\n    return .15;"
)

replace_once(
    "    var leads = adSpend / BASE_CPL;",
    "    var leads = (adSpend / BASE_CPL) * SYSTEM_UPLIFT;"
)
replace_once(
    "    var grossProfit = revenue * profitMargin;\n    var net = grossProfit - adSpend - SCALE_FEE;",
    "    var grossProfit = revenue * profitMargin;\n    var profitAfterAds = grossProfit - adSpend;\n    var net = profitAfterAds - SCALE_FEE;"
)
replace_once(
    "      grossProfit:grossProfit,\n      adSpend:adSpend,",
    "      grossProfit:grossProfit,\n      profitAfterAds:profitAfterAds,\n      adSpend:adSpend,"
)
replace_once(
    "    setText('calc-net90',money(r90.net));",
    "    setText('calc-net90',money(r90.profitAfterAds));"
)

# Add the new top-line profit metric into the longer-term cards while keeping true net visible.
replace_once(
    "          '<div class=\"projection-row\"><span>Gross profit</span><b>'+money(c.data.grossProfit)+'</b></div>' +\n          '<div class=\"projection-row\"><span>Ad spend</span><b>'+money(c.data.adSpend)+'</b></div>' +",
    "          '<div class=\"projection-row\"><span>Gross profit</span><b>'+money(c.data.grossProfit)+'</b></div>' +\n          '<div class=\"projection-row\"><span>Ad spend</span><b>'+money(c.data.adSpend)+'</b></div>' +\n          '<div class=\"projection-row\"><span>Profit after ad spend</span><b>'+money(c.data.profitAfterAds)+'</b></div>' +"
)

# Replace the calculator disclaimer as one complete block so assumptions are explicit.
start_marker = '      <div class="calc-disclaimer">'
start = s.index(start_marker)
end = s.index('      </div>', start) + len('      </div>')
new_disclaimer = '''      <div class="calc-disclaimer">
        Projection model, not a guarantee. The proof summary above reflects 2,000+ tracked leads and $25,000+ in documented ad spend across Ignite's broader campaign history. The forecast starts from Wranglin Wranglers' measured $33.26 CPL and applies a 20% modeled optimization uplift to lead volume, equivalent to roughly a $27.72 modeled CPL. That uplift is a planning assumption, not historical performance. The lead-to-job close rate entered above then controls initial job volume. Follow-up and reactivation are modeled only on leads that do not close initially: 10% recovered by 90 days, 13% cumulatively by 6 months, and 15% cumulatively by 12 months. Those recovery rates are also planning assumptions, not guaranteed outcomes. Profit uses the margin entered above. Profit after ad spend subtracts advertising spend but does not subtract the Ignite implementation fee; the longer-term net rows subtract both advertising spend and the initial Scale implementation investment. Actual results vary by market, service mix, pricing, lead quality, sales ability, seasonality, response speed, budget, and execution.
      </div>'''
s = s[:start] + new_disclaimer + s[end:]

# Verification
checks = [
    'Profit after ad spend',
    'var SYSTEM_UPLIFT = 1.20;',
    '10% recovered by 90 days',
    '13% cumulatively by 6 months',
    '15% cumulatively by 12 months',
    "setText('calc-net90',money(r90.profitAfterAds));",
    'equivalent to roughly a $27.72 modeled CPL'
]
for item in checks:
    if item not in s:
        raise SystemExit('Verification failed: ' + item)
if '90-day net impact' in s:
    raise SystemExit('Old headline still present')

path.write_text(s)
print('updated', len(s), 'chars')
