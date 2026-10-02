from pathlib import Path
p=Path('index.html')
s=p.read_text()

# 1) Remove old foundation payback card from the main input column.
old='''          <div class="foundation-payback">\n            <div>\n              <h4>Foundation Build recovery</h4>\n              <p>The $1,500 Foundation Build does not include paid advertising, so the cleanest payback measurement is how many average-profit jobs are needed to recover the implementation.</p>\n            </div>\n            <div class="foundation-number">\n              <strong id="calc-foundation-jobs">6 jobs</strong>\n              <span id="calc-foundation-detail">to recover $1,500</span>\n            </div>\n          </div>\n'''
assert old in s
s=s.replace(old,'')

# 2) Remove the short-horizon timeline section entirely.
old='''          <div class="calc-section-title"><h4>What happens as the system keeps working</h4><span>Revenue and CAC mature as older leads convert</span></div>\n          <div class="calc-timeline" id="calc-timeline"></div>\n\n'''
assert old in s
s=s.replace(old,'')

# 3) Hide investment amounts in calculator copy.
s=s.replace('When projected gross profit has covered ad spend and the $3,500 Scale investment.',
            'When projected gross profit has covered advertising and the total growth investment.')
s=s.replace('Projected gross profit minus ad spend and the $3,500 Ignite investment.',
            'Projected gross profit after advertising and the total implementation investment.')

# 4) Add standalone Foundation mini calculator at the bottom of the ROI calculator.
anchor='''      </div>\n\n      <div class="calc-disclaimer">\n'''
assert anchor in s
foundation='''      </div>\n\n      <section class="foundation-mini" aria-label="Foundation recovery calculator">\n        <div class="foundation-mini-head">\n          <div>\n            <div class="eyebrow">Foundation recovery calculator</div>\n            <h4>How quickly can the foundation pay for itself?</h4>\n            <p>This model uses your average ticket and margin from above, then looks at the organic opportunities you already receive from Google, your website, referrals, and social channels. It does not assume any extra lift from stronger reviews, a better Business Profile, improved website conversion, or stronger social proof.</p>\n          </div>\n          <div class="foundation-proof-note">\n            <strong>Why this matters before adding more ad spend</strong>\n            <p>Google says complete and accurate Business Profile information makes a business more likely to appear in local results, while more reviews and positive ratings can help local ranking. BrightLocal's 2026 consumer survey found 97% of consumers read local-business reviews, and 54% visit a business website after reading positive reviews.</p>\n          </div>\n        </div>\n\n        <div class="foundation-mini-grid">\n          <div class="foundation-mini-inputs">\n            <div class="calc-field">\n              <div class="calc-label"><label for="foundation-organic-leads">Current organic leads per month</label><span>Google, website, referrals, social</span></div>\n              <div class="calc-input-wrap"><input class="calc-input no-prefix" id="foundation-organic-leads" type="number" inputmode="decimal" min="0" step="1" value="12"><span class="calc-suffix">/mo</span></div>\n            </div>\n\n            <div class="calc-field">\n              <div class="calc-label"><label for="foundation-organic-close">Organic lead-to-job close rate</label><span>How many current organic leads become jobs</span></div>\n              <div class="calc-input-wrap"><input class="calc-input no-prefix" id="foundation-organic-close" type="number" inputmode="decimal" min="1" max="95" step="1" value="25"><span class="calc-suffix">%</span></div>\n            </div>\n\n            <p class="foundation-mini-hint">The recovery estimate is intentionally based on your current organic lead flow. Any improvement created by better reviews, stronger Google visibility, a more credible website, or better follow-up is upside that is not baked into the number.</p>\n          </div>\n\n          <div class="foundation-mini-results">\n            <div class="foundation-result primary">\n              <span>Jobs needed to recover the investment</span>\n              <strong id="calc-foundation-jobs">0 jobs</strong>\n              <small>Based on your average ticket and profit margin.</small>\n            </div>\n            <div class="foundation-result">\n              <span>Estimated recovery at your current organic pace</span>\n              <strong id="calc-foundation-time">-</strong>\n              <small id="calc-foundation-time-detail">Enter your current monthly organic lead flow.</small>\n            </div>\n            <div class="foundation-result">\n              <span>Current modeled organic job pace</span>\n              <strong id="calc-foundation-jobs-month">0 / mo</strong>\n              <small>Before assuming any lift from the Foundation systems.</small>\n            </div>\n          </div>\n        </div>\n\n        <div class="foundation-stats">\n          <div><strong>97%</strong><span>of consumers read reviews for local businesses</span></div>\n          <div><strong>54%</strong><span>visit a business website after reading positive reviews</span></div>\n          <div><strong>24%</strong><span>visit a business's social channels after positive reviews</span></div>\n          <div><strong>Google</strong><span>says more reviews and positive ratings can help local ranking</span></div>\n        </div>\n        <p class="foundation-sources">Consumer behavior figures: BrightLocal Local Consumer Review Survey 2026. Google ranking guidance: Google Business Profile Help. These are local-business benchmarks, not junk-removal-specific performance guarantees.</p>\n      </section>\n\n      <div class="calc-disclaimer">\n'''
s=s.replace(anchor,foundation,1)

