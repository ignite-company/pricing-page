from pathlib import Path

p = Path('index.html')
s = p.read_text()

old_hint = '''            <div class="calc-input-hint">Wranglin Wranglers converted 9 of 44 tracked website leads into closed/completed jobs, or 20.5%. To keep the forecast conservative, the model uses the lower of your entered close rate and that measured 20.5% benchmark. No extra follow-up lift is automatically added.</div>\n'''
if old_hint in s:
    s = s.replace(old_hint, '', 1)
else:
    # Fallback: remove any current helper directly beneath the close-rate input.
    anchor = '<div class="calc-input-wrap"><input class="calc-input no-prefix" id="calc-close"'
    pos = s.find(anchor)
    if pos == -1:
        raise SystemExit('close-rate input not found')
    hint_start = s.find('<div class="calc-input-hint">', pos)
    next_field = s.find('<div class="calc-field">', pos + len(anchor))
    if hint_start != -1 and (next_field == -1 or hint_start < next_field):
        hint_end = s.find('</div>', hint_start)
        if hint_end == -1:
            raise SystemExit('close-rate helper closing tag not found')
        hint_end += len('</div>')
        while hint_end < len(s) and s[hint_end] in '\r\n':
            hint_end += 1
        s = s[:hint_start] + s[hint_end:]

old_sim = '''  function simulate(days, avgTicket, enteredCloseRate, profitMargin, dailyBudget){\n    // Never assume better paid-lead conversion than the measured Wranglin baseline.\n    // If the prospect's real close rate is lower, honor the lower number.\n    var modeledClose = Math.min(enteredCloseRate, BASE_CLOSE);\n'''
new_sim = '''  function simulate(days, avgTicket, enteredCloseRate, profitMargin, dailyBudget){\n    // Wranglin anchors lead cost. The prospect's entered close rate controls conversion.\n    // No nurture, reactivation, repeat, or referral lift is automatically added.\n    var modeledClose = enteredCloseRate;\n'''
if old_sim not in s:
    raise SystemExit('old simulate close-rate logic not found')
s = s.replace(old_sim, new_sim, 1)

old_disclaimer = "Forecast math is intentionally calibrated to the Wranglin Wranglers case: $1,463.54 ad spend produced 44 tracked website leads at $33.26 per lead, with 9 closed/completed jobs and approximately $6,000 collected over 29.27 days. The model uses that $33.26 CPL and will not assume a paid-lead close rate above the observed 9-of-44 rate of 20.5%; a lower close rate entered above is respected. No additional follow-up, reactivation, repeat, referral, or database revenue is automatically added."
new_disclaimer = "Forecast math is intentionally calibrated to the Wranglin Wranglers case: $1,463.54 ad spend produced 44 tracked website leads at $33.26 per lead, with 9 closed/completed jobs and approximately $6,000 collected over 29.27 days. The model uses that real $33.26 CPL to estimate lead volume, then applies the lead-to-job close rate entered above to estimate jobs. No additional follow-up, reactivation, repeat, referral, or database revenue is automatically added."
if old_disclaimer not in s:
    raise SystemExit('old disclaimer model copy not found')
s = s.replace(old_disclaimer, new_disclaimer, 1)

old_hero = 'Revenue from projected paid-lead jobs using the grounded Wranglin campaign baseline. No extra nurture or reactivation revenue is automatically added.'
new_hero = 'Revenue from projected paid-lead jobs using Wranglin\'s measured lead-cost baseline and the close rate you enter. No extra nurture or reactivation revenue is automatically added.'
if old_hero in s:
    s = s.replace(old_hero, new_hero, 1)

# Verification
assert 'var modeledClose = enteredCloseRate;' in s
assert 'Math.min(enteredCloseRate, BASE_CLOSE)' not in s
assert 'will not assume a paid-lead close rate above' not in s
assert 'id="calc-close"' in s

close_pos = s.find('id="calc-close"')
next_field = s.find('<div class="calc-field">', close_pos + 1)
segment = s[close_pos:next_field if next_field != -1 else close_pos + 2000]
assert 'calc-input-hint' not in segment

p.write_text(s)
print('close-rate input now drives projections and helper text is removed')
