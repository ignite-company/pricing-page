from pathlib import Path

p = Path('index.html')
s = p.read_text()

if 'IGNITE PROOF LIGHTBOX V1' in s:
    raise SystemExit('proof lightbox already applied')

# Make carousel proof images eager so they do not arrive blank halfway across the viewport.
start = s.index('<div class="calc-proof-window"')
end = s.index('      <div class="calc-evidence">', start)
block = s[start:end]
block = block.replace(' loading="lazy"', ' loading="eager" decoding="async"')
s = s[:start] + block + s[end:]

css = r'''

/* IGNITE PROOF LIGHTBOX V1 */
#ignite-offers-v7 .calc-proof-card{
  cursor:zoom-in;
}

#ignite-offers-v7 .calc-proof-card img{
  user-select:none;
  -webkit-user-drag:none;
}

/* Keep the proof rail moving continuously. It only pauses while an image is expanded. */
#ignite-offers-v7 .calc-proof-window:hover .calc-proof-track{
  animation-play-state:running;
}

body.ignite-proof-modal-open{
  overflow:hidden;
}

#ignite-proof-lightbox{
  position:fixed;
  inset:0;
  z-index:2147483646;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:28px;
  background:rgba(2,4,7,.88);
  backdrop-filter:blur(14px);
  -webkit-backdrop-filter:blur(14px);
  opacity:0;
  visibility:hidden;
  pointer-events:none;
  transition:opacity .18s ease,visibility .18s ease;
}

#ignite-proof-lightbox.open{
  opacity:1;
  visibility:visible;
  pointer-events:auto;
}

#ignite-proof-lightbox .ignite-proof-lightbox-inner{
  position:relative;
  max-width:min(94vw,1600px);
  max-height:92vh;
  display:flex;
  align-items:center;
  justify-content:center;
}

#ignite-proof-lightbox img{
  display:block;
  max-width:min(94vw,1600px);
  max-height:90vh;
  width:auto;
  height:auto;
  object-fit:contain;
  border-radius:16px;
  background:#090c10;
  box-shadow:0 30px 100px rgba(0,0,0,.68);
}

#ignite-proof-lightbox .ignite-proof-lightbox-close{
  position:absolute;
  top:-18px;
  right:-18px;
  width:42px;
  height:42px;
  border:1px solid rgba(255,255,255,.18);
  border-radius:999px;
  background:rgba(12,15,19,.92);
  color:#fff;
  font-size:24px;
  line-height:1;
  display:grid;
  place-items:center;
  cursor:pointer;
  box-shadow:0 10px 30px rgba(0,0,0,.4);
}

#ignite-proof-lightbox .ignite-proof-lightbox-close:hover{
  background:#171b21;
}

@media (max-width:760px){
  #ignite-proof-lightbox{
    padding:14px;
  }
  #ignite-proof-lightbox img{
    max-width:96vw;
    max-height:86vh;
    border-radius:12px;
  }
  #ignite-proof-lightbox .ignite-proof-lightbox-close{
    top:-12px;
    right:-6px;
  }
}
'''

first_style_close = s.index('</style>')
s = s[:first_style_close] + css + '\n' + s[first_style_close:]

js = r'''

<script>
/* IGNITE PROOF LIGHTBOX V1 */
(function(){
  var root = document.getElementById('ignite-offers-v7');
  if(!root) return;
  var track = root.querySelector('.calc-proof-track');
  var cards = Array.prototype.slice.call(root.querySelectorAll('.calc-proof-card'));
  var images = Array.prototype.slice.call(root.querySelectorAll('.calc-proof-card img'));
  if(!track || !images.length) return;

  // Preload every unique proof image immediately. This prevents blank cards from
  // reaching the center of the marquee before the browser decides to fetch them.
  var seen = {};
  images.forEach(function(img){
    img.loading = 'eager';
    img.decoding = 'async';
    if(!seen[img.src]){
      seen[img.src] = true;
      var preload = new Image();
      preload.decoding = 'async';
      preload.src = img.src;
    }
  });

  var lightbox = document.getElementById('ignite-proof-lightbox');
  if(!lightbox){
    lightbox = document.createElement('div');
    lightbox.id = 'ignite-proof-lightbox';
    lightbox.setAttribute('aria-hidden','true');
    lightbox.innerHTML = '<div class="ignite-proof-lightbox-inner"><button class="ignite-proof-lightbox-close" type="button" aria-label="Close image">&times;</button><img alt="Expanded client proof"></div>';
    document.body.appendChild(lightbox);
  }

  var expanded = lightbox.querySelector('img');
  var closeBtn = lightbox.querySelector('.ignite-proof-lightbox-close');

  function openProof(img){
    expanded.src = img.currentSrc || img.src;
    expanded.alt = img.alt || 'Expanded client proof';
    track.style.animationPlayState = 'paused';
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden','false');
    document.body.classList.add('ignite-proof-modal-open');
  }

  function closeProof(){
    if(!lightbox.classList.contains('open')) return;
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden','true');
    document.body.classList.remove('ignite-proof-modal-open');
    track.style.animationPlayState = 'running';
    setTimeout(function(){ expanded.removeAttribute('src'); }, 200);
  }

  cards.forEach(function(card){
    var img = card.querySelector('img');
    if(!img) return;
    card.setAttribute('role','button');
    card.setAttribute('tabindex','0');
    card.setAttribute('aria-label','Expand proof screenshot');
    card.addEventListener('click',function(){ openProof(img); });
    card.addEventListener('keydown',function(e){
      if(e.key === 'Enter' || e.key === ' '){
        e.preventDefault();
        openProof(img);
      }
    });
  });

  closeBtn.addEventListener('click',function(e){
    e.stopPropagation();
    closeProof();
  });

  lightbox.addEventListener('click',function(e){
    if(e.target === lightbox) closeProof();
  });

  lightbox.querySelector('.ignite-proof-lightbox-inner').addEventListener('click',function(e){
    if(e.target !== closeBtn) e.stopPropagation();
  });

  document.addEventListener('keydown',function(e){
    if(e.key === 'Escape') closeProof();
  });

  document.addEventListener('visibilitychange',function(){
    if(!document.hidden && !lightbox.classList.contains('open')){
      track.style.animationPlayState = 'running';
    }
  });
})();
</script>
'''

# Add the behavior near the end without disturbing existing calculators/scripts.
s += js

p.write_text(s)
print('proof carousel now preloads images and supports click-to-expand lightbox')