# 5) Update longer-term projection copy to avoid pricing terminology.
s=s.replace('Net after ads + initial Ignite','Net after ads + implementation')

# 6) Remove timeline collection/rendering from the model.
s=s.replace('''    var timeline = [];\n    var checkpoints = {7:true,30:true,60:true,90:true};\n''','')
s=s.replace('''\n      if(checkpoints[day]){\n        timeline.push({\n          day:day,\n          jobs:cumJobs,\n          revenue:cumRevenue,\n          adSpend:adSpend,\n          cac:cumJobs > 0 ? adSpend/cumJobs : 0\n        });\n      }\n''','\n')
s=s.replace('''      eventualRate:Math.min(.95, immediateRate + delayedRate),\n      timeline:timeline\n''','''      eventualRate:Math.min(.95, immediateRate + delayedRate)\n''')
s=s.replace('''\n    var timeline = document.getElementById('calc-timeline');\n    if(timeline){\n      timeline.innerHTML = r90.timeline.map(function(t){\n        return '<div class="timeline-card">' +\n          '<div class="timeline-day">Day '+t.day+'</div>' +\n          '<strong>'+money(t.revenue)+'</strong>' +\n          '<p>'+number(t.jobs)+' cumulative jobs<br>Effective ad CAC: '+money(t.cac)+'</p>' +\n        '</div>';\n      }).join('');\n    }\n''','\n')

# 7) Add foundation inputs to JS and calculate hidden-price recovery without showing amount.
s=s.replace("  var budget = document.getElementById('calc-budget');\n",
'''  var budget = document.getElementById('calc-budget');\n  var foundationOrganicLeads = document.getElementById('foundation-organic-leads');\n  var foundationOrganicClose = document.getElementById('foundation-organic-close');\n''')

old_js='''    var profitPerJob = avgTicket * profitMargin;\n    var foundationJobs = profitPerJob > 0 ? Math.ceil(FOUNDATION_FEE / profitPerJob) : 0;\n    setText('calc-foundation-jobs',foundationJobs + (foundationJobs === 1 ? ' job' : ' jobs'));\n    setText('calc-foundation-detail','to recover $1,500 at ' + money(profitPerJob) + ' gross profit per job');\n'''
assert old_js in s
new_js='''    var profitPerJob = avgTicket * profitMargin;\n    var foundationJobs = profitPerJob > 0 ? Math.ceil(FOUNDATION_FEE / profitPerJob) : 0;\n    var organicLeads = foundationOrganicLeads ? Math.max(0, val(foundationOrganicLeads,12)) : 0;\n    var organicClose = foundationOrganicClose ? clamp(val(foundationOrganicClose,25)/100, .01, .95) : .25;\n    var organicJobsPerMonth = organicLeads * organicClose;\n    var organicGrossProfitPerMonth = organicJobsPerMonth * profitPerJob;\n    var foundationMonths = organicGrossProfitPerMonth > 0 ? FOUNDATION_FEE / organicGrossProfitPerMonth : null;\n    var foundationDays = foundationMonths !== null ? Math.max(1, Math.ceil(foundationMonths * 30.44)) : null;\n\n    setText('calc-foundation-jobs',foundationJobs + (foundationJobs === 1 ? ' job' : ' jobs'));\n    setText('calc-foundation-jobs-month',organicJobsPerMonth.toFixed(organicJobsPerMonth < 10 ? 1 : 0) + ' / mo');\n    setText('calc-foundation-time',foundationDays ? foundationDays + (foundationDays === 1 ? ' day' : ' days') : '-');\n    setText('calc-foundation-time-detail',foundationDays ? 'At your current organic lead pace, before assuming any lift from the new systems.' : 'Enter your current monthly organic lead flow.');\n'''
s=s.replace(old_js,new_js)

s=s.replace("  [ticket,closeRate,margin,budget].forEach(function(el){\n    el.addEventListener('input',render);\n    el.addEventListener('change',render);\n  });",
'''  [ticket,closeRate,margin,budget,foundationOrganicLeads,foundationOrganicClose].filter(Boolean).forEach(function(el){\n    el.addEventListener('input',render);\n    el.addEventListener('change',render);\n  });''')

# 8) Add screen-share typography overrides + Foundation mini styles at the very end of CSS.
css=Path('.patch/extra.css').read_text()
assert '</style>' in s
s=s.replace('</style>','\n'+css+'\n</style>',1)

p.write_text(s)
print('updated index.html',len(s),s.count('\n')+1)
