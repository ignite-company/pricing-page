<script>
(function(){
  var root = document.getElementById('ignite-roi-calculator');
  if(!root) return;

  var CPL = 16.2793944954;
  var SCALE_FEE = 3500;
  var FOUNDATION_FEE = 1500;
  var RECOVERY_LIFT = 2/3;
  var RECOVERY_OFFSETS = [11,18,26,45,75];
  var RECOVERY_WEIGHTS = [2/6,1/6,1/6,1/6,1/6];

  var ticket = document.getElementById('calc-ticket');
  var closeRate = document.getElementById('calc-close');
  var margin = document.getElementById('calc-margin');
  var budget = document.getElementById('calc-budget');

  function val(el, fallback){
    var n = parseFloat(el.value);
    return isFinite(n) ? n : fallback;
  }

  function clamp(n, min, max){
    return Math.min(max, Math.max(min, n));
  }

  function money(n){
    var sign = n < 0 ? '-' : '';
    return sign + '$' + Math.abs(n).toLocaleString('en-US',{maximumFractionDigits:0});
  }

  function number(n){
    return Math.round(n).toLocaleString('en-US');
  }

  function pct(n){
    return (n * 100).toFixed(n * 100 < 10 ? 1 : 0) + '%';
  }

  function simulate(days, avgTicket, immediateRate, profitMargin, dailyBudget){
    var dailyLeads = dailyBudget / CPL;
    var delayedRate = Math.min(immediateRate * RECOVERY_LIFT, Math.max(0, .95 - immediateRate));
    var revenue = new Array(days).fill(0);
    var jobs = new Array(days).fill(0);
    var immediateJobs = new Array(days).fill(0);
    var recoveredJobs = new Array(days).fill(0);

    for(var d=0; d<days; d++){
      var immediate = dailyLeads * immediateRate;
      immediateJobs[d] += immediate;
      jobs[d] += immediate;
      revenue[d] += immediate * avgTicket;

      for(var i=0;i<RECOVERY_OFFSETS.length;i++){
        var target = d + RECOVERY_OFFSETS[i];
        if(target < days){
          var recovered = dailyLeads * delayedRate * RECOVERY_WEIGHTS[i];
          recoveredJobs[target] += recovered;
          jobs[target] += recovered;
          revenue[target] += recovered * avgTicket;
        }
      }
    }

    var cumRevenue = 0;
    var cumJobs = 0;
    var cumImmediate = 0;
    var cumRecovered = 0;
    var breakEvenDay = null;
    var timeline = [];
    var checkpoints = {7:true,30:true,60:true,90:true};

    for(var day=1; day<=days; day++){
      cumRevenue += revenue[day-1];
      cumJobs += jobs[day-1];
      cumImmediate += immediateJobs[day-1];
      cumRecovered += recoveredJobs[day-1];

      var grossProfit = cumRevenue * profitMargin;
      var adSpend = dailyBudget * day;
      var net = grossProfit - adSpend - SCALE_FEE;

      if(breakEvenDay === null && net >= 0){
        breakEvenDay = day;
      }

      if(checkpoints[day]){
        timeline.push({
          day:day,
          jobs:cumJobs,
          revenue:cumRevenue,
          adSpend:adSpend,
          cac:cumJobs > 0 ? adSpend/cumJobs : 0
        });
      }
    }

    return {
      days:days,
      leads:dailyLeads * days,
      jobs:cumJobs,
      immediateJobs:cumImmediate,
      recoveredJobs:cumRecovered,
      revenue:cumRevenue,
      immediateRevenue:cumImmediate * avgTicket,
      recoveredRevenue:cumRecovered * avgTicket,
      grossProfit:cumRevenue * profitMargin,
      adSpend:dailyBudget * days,
      net:cumRevenue * profitMargin - dailyBudget * days - SCALE_FEE,
      breakEvenDay:breakEvenDay,
      cac:cumJobs > 0 ? (dailyBudget * days)/cumJobs : 0,
      eventualRate:Math.min(.95, immediateRate + delayedRate),
      timeline:timeline
    };
  }

  function setText(id, value){
    var el = document.getElementById(id);
    if(el) el.textContent = value;
  }

  function render(){
    var avgTicket = Math.max(1, val(ticket,500));
    var immediateRate = clamp(val(closeRate,18)/100, .01, .90);
    var profitMargin = clamp(val(margin,50)/100, .01, .95);
    var dailyBudget = Math.max(1, val(budget,50));

    var r90 = simulate(90,avgTicket,immediateRate,profitMargin,dailyBudget);
    var r180 = simulate(180,avgTicket,immediateRate,profitMargin,dailyBudget);
    var r365 = simulate(365,avgTicket,immediateRate,profitMargin,dailyBudget);

    setText('calc-revenue90',money(r90.revenue));
    setText('calc-breakeven',r365.breakEvenDay ? r365.breakEvenDay + ' days' : '365+ days');
    setText('calc-net90',money(r90.net));
    setText('calc-leads90',number(r90.leads));
    setText('calc-immediate-jobs',number(r90.immediateJobs));
    setText('calc-recovered-jobs','+'+number(r90.recoveredJobs));
    setText('calc-total-jobs',number(r90.jobs));
    setText('calc-adspend90',money(r90.adSpend));
    setText('calc-grossprofit90',money(r90.grossProfit));
    setText('calc-cac90',money(r90.cac));
    setText('calc-eventual-rate',pct(r90.eventualRate));
    setText('calc-immediate-revenue',money(r90.immediateRevenue));
    setText('calc-recovered-revenue','+'+money(r90.recoveredRevenue));

    var profitPerJob = avgTicket * profitMargin;
    var foundationJobs = profitPerJob > 0 ? Math.ceil(FOUNDATION_FEE / profitPerJob) : 0;
    setText('calc-foundation-jobs',foundationJobs + (foundationJobs === 1 ? ' job' : ' jobs'));
    setText('calc-foundation-detail','to recover $1,500 at ' + money(profitPerJob) + ' gross profit per job');

    var timeline = document.getElementById('calc-timeline');
    if(timeline){
      timeline.innerHTML = r90.timeline.map(function(t){
        return '<div class="timeline-card">' +
          '<div class="timeline-day">Day '+t.day+'</div>' +
          '<strong>'+money(t.revenue)+'</strong>' +
          '<p>'+number(t.jobs)+' cumulative jobs<br>Effective ad CAC: '+money(t.cac)+'</p>' +
        '</div>';
      }).join('');
    }

    var projections = document.getElementById('calc-projections');
    if(projections){
      var cards = [
        {label:'90 days',data:r90},
        {label:'6 months',data:r180},
        {label:'12 months',data:r365}
      ];
      projections.innerHTML = cards.map(function(c){
        return '<div class="projection-card">' +
          '<div class="period">'+c.label+'</div>' +
          '<div class="projection-revenue">'+money(c.data.revenue)+'</div>' +
          '<div class="projection-row"><span>Projected jobs</span><b>'+number(c.data.jobs)+'</b></div>' +
          '<div class="projection-row"><span>Gross profit</span><b>'+money(c.data.grossProfit)+'</b></div>' +
          '<div class="projection-row"><span>Ad spend</span><b>'+money(c.data.adSpend)+'</b></div>' +
          '<div class="projection-row"><span>Net after ads + initial Ignite</span><b>'+money(c.data.net)+'</b></div>' +
        '</div>';
      }).join('');
    }
  }

  [ticket,closeRate,margin,budget].forEach(function(el){
    el.addEventListener('input',render);
    el.addEventListener('change',render);
  });

  render();
})();
</script>
