(function(){
  var $=function(s,c){return (c||document).querySelector(s)};
  var $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* nawigacja */
  var nav=$('.nav');
  var onScroll=function(){nav.classList.toggle('is-scrolled',window.scrollY>24)};
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  $('.nav-toggle').addEventListener('click',function(){
    var open=nav.classList.toggle('is-open');
    this.setAttribute('aria-expanded',open);document.body.style.overflow=open?'hidden':'';
  });
  $$('.nav-links a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('is-open');document.body.style.overflow=''})});

  /* reveal */
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}});
  },{threshold:.12,rootMargin:'0px 0px -40px 0px'}):null;
  $$('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('is-in')});

  /* mozaika składana z odłamków: siatka z przesuniętymi węzłami, każdy czworokąt = 2 trójkąty */
  $$('.mz-assemble').forEach(function(box){
    var img=$('img',box);if(!img)return;
    var src=img.currentSrc||img.src,cols=+box.dataset.cols||5,rows=+box.dataset.rows||7;
    var seed=7;var rnd=function(){seed=(seed*9301+49297)%233280;return seed/233280};
    var P=[];
    for(var r=0;r<=rows;r++){P[r]=[];for(var c=0;c<=cols;c++){
      var x=c/cols*100,y=r/rows*100;
      if(c>0&&c<cols)x+=(rnd()-.5)*(70/cols);
      if(r>0&&r<rows)y+=(rnd()-.5)*(70/rows);
      P[r][c]=[x,y];
    }}
    var shrink=function(t){ /* odsunięcie od środka = fuga */
      var cx=(t[0][0]+t[1][0]+t[2][0])/3,cy=(t[0][1]+t[1][1]+t[2][1])/3;
      return t.map(function(p){return [cx+(p[0]-cx)*.982,cy+(p[1]-cy)*.982]});
    };
    var frag=document.createDocumentFragment(),i=0;
    for(var r2=0;r2<rows;r2++)for(var c2=0;c2<cols;c2++){
      var a=P[r2][c2],b=P[r2][c2+1],d=P[r2+1][c2],e=P[r2+1][c2+1];
      var tris=rnd()>.5?[[a,b,e],[a,e,d]]:[[a,b,d],[b,e,d]];
      tris.forEach(function(t){
        t=shrink(t);
        var pc=document.createElement('span');pc.className='pc';
        pc.style.backgroundImage='url("'+src+'")';
        pc.style.clipPath='polygon('+t.map(function(p){return p[0].toFixed(2)+'% '+p[1].toFixed(2)+'%'}).join(',')+')';
        if(!reduce){
          pc.style.transform='translate('+((rnd()-.5)*60).toFixed(1)+'px,'+((rnd()*-50)-20).toFixed(1)+'px) rotate('+((rnd()-.5)*24).toFixed(1)+'deg)';
          pc.style.transitionDelay=(i*16+rnd()*120).toFixed(0)+'ms';
        }
        pc.dataset.t=pc.style.transform;frag.appendChild(pc);i++;
      });
    }
    box.appendChild(frag);box.classList.add('has-js');
    var place=function(){box.classList.add('is-in');$$('.pc',box).forEach(function(p){p.style.transform='none'})};
    if(reduce||!('IntersectionObserver' in window)){place();return}
    new IntersectionObserver(function(es,o){es.forEach(function(e){if(e.isIntersecting){place();o.disconnect()}})},{threshold:.35}).observe(box);
  });

  /* filmy: odtwarzanie w kadrze, klik = pauza */
  $$('.reel').forEach(function(r){
    var v=$('video',r),btn=$('.reel-play',r);if(!v)return;
    var manual=false;
    var play=function(){var p=v.play();if(p&&p.catch)p.catch(function(){});r.classList.add('is-playing')};
    var stop=function(){v.pause();r.classList.remove('is-playing')};
    btn.addEventListener('click',function(){manual=true;v.paused?play():stop()});
    if(reduce||!('IntersectionObserver' in window))return;
    new IntersectionObserver(function(es){es.forEach(function(e){
      if(e.isIntersecting&&!manual)play();else if(!e.isIntersecting)stop();
    })},{threshold:.55}).observe(r);
  });
  var hv=$('.hero-art video');
  if(hv&&reduce){hv.removeAttribute('autoplay');hv.pause()}

  /* przed / po */
  $$('.ba').forEach(function(ba){
    var inp=$('input',ba);
    var set=function(){ba.style.setProperty('--x',inp.value+'%')};
    inp.addEventListener('input',set);set();
  });

  /* filtr realizacji */
  var grid=$('.masonry');
  $$('.filters button').forEach(function(b){
    b.addEventListener('click',function(){
      $$('.filters button').forEach(function(x){x.classList.toggle('is-on',x===b);x.setAttribute('aria-pressed',x===b)});
      var f=b.dataset.f;
      $$('a',grid).forEach(function(a){a.classList.toggle('is-hidden',f!=='all'&&a.dataset.cat!==f)});
    });
  });

  /* lightbox */
  var items=$$('[data-lb]');
  if(items.length){
    var lb=document.createElement('div');lb.className='lb';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');
    lb.innerHTML='<img alt=""><button class="lb-x" aria-label="Zamknij">✕</button><button class="lb-p" aria-label="Poprzednie">←</button><button class="lb-n" aria-label="Następne">→</button><div class="lb-count"></div>';
    document.body.appendChild(lb);
    var cur=0,vis=function(){return items.filter(function(a){return !a.classList.contains('is-hidden')})};
    var show=function(i){var v=vis();cur=(i+v.length)%v.length;var a=v[cur];$('img',lb).src=a.getAttribute('href');$('img',lb).alt=($('img',a)||{}).alt||'';$('.lb-count',lb).textContent=(cur+1)+' / '+v.length};
    items.forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();show(vis().indexOf(a));lb.classList.add('is-open');document.body.style.overflow='hidden'})});
    var close=function(){lb.classList.remove('is-open');document.body.style.overflow=''};
    $('.lb-x',lb).addEventListener('click',close);
    $('.lb-p',lb).addEventListener('click',function(){show(cur-1)});
    $('.lb-n',lb).addEventListener('click',function(){show(cur+1)});
    lb.addEventListener('click',function(e){if(e.target===lb)close()});
    document.addEventListener('keydown',function(e){if(!lb.classList.contains('is-open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)});
    var sx=null;lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
    lb.addEventListener('touchend',function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50)show(cur+(dx<0?1:-1));sx=null});
  }

  /* formularz — wersja pokazowa */
  var form=$('#form');
  if(form)form.addEventListener('submit',function(e){
    e.preventDefault();var n=$('.f-note',form);
    if(!form.checkValidity()){n.textContent='Uzupełnij imię, telefon i zaznacz zgodę.';return}
    n.textContent='To wersja pokazowa strony — formularz zostanie podłączony po akceptacji projektu. Prosimy o kontakt telefoniczny: 730 230 019.';
  });
})();
(function(){try{if(String(location.protocol).indexOf('http')!==0)return;try{if(/[?&#]team=1/.test(location.search+location.hash)){localStorage.setItem('nb_team','1');}}catch(e){}try{if(localStorage.getItem('nb_team')==='1')return;}catch(e){}if((document.referrer||'').indexOf('crm-newbeginning')>-1)return;try{if(navigator.webdriver)return;}catch(e){}try{if(/^https?:\/\/(kris20032|impulseo-pl)\.github\.io\/?$/i.test(document.referrer||''))return;}catch(e){}if(sessionStorage.getItem('_dv'))return;sessionStorage.setItem('_dv','1');var seg=(location.pathname.split('/').filter(Boolean)[0])||'';var base=location.origin+(seg?('/'+seg):'');var ua='';try{ua=(navigator.userAgent||'').slice(0,300);}catch(e){}var EP='https://zngfubfinbojfgaxdrbf.supabase.co/rest/v1/demo_views';var KEY='sb_publishable_MWwoyGlSCWnJ4awtOPF0ow_ZVS0Y8qK';function send(g){try{fetch(EP,{method:'POST',keepalive:true,headers:{'Content-Type':'application/json','apikey':KEY,'Authorization':'Bearer '+KEY,'Prefer':'return=minimal'},body:JSON.stringify({demo_url:base,page:location.pathname,referrer:(document.referrer||null),user_agent:(ua||null),ip:(g&&g.ip)||null,country:(g&&g.cc)||null,city:(g&&g.city)||null})}).catch(function(){});}catch(e){}}var done=false;function once(g){if(done)return;done=true;send(g);}try{var t=setTimeout(function(){once(null);},1500);fetch('https://ipwho.is/?fields=ip,success,country_code,city',{cache:'no-store'}).then(function(r){return r.json();}).then(function(d){clearTimeout(t);once(d&&d.success!==false?{ip:d.ip,cc:d.country_code,city:d.city}:null);}).catch(function(){clearTimeout(t);once(null);});}catch(e){once(null);}}catch(e){}})();
