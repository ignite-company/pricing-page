from pathlib import Path

p=Path('index.html')
s=p.read_text()

start=s.index('<div class="calc-proof-window"')
end=s.index('<div class="calc-evidence">', start)
block=s[start:end]
block=block.replace(' loading="lazy"',' loading="eager" decoding="async"')
s=s[:start]+block+s[end:]

marker='<!-- PROOF LIGHTBOX + RELIABLE LOADING V1 -->'
if marker not in s:
    addition=r'''
<!-- PROOF LIGHTBOX + RELIABLE LOADING V1 -->
<style>
#ignite-offers-v7 .calc-proof-card{cursor:zoom-in;}
#ignite-offers-v7 .calc-proof-window:hover .calc-proof-track{animation-play-state:running;}
#ignite-offers-v7 .calc-proof-window.proof-paused .calc-proof-track{animation-play-state:paused!important;}
#ignite-proof-lightbox{position:fixed;inset:0;z-index:2147483000;display:none;align-items:center;justify-content:center;padding:24px;background:rgba(2,4,7,.92);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);}
#ignite-proof-lightbox.open{display:flex;}
#ignite-proof-lightbox .proof-lightbox-inner{position:relative;max-width:min(1180px,94vw);max-height:92vh;display:flex;align-items:center;justify-content:center;}
#ignite-proof-lightbox img{display:block;max-width:94vw;max-height:88vh;width:auto;height:auto;object-fit:contain;border-radius:14px;box-shadow:0 28px 100px rgba(0,0,0,.65);background:#0a0d10;}
#ignite-proof-lightbox .proof-lightbox-close{position:absolute;right:-12px;top:-12px;width:40px;height:40px;border-radius:999px;border:1px solid rgba(255,255,255,.18);background:#11161c;color:#fff;font-size:24px;line-height:1;display:grid;place-items:center;cursor:pointer;box-shadow:0 12px 30px rgba(0,0,0,.4);}
@media(max-width:760px){#ignite-proof-lightbox{padding:14px;}#ignite-proof-lightbox img{max-width:96vw;max-height:84vh;border-radius:10px;}#ignite-proof-lightbox .proof-lightbox-close{right:4px;top:-48px;}}
</style>
<script>
(function(){
  var win=document.querySelector('#ignite-offers-v7 .calc-proof-window');
  if(!win) return;
  var track=win.querySelector('.calc-proof-track');
  var imgs=[].slice.call(win.querySelectorAll('.calc-proof-card img'));
  imgs.forEach(function(img){img.loading='eager';img.decoding='async';});

  var lb=document.createElement('div');
  lb.id='ignite-proof-lightbox';
  lb.setAttribute('aria-hidden','true');
  lb.innerHTML='<div class="proof-lightbox-inner"><img alt="Expanded proof screenshot"><button class="proof-lightbox-close" type="button" aria-label="Close proof image">×</button></div>';
  document.body.appendChild(lb);
  var lbImg=lb.querySelector('img');
  var closeBtn=lb.querySelector('.proof-lightbox-close');

  function openProof(src,alt){
    if(!src) return;
    win.classList.add('proof-paused');
    lbImg.src=src;
    lbImg.alt=alt || 'Expanded proof screenshot';
    lb.classList.add('open');
    lb.setAttribute('aria-hidden','false');
    document.documentElement.style.overflow='hidden';
  }
  function resumeProofTrack(){
    if(!track) return;
    track.style.animationPlayState='running';
    if(track.getAnimations){
      track.getAnimations().forEach(function(anim){try{anim.play();}catch(e){}});
    }
    requestAnimationFrame(function(){
      track.style.animationPlayState='running';
      if(track.getAnimations){
        track.getAnimations().forEach(function(anim){try{anim.play();}catch(e){}});
      }
    });
  }
  function closeProof(){
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden','true');
    lbImg.removeAttribute('src');
    document.documentElement.style.overflow='';
    win.classList.remove('proof-paused');
    resumeProofTrack();
  }

  win.addEventListener('click',function(e){
    var img=e.target.closest && e.target.closest('.calc-proof-card img');
    if(!img) return;
    openProof(img.currentSrc || img.src,img.alt);
  });
  closeBtn.addEventListener('click',function(e){e.stopPropagation();closeProof();});
  lb.addEventListener('click',function(e){if(e.target===lb) closeProof();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape' && lb.classList.contains('open')) closeProof();});
  document.addEventListener('visibilitychange',function(){
    if(!document.hidden && !lb.classList.contains('open')) resumeProofTrack();
  });
})();
</script>
'''
    s=s.replace('<!-- PAYMENT OPTIONS UPDATE V1 -->', addition+'\n<!-- PAYMENT OPTIONS UPDATE V1 -->')
else:
    old="""  function closeProof(){\n    lb.classList.remove('open');\n    lb.setAttribute('aria-hidden','true');\n    lbImg.removeAttribute('src');\n    document.documentElement.style.overflow='';\n    win.classList.remove('proof-paused');\n  }"""
    new="""  function resumeProofTrack(){\n    if(!track) return;\n    track.style.animationPlayState='running';\n    if(track.getAnimations){\n      track.getAnimations().forEach(function(anim){try{anim.play();}catch(e){}});\n    }\n    requestAnimationFrame(function(){\n      track.style.animationPlayState='running';\n      if(track.getAnimations){\n        track.getAnimations().forEach(function(anim){try{anim.play();}catch(e){}});\n      }\n    });\n  }\n  function closeProof(){\n    lb.classList.remove('open');\n    lb.setAttribute('aria-hidden','true');\n    lbImg.removeAttribute('src');\n    document.documentElement.style.overflow='';\n    win.classList.remove('proof-paused');\n    resumeProofTrack();\n  }"""
    if old in s:
        s=s.replace(old,new,1)
    old_vis="""  document.addEventListener('visibilitychange',function(){\n    if(!document.hidden && track && !lb.classList.contains('open')){\n      track.style.animationPlayState='running';\n      requestAnimationFrame(function(){track.style.animationPlayState='';});\n    }\n  });"""
    new_vis="""  document.addEventListener('visibilitychange',function(){\n    if(!document.hidden && !lb.classList.contains('open')) resumeProofTrack();\n  });"""
    if old_vis in s:
        s=s.replace(old_vis,new_vis,1)

p.write_text(s)
