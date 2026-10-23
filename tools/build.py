"""Generator dema DK-FLIZ: wspólny nagłówek/stopka + 4 podstrony -> *.html w katalogu głównym.
Uruchom: python3 tools/build.py"""
import hashlib, json, os, random
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://impulseo-pl.github.io/dk-fliz/'
NAME = 'DK-FLIZ'
FULL = 'DK-fliz Usługi Glazurnicze i Wykończeniowe'
TEL = '730 230 019'
TEL_H = '+48730230019'
MAIL = 'dk.fliz.kontakt@gmail.com'
FB = 'https://www.facebook.com/profile.php?id=61575846427775'


def ver(path):
    with open(os.path.join(ROOT, path), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def size(name):
    with Image.open(os.path.join(ROOT, 'img', name)) as im:
        return im.size


def img(name, alt, cls='', lazy=True, mobile=True, prio=False):
    w, h = size(f'{name}.webp')
    srcset = f' srcset="img/{name}-m.webp 860w, img/{name}.webp {w}w" sizes="(max-width: 900px) 100vw, 50vw"' if mobile else ''
    load = ' fetchpriority="high"' if prio else (' loading="lazy"' if lazy else '')
    c = f' class="{cls}"' if cls else ''
    return f'<img src="img/{name}.webp"{srcset} alt="{alt}" width="{w}" height="{h}"{load} decoding="async"{c}>'


ICO_TEL = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11.4 11.4 0 0 0 3.6.58 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.46.58 3.6a1 1 0 0 1-.25 1l-2.23 2.2Z" fill="currentColor"/></svg>'
ICO_MAIL = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="m4 7 8 6 8-6" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ICO_PIN = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="9.5" r="2.5" stroke="currentColor" stroke-width="1.8"/></svg>'
ICO_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.1 23.7v-8H6.6V12h2.5v-1.6c0-4 1.9-6 5.9-6 .4 0 1 0 1.5.1l1.1.2v3.3h-1.4c-.7 0-1.3.1-1.7.3-.3.2-.5.4-.7.6-.3.4-.4 1-.4 1.8V12h3.9l-.4 2.1-.3 1.6h-3.2v8.2C19.4 23.2 24 18.2 24 12 24 5.4 18.6 0 12 0S0 5.4 0 12c0 5.6 3.9 10.4 9.1 11.7Z" fill="currentColor"/></svg>'
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 3 6.6 7.2.8-5.4 4.9 1.5 7.1L12 17.8 5.7 21.4l1.5-7.1L1.8 9.4 9 8.6Z" fill="currentColor"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12-7.5Z" fill="currentColor"/></svg>'

MARK = ('<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">'
        '<path d="M2 2H38L24 17Z" fill="#17181B"/>'
        '<path d="M38 2V38L24 17Z" fill="#A3582F"/>'
        '<path d="M38 38H2L24 17Z" fill="#8E8A84"/>'
        '<path d="M2 38V2L24 17Z" fill="#3A3B40"/></svg>')


def shards(top, bottom, flip=False):
    """Poszarpana krawędź z odłamków między sekcjami (top = tło nad, bottom = kolor sekcji pod)."""
    pts = '0,80 0,44 120,62 250,20 390,56 520,30 650,68 790,24 930,52 1070,14 1210,58 1330,30 1440,48 1440,80'
    t = ' style="transform:scaleY(-1)"' if flip else ''
    return (f'<svg class="shards" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true" style="background:{top}"><g{t} style="transform-origin:center">'
            f'<polygon points="{pts}" fill="{bottom}"/>'
            f'<polygon points="250,20 390,56 300,64" fill="#A3582F"/>'
            f'<polygon points="1070,14 1210,58 1120,54" fill="#8E8A84"/>'
            f'<polygon points="650,68 790,24 720,72" fill="#3A3B40"/></g></svg>')


NAV = [('index.html', 'Start'), ('mozaiki.html', 'Mozaiki'), ('realizacje.html', 'Realizacje'), ('kontakt.html', 'Kontakt')]


def page(fname, title, desc, body, pagehead=''):
    css, js = ver('assets/styles.css'), ver('assets/main.js')
    url = URL + ('' if fname == 'index.html' else fname)
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{cur if h == fname else ""}>{t}</a>' for h, t in NAV[1:])
    ld = {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": FULL, "url": URL,
          "telephone": TEL_H, "email": MAIL, "image": URL + 'img/og.jpg',
          "address": {"@type": "PostalAddress", "addressLocality": "Maków Podhalański", "addressRegion": "małopolskie", "addressCountry": "PL"},
          "areaServed": ["Maków Podhalański", "Sucha Beskidzka", "Wadowice", "Kraków", "małopolskie"],
          "sameAs": [FB]}
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#EEEAE3">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{URL}img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css?v={css}">
</head>
<body{' class="on-dark"' if pagehead else ''}>

<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="index.html" aria-label="{NAME} — strona główna">{MARK}<span class="brand-txt"><span class="brand-name">{NAME}</span><span class="brand-sub">Glazurnictwo · Mozaiki</span></span></a>
    <nav class="nav-links" aria-label="Główna">
      {links}
      <a href="tel:{TEL_H}" class="pill">Zadzwoń {TEL}</a>
    </nav>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>

<main>
{pagehead}{body}
</main>

<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="index.html">{MARK}<span class="brand-txt"><span class="brand-name">{NAME}</span><span class="brand-sub">Usługi glazurnicze i wykończeniowe</span></span></a>
        <p>Kompleksowe wykończenie łazienek i mozaiki z płytek na podstawie obrazów. Maków Podhalański i województwo małopolskie.</p>
      </div>
      <div class="foot-col">
        <h4>Strona</h4>
        {''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}
      </div>
      <div class="foot-col">
        <h4>Kontakt</h4>
        <a href="tel:{TEL_H}">{TEL}</a>
        <a href="mailto:{MAIL}">{MAIL}</a>
        <p>Maków Podhalański, małopolskie</p>
        <a class="soc" href="{FB}" target="_blank" rel="noopener" aria-label="Facebook {NAME}">{ICO_FB}</a>
      </div>
    </div>
    <div class="foot-bot">
      <span>© 2026 {FULL}</span>
      <span>Projekt strony: <a href="https://impulseo.pl" target="_blank" rel="noopener">Impulseo</a></span>
    </div>
  </div>
</footer>
<div class="sticky-call"><a class="sc-call" href="tel:{TEL_H}">{ICO_TEL} Zadzwoń</a><a class="sc-quote" href="kontakt.html">Bezpłatna wycena</a></div>

<script src="assets/main.js?v={js}"></script>
</body>
</html>
'''


def reel(video, poster, title, sub):
    return f'''<figure class="reel reveal">
        <div class="reel-frame"><video src="video/{video}.mp4" poster="img/poster-{video}.webp" muted loop playsinline preload="none" aria-label="{title}"></video>
        <button class="reel-play" aria-label="Odtwórz lub zatrzymaj film: {title}"><span>{PLAY}</span></button></div>
        <figcaption><b>{title}</b><span>{sub}</span></figcaption>
      </figure>'''


def final_cta():
    return f'''{shards('var(--paper)', 'var(--dark)')}
<section class="sec dark final">
  <div class="wrap reveal">
    <span class="eyebrow">Bezpłatna wycena</span>
    <h2 class="h2" style="margin-top:1.2rem">Porozmawiajmy o&nbsp;Twojej łazience</h2>
    <a href="tel:{TEL_H}" class="final-tel">{TEL}</a>
    <div class="final-actions"><a href="tel:{TEL_H}" class="pill pill-light">Zadzwoń teraz</a><a href="kontakt.html" class="more" style="color:var(--on-dark)">Napisz wiadomość <span class="arr">→</span></a></div>
    <p class="motto">„Rób tak, jak dla siebie” — motto DK-FLIZ</p>
  </div>
</section>'''


# ---------------------------------------------------------------- index
def index():
    hero = f'''<section class="hero">
  <div class="hero-art">
    <video autoplay muted loop playsinline poster="img/poster-hero.webp" aria-label="Film z realizacji łazienki z podświetleniem LED"><source src="video/hero.mp4" type="video/mp4"></video>
    <svg class="grout" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
      <polygon points="48,30 74,52 36,64" fill="rgba(255,255,255,.07)"/>
      <polygon points="74,52 100,74 100,100 84,100" fill="rgba(0,0,0,.2)"/>
      <polygon points="56,0 100,0 100,22 48,30" fill="rgba(0,0,0,.14)"/>
      <path d="M56 0 L48 30 L15 40"/>
      <path d="M48 30 L74 52 L100 22"/>
      <path d="M74 52 L36 64 L0 60"/>
      <path d="M48 30 L36 64 L58 100"/>
      <path d="M74 52 L100 74"/>
      <path d="M74 52 L84 100"/>
    </svg>
  </div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <span class="eyebrow">Maków Podhalański · Małopolska</span>
      <h1 class="h1">Łazienki <em>&amp;</em> mozaiki z&nbsp;płytek</h1>
      <p class="lead">DK-FLIZ to usługi glazurnicze i&nbsp;wykończeniowe. Specjalizujemy się w&nbsp;kompleksowym wykończeniu łazienek oraz w&nbsp;mozaikach z&nbsp;płytek wykonywanych na podstawie obrazów — fachowo, terminowo i&nbsp;dokładnie, od pierwszej płytki do ostatniego detalu.</p>
      <div class="hero-actions">
        <a href="kontakt.html" class="pill">Bezpłatna wycena</a>
        <a href="tel:{TEL_H}" class="tel">{ICO_TEL} {TEL}</a>
      </div>
      <ul class="trust"><li>Bezpłatna wycena</li><li>Kraków · Wadowice · Sucha Beskidzka</li><li>Mozaiki według obrazu</li></ul>
    </div>
  </div>
</section>
'''
    body = hero + f'''{shards('var(--paper)', 'var(--dark)')}
<section class="sec dark">
  <span class="ghost" aria-hidden="true">DK-FLIZ</span>
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Czym się zajmujemy</span>
      <h2 class="h2">Dwie specjalności</h2>
      <p class="lead">Najwięcej czasu poświęcamy łazienkom: płytkom wielkoformatowym, odpływom liniowym, wnękom z&nbsp;podświetleniem LED i&nbsp;zabudowom stelaży. Drugą specjalnością są mozaiki z&nbsp;płytek — postacie i&nbsp;motywy układane z&nbsp;ręcznie ciętych elementów na podstawie obrazu lub zdjęcia.</p>
    </div>
    <div class="duo">
      <a href="realizacje.html" class="feature reveal">{img('lazienka-granat', 'Łazienka z kabiną prysznicową, granatową szafką i lustrem LED')}<span class="feature-txt"><span class="feature-ttl">Łazienki pod klucz</span><span class="feature-sub">Kompleksowe wykończenie — od ścian po biały montaż.</span></span></a>
      <a href="mozaiki.html" class="feature reveal">{img('mozaika-kot-czarny-2', 'Mozaika z czarnych płytek przedstawiająca głowę kota')}<span class="feature-txt"><span class="feature-ttl">Mozaiki z&nbsp;płytek</span><span class="feature-sub">Obraz ułożony z ręcznie ciętych płytek.</span></span></a>
    </div>
  </div>
</section>
{shards('var(--dark)', 'var(--paper)')}
<section class="sec">
  <div class="wrap mz-split">
    <div class="mz-assemble reveal" data-cols="4" data-rows="5">{img('mozaika-kot-czarny', 'Mozaika z płytek — czarny kot na białej ścianie', mobile=False)}</div>
    <div class="mz-copy reveal">
      <span class="eyebrow">Znak rozpoznawczy</span>
      <h2 class="h2">Mozaika z&nbsp;płytek na podstawie <em>obrazu</em></h2>
      <p class="lead">Każdy projekt zaczyna się od obrazu lub zdjęcia. Motyw dzielimy na pola, a&nbsp;następnie wycinamy z&nbsp;płytek i&nbsp;numerujemy kolejne elementy. Na ścianie lub posadzce składają się one w&nbsp;jeden obraz, a&nbsp;fuga wyznacza jego kontur.</p>
      <div class="mz-facts">
        <div><b>70+</b><span>elementów w&nbsp;jednym portrecie</span></div>
        <div><b>100%</b><span>cięte i&nbsp;dopasowane ręcznie</span></div>
        <div><b>1:1</b><span>według Twojego obrazu</span></div>
      </div>
      <a href="mozaiki.html" class="pill">Zobacz mozaiki</a>
    </div>
  </div>
</section>
{shards('var(--paper)', 'var(--dark)')}
<section class="sec dark">
  <div class="wrap">
    <div class="head-row reveal">
      <h2 class="big">Realizacje</h2>
      <a href="realizacje.html" class="more" style="color:var(--on-dark)">Zobacz wszystkie <span class="arr">→</span></a>
    </div>
    <div class="trio">
      <a href="realizacje.html" class="project reveal"><span class="project-img">{img('lazienka-grafit-1', 'Łazienka w grafitowych płytkach z drewnianym blatem i podświetleniem')}</span><h3>Łazienki</h3></a>
      <a href="mozaiki.html" class="project reveal"><span class="project-img">{img('mozaika-kot-bialy', 'Mozaika z płytek: biały kot na czarnej ścianie w kuchni')}</span><h3>Mozaiki</h3></a>
      <a href="realizacje.html" class="project reveal"><span class="project-img">{img('taras-3', 'Schody wejściowe i taras wyłożone grafitowym gresem')}</span><h3>Schody i&nbsp;tarasy</h3></a>
    </div>
    <div class="head reveal" style="margin:clamp(80px,10vw,140px) 0 clamp(36px,5vw,60px)">
      <span class="eyebrow">Realizacje na filmie</span>
      <h2 class="h2">Zobacz z&nbsp;bliska</h2>
    </div>
    <div class="reels">
      {reel('przed-po', '', 'Przed i po', 'Metamorfoza łazienki w jasnym kamieniu')}
      {reel('lazienka-marmur', '', 'Łazienka w marmurze', 'Odpływ liniowy, lamele i podświetlana półka')}
      {reel('lazienka-led', '', 'Grafit i LED', 'Lustra, wnęki i światło w fudze')}
    </div>
  </div>
</section>
{shards('var(--dark)', 'var(--paper-2)')}
<section class="sec paper-2">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Usługi</span>
      <h2 class="h2">Zakres prac</h2>
      <p class="lead">Prowadzimy całe wykończenie albo wchodzimy na wybrany etap.</p>
    </div>
    <div class="cards">
      <a href="realizacje.html" class="card reveal"><span class="card-img">{img('lazienka-beton-1', 'Łazienka w szarych płytkach z okrągłym lustrem LED')}</span><span class="card-body"><span class="card-no">01</span><h3>Łazienki pod klucz</h3><p>Przygotowanie ścian, płytki ścienne i&nbsp;podłogowe, odpływy liniowe, wnęki i&nbsp;półki z&nbsp;podświetleniem oraz biały montaż.</p></span></a>
      <a href="mozaiki.html" class="card reveal"><span class="card-img">{img('mozaika-twarz', 'Ponumerowane elementy mozaiki portretowej z płytek')}</span><span class="card-body"><span class="card-no">02</span><h3>Mozaiki z&nbsp;płytek</h3><p>Mozaiki artystyczne na ścianę lub posadzkę, wykonywane według obrazu, zdjęcia albo własnego pomysłu klienta.</p></span></a>
      <a href="realizacje.html" class="card reveal"><span class="card-img">{img('schody', 'Schody wewnętrzne wyłożone płytkami imitującymi kamień')}</span><span class="card-body"><span class="card-no">03</span><h3>Schody i&nbsp;tarasy</h3><p>Okładzina schodów wewnętrznych i&nbsp;zewnętrznych oraz tarasów z&nbsp;płytek gresowych, z&nbsp;wykończeniem krawędzi i&nbsp;cokołów.</p></span></a>
      <a href="realizacje.html" class="card reveal"><span class="card-img">{img('zabudowa-luk-2', 'Pomieszczenie z łukowym przejściem z płyt gipsowo-kartonowych')}</span><span class="card-body"><span class="card-no">04</span><h3>Wykończenia wnętrz</h3><p>Zabudowy z&nbsp;płyt gipsowo-kartonowych, łuki i&nbsp;ścianki działowe oraz posadzki z&nbsp;płytek wielkoformatowych.</p></span></a>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="head-row reveal">
      <div><span class="eyebrow">Przed i po</span><h2 class="h2" style="margin-top:1rem">Przesuń i&nbsp;porównaj</h2></div>
      <p class="lead" style="max-width:44ch">Schody wejściowe i&nbsp;podest: stara okładzina zastąpiona grafitowym gresem z&nbsp;wykończonymi krawędziami.</p>
    </div>
    <div class="ba reveal">
      {img('ba-taras-przed', 'Schody wejściowe przed remontem — jasne, stare płytki', mobile=False)}
      {img('ba-taras-po', 'Schody wejściowe po remoncie — grafitowy gres', cls='ba-po', mobile=False)}
      <span class="ba-tag l">Przed</span><span class="ba-tag r">Po</span>
      <span class="ba-line"></span><span class="ba-knob"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m9 6-6 6 6 6M15 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <input type="range" min="0" max="100" value="50" aria-label="Porównanie przed i po">
    </div>
  </div>
</section>
<section class="sec" style="padding-top:0">
  <div class="wrap quote reveal">
    <svg class="quote-mark" viewBox="0 0 54 54" aria-hidden="true"><polygon points="0,6 24,0 18,30 0,30" fill="currentColor"/><polygon points="30,6 54,0 48,30 30,30" fill="currentColor" opacity=".55"/></svg>
    <blockquote>Profesjonalne podejście do klienta, fachowe doradztwo oraz terminowa realizacja zlecenia. Prace zostały wykonane starannie i&nbsp;z&nbsp;dbałością o&nbsp;detale, a&nbsp;kontakt na każdym etapie współpracy był bezproblemowy.</blockquote>
    <cite><b>Agnieszka K.</b> · opinia na Facebooku</cite>
    <div class="stars" aria-label="Ocena: polecam">{STAR * 5}</div>
  </div>
</section>
{shards('var(--paper)', 'var(--dark)')}
<section class="sec dark">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Jak pracujemy</span>
      <h2 class="h2">Krok po kroku</h2>
    </div>
    <ol class="steps">
      <li class="reveal"><span class="no">01</span><h3>Rozmowa</h3><p>Zadzwoń pod numer {TEL} i&nbsp;opisz zakres prac. Najwięcej da się ustalić w&nbsp;bezpośredniej rozmowie.</p></li>
      <li class="reveal"><span class="no">02</span><h3>Oględziny i&nbsp;wycena</h3><p>Przyjeżdżamy na miejsce, mierzymy pomieszczenie i&nbsp;omawiamy płytki, rozwiązania oraz koszt prac.</p></li>
      <li class="reveal"><span class="no">03</span><h3>Termin</h3><p>Ustalamy datę rozpoczęcia prac i&nbsp;ich harmonogram, tak aby klient wiedział, czego i&nbsp;kiedy się spodziewać.</p></li>
      <li class="reveal"><span class="no">04</span><h3>Realizacja i&nbsp;odbiór</h3><p>Pracujemy do momentu, w&nbsp;którym każdy detal jest dopracowany, a&nbsp;klient zadowolony z&nbsp;efektu.</p></li>
    </ol>
  </div>
</section>
{shards('var(--dark)', 'var(--paper)')}
<section class="sec">
  <div class="wrap mz-split" style="grid-template-columns:1fr 1fr">
    <div class="reveal">
      <span class="eyebrow">O nas</span>
      <h2 class="h2" style="margin:1.2rem 0 1.4rem">Rób tak, jak dla siebie</h2>
      <p class="lead">DK-fliz Usługi Glazurnicze i&nbsp;Wykończeniowe to firma z&nbsp;Makowa Podhalańskiego, specjalizująca się w&nbsp;kompleksowym wykończeniu łazienek oraz w&nbsp;mozaikach z&nbsp;płytek. Wykonujemy także remonty mieszkań i&nbsp;domów, schodów oraz tarasów.</p>
      <p class="lead" style="margin-top:1rem">Od października 2026 r. realizujemy usługi glazurnicze i&nbsp;wykończeniowe na terenie województwa małopolskiego.</p>
      <div class="hero-actions"><a href="tel:{TEL_H}" class="pill">Zadzwoń: {TEL}</a></div>
    </div>
    <div class="about-img reveal">{img('lazienka-drewno', 'Łazienka z wanną, płytkami drewnopodobnymi i stelażem podwieszanym')}</div>
  </div>
</section>
{final_cta()}'''
    return page('index.html', f'{NAME} — łazienki i mozaiki z płytek · Maków Podhalański',
                f'DK-FLIZ: kompleksowe wykończenie łazienek i mozaiki z płytek na podstawie obrazów. Maków Podhalański, Kraków, Wadowice, Sucha Beskidzka. Tel. {TEL}.', body)


def grid_art(seed=3, cols=5, rows=7):
    """Rysunek projektu mozaiki — ta sama siatka odłamków co w JS, tylko jako linie."""
    rnd = random.Random(seed)
    P = [[[c / cols * 300 + ((rnd.random() - .5) * 70 / cols * 3 if 0 < c < cols else 0),
           r / rows * 400 + ((rnd.random() - .5) * 70 / rows * 4 if 0 < r < rows else 0)] for c in range(cols + 1)] for r in range(rows + 1)]
    lines = []
    for r in range(rows):
        for c in range(cols):
            a, b, d, e = P[r][c], P[r][c + 1], P[r + 1][c], P[r + 1][c + 1]
            diag = (a, e) if rnd.random() > .5 else (b, d)
            lines += [(a, b), (a, d), diag]
    paths = ''.join(f'M{p[0]:.0f} {p[1]:.0f}L{q[0]:.0f} {q[1]:.0f}' for p, q in lines)
    fills = ''.join(f'<polygon points="{P[r][c][0]:.0f},{P[r][c][1]:.0f} {P[r][c+1][0]:.0f},{P[r][c+1][1]:.0f} {P[r+1][c][0]:.0f},{P[r+1][c][1]:.0f}" fill="#A3582F" opacity="{op}"/>'
                    for r, c, op in ((2, 1, .5), (3, 2, .3), (4, 2, .6), (1, 3, .25), (5, 1, .35)))
    return (f'<svg class="grid-art" viewBox="0 0 300 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{fills}'
            f'<path d="{paths}" fill="none" stroke="#ECE7DF" stroke-opacity=".55" stroke-width="1.2"/></svg>')


# ---------------------------------------------------------------- mozaiki
def mozaiki():
    head = f'''<section class="pagehead">
  <div class="wrap pagehead-grid">
    <div class="pagehead-copy reveal">
      <span class="eyebrow">Znak rozpoznawczy DK-FLIZ</span>
      <h1 class="h1">Mozaiki z&nbsp;płytek</h1>
      <p class="lead">Obraz, zdjęcie lub własny pomysł przenosimy na ścianę albo posadzkę. Motyw układamy z&nbsp;ręcznie ciętych elementów, a&nbsp;fuga wyznacza linie rysunku.</p>
      <div class="hero-actions"><a href="kontakt.html" class="pill pill-light">Zapytaj o mozaikę</a><a href="tel:{TEL_H}" class="tel">{ICO_TEL} {TEL}</a></div>
    </div>
    <div class="pagehead-art">{img('mozaika-kot-bialy-2', 'Mozaika z białych płytek — kot na czarnej ścianie', lazy=False, prio=True)}</div>
  </div>
</section>
'''
    body = f'''<section class="sec">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Od obrazu do mozaiki</span>
      <h2 class="h2">Jak powstaje mozaika</h2>
      <p class="lead">Mozaika z&nbsp;płytek to praca bliższa rzemiosłu artystycznemu niż zwykłemu płytkowaniu. Każdy element jest projektowany, cięty i&nbsp;dopasowywany osobno.</p>
    </div>
    <div class="process">
      <figure class="reveal"><div class="ph">{grid_art()}</div><figcaption><span class="no">01</span><h3>Projekt</h3><p>Na podstawie obrazu lub zdjęcia przygotowujemy rysunek, który dzieli motyw na pola o&nbsp;prostych krawędziach.</p></figcaption></figure>
      <figure class="reveal"><div class="ph">{img('mozaika-twarz', 'Ponumerowane elementy portretu z płytek rozłożone na podłodze')}</div><figcaption><span class="no">02</span><h3>Cięcie i&nbsp;numeracja</h3><p>Każde pole przenosimy na płytkę, wycinamy i&nbsp;oznaczamy numerem. Ten portret składa się z&nbsp;ponad 70 elementów.</p></figcaption></figure>
      <figure class="reveal"><div class="ph">{img('mozaika-pies-detal', 'Mozaika psa z białego marmuru w trakcie fugowania')}</div><figcaption><span class="no">03</span><h3>Montaż</h3><p>Elementy układamy na ścianie lub posadzce według numeracji, pilnując równej szerokości fugi.</p></figcaption></figure>
      <figure class="reveal"><div class="ph">{img('mozaika-kot-bialy', 'Gotowa mozaika — biały kot na czarnej ścianie w kuchni')}</div><figcaption><span class="no">04</span><h3>Efekt</h3><p>Fuga staje się konturem rysunku, a&nbsp;mozaika stałym elementem wnętrza.</p></figcaption></figure>
    </div>
  </div>
</section>
{shards('var(--paper)', 'var(--dark)')}
<section class="sec dark">
  <span class="ghost" aria-hidden="true">MOZAIKI</span>
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Realizacje</span>
      <h2 class="h2">Mozaiki DK-FLIZ</h2>
    </div>
    <div class="mz-gallery">
      <a href="img/mozaika-kot-czarny.webp" data-lb class="mz-item a reveal">{img('mozaika-kot-czarny', 'Czarny kot z płytek łupkowych na białej ścianie')}<span class="cap">Kot z łupka</span></a>
      <a href="img/mozaika-pies.webp" data-lb class="mz-item b reveal">{img('mozaika-pies', 'Mozaika psa z marmurowych płytek w czarnej ramie')}<span class="cap">Pies w marmurze — mozaika według obrazu</span></a>
      <a href="img/mozaika-twarz.webp" data-lb class="mz-item c reveal" style="aspect-ratio:4/3">{img('mozaika-twarz', 'Portret z szarych płytek w trakcie przygotowania')}<span class="cap">Portret — przygotowanie elementów</span></a>
      <a href="img/mozaika-kot-bialy.webp" data-lb class="mz-item d reveal">{img('mozaika-kot-bialy', 'Biały kot z płytek na czarnej ścianie kuchni')}<span class="cap">Biały kot w kuchni</span></a>
    </div>
  </div>
</section>
{shards('var(--dark)', 'var(--paper)')}
<section class="sec">
  <div class="wrap mz-split">
    <div class="mz-assemble reveal" data-cols="4" data-rows="6">{img('mozaika-kot-bialy-2', 'Mozaika z płytek — biały kot', mobile=False)}</div>
    <div class="mz-copy reveal">
      <span class="eyebrow">Twój motyw</span>
      <h2 class="h2">Masz obraz, który chcesz przenieść na <em>ścianę</em>?</h2>
      <p class="lead">Wyślij zdjęcie obrazu, ulubionego zwierzaka albo szkic pomysłu. Ocenimy, jak motyw będzie wyglądał w&nbsp;płytkach, i&nbsp;zaproponujemy kolory oraz rozmiar mozaiki.</p>
      <p class="lead">Mozaika sprawdza się na ścianie w&nbsp;łazience, kuchni lub salonie, a&nbsp;także na posadzce w&nbsp;holu.</p>
      <div class="hero-actions"><a href="kontakt.html" class="pill">Wyślij swój motyw</a><a href="mailto:{MAIL}" class="tel">{ICO_MAIL} {MAIL}</a></div>
    </div>
  </div>
</section>
{final_cta()}'''
    return page('mozaiki.html', f'Mozaiki z płytek na podstawie obrazów · {NAME}',
                f'Mozaiki z płytek wykonywane ręcznie na podstawie obrazu lub zdjęcia — na ścianę i posadzkę. DK-FLIZ, Maków Podhalański. Tel. {TEL}.', body, head)


# ---------------------------------------------------------------- realizacje
GALLERY = [
    ('lazienka-grafit-1', 'lazienki', 'Łazienka w grafitowym kamieniu z drewnianym blatem'),
    ('mozaika-kot-czarny', 'mozaiki', 'Mozaika — czarny kot'),
    ('lazienka-granat', 'lazienki', 'Łazienka z kabiną i lustrem LED'),
    ('taras-1', 'schody', 'Schody wejściowe z grafitowego gresu'),
    ('lazienka-tropik', 'lazienki', 'Łazienka z tapetą w liście i podświetlanym lustrem'),
    ('mozaika-pies', 'mozaiki', 'Mozaika psa z marmurowych płytek'),
    ('kabina-led-1', 'lazienki', 'Kabina prysznicowa z podświetlanymi półkami'),
    ('lazienka-beton-1', 'lazienki', 'Łazienka w szarych płytkach z okrągłym lustrem'),
    ('schody', 'schody', 'Schody wewnętrzne w płytkach'),
    ('lazienka-okno', 'lazienki', 'Łazienka z oknem i drewnianą szafką'),
    ('mozaika-kot-bialy', 'mozaiki', 'Mozaika — biały kot w kuchni'),
    ('poddasze-1', 'lazienki', 'Łazienka na poddaszu'),
    ('lazienka-grafit-3', 'lazienki', 'Łazienka w grafitowych płytkach'),
    ('taras-3', 'schody', 'Podest i schody z gresu'),
    ('lazienka-drewno', 'lazienki', 'Łazienka z wanną i płytkami drewnopodobnymi'),
    ('mozaika-twarz', 'mozaiki', 'Portret z płytek — elementy ponumerowane'),
    ('lazienka-beton-2', 'lazienki', 'Łazienka z wanną narożną'),
    ('poddasze-2', 'lazienki', 'Drewniany blat na poddaszu'),
    ('lazienka-zielen-2', 'lazienki', 'Łazienka z zieloną ścianą'),
    ('posadzka', 'wnetrza', 'Posadzka z płytek wielkoformatowych'),
    ('lazienka-grafit-4', 'lazienki', 'Łazienka z umywalką nablatową'),
    ('mozaika-kot-czarny-2', 'mozaiki', 'Mozaika — głowa kota z bliska'),
    ('taras-2', 'schody', 'Narożnik schodów z wykończeniem krawędzi'),
    ('lazienka-zielen-1', 'lazienki', 'Prysznic z zieloną ścianką'),
    ('zabudowa-luk-2', 'wnetrza', 'Łukowe przejście z płyt g-k'),
    ('lazienka-beton-3', 'lazienki', 'Łazienka z lustrem LED i wanną'),
    ('mozaika-pies-detal', 'mozaiki', 'Mozaika psa — detal'),
    ('pokoj-2', 'wnetrza', 'Pomieszczenie przygotowane pod wykończenie'),
    ('zabudowa-luk-1', 'wnetrza', 'Zabudowa z łukiem w trakcie prac'),
    ('trakcie-1', 'trakcie', 'Płytki drewnopodobne pod prysznicem — w trakcie'),
    ('trakcie-2', 'trakcie', 'Odpływ liniowy i posadzka — w trakcie'),
    ('trakcie-3', 'trakcie', 'Łazienka w trakcie płytkowania'),
    ('trakcie-4', 'trakcie', 'Przygotowanie ścian pod płytki'),
    ('mozaika-kot-bialy-2', 'mozaiki', 'Biały kot z płytek — widok z boku'),
    ('taras-4', 'schody', 'Schody wejściowe — efekt końcowy'),
]
CATS = [('all', 'Wszystkie'), ('lazienki', 'Łazienki'), ('mozaiki', 'Mozaiki'), ('schody', 'Schody i tarasy'), ('wnetrza', 'Wnętrza'), ('trakcie', 'W trakcie prac')]


def realizacje():
    head = f'''<section class="pagehead">
  <div class="wrap pagehead-grid">
    <div class="pagehead-copy reveal">
      <span class="eyebrow">Portfolio</span>
      <h1 class="h1">Realizacje</h1>
      <p class="lead">Łazienki, mozaiki, schody i&nbsp;wnętrza — zdjęcia i&nbsp;filmy z&nbsp;naszych realizacji, także z&nbsp;etapów, których po zakończeniu prac już nie widać.</p>
    </div>
    <div class="pagehead-art">{img('lazienka-tropik', 'Łazienka z tapetą w liście, granatową szafką i lustrem LED', lazy=False, prio=True)}</div>
  </div>
</section>
'''
    count = {k: sum(1 for g in GALLERY if g[1] == k) for k, _ in CATS}
    count['all'] = len(GALLERY)
    labels = dict(CATS)
    btns = ''.join(f'<button type="button" data-f="{k}" class="{"is-on" if k == "all" else ""}" aria-pressed="{"true" if k == "all" else "false"}">{t}<small>{count[k]}</small></button>' for k, t in CATS)
    tiles = '\n      '.join(
        f'<a href="img/{n}.webp" data-lb data-cat="{c}">{img(n, a)}<span>{labels[c]}</span></a>' for n, c, a in GALLERY)
    body = f'''<section class="sec">
  <div class="wrap">
    <div class="filters reveal" role="group" aria-label="Filtr realizacji">{btns}</div>
    <div class="masonry">
      {tiles}
    </div>
  </div>
</section>
{shards('var(--paper)', 'var(--dark)')}
<section class="sec dark">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Filmy</span>
      <h2 class="h2">Realizacje na filmie</h2>
    </div>
    <div class="reels">
      {reel('przed-po', '', 'Przed i po', 'Metamorfoza łazienki w jasnym kamieniu')}
      {reel('lazienka-marmur', '', 'Łazienka w marmurze', 'Odpływ liniowy, lamele i podświetlana półka')}
      {reel('lazienka-beton', '', 'Beton i drewno', 'Kilka łazienek w jednym filmie')}
    </div>
  </div>
</section>
{shards('var(--dark)', 'var(--paper)')}
<section class="sec">
  <div class="wrap">
    <div class="head-row reveal">
      <div><span class="eyebrow">Przed i po</span><h2 class="h2" style="margin-top:1rem">Schody wejściowe</h2></div>
      <p class="lead" style="max-width:44ch">Przesuń suwak, aby porównać stan przed remontem i&nbsp;po wymianie okładziny.</p>
    </div>
    <div class="ba reveal">
      {img('ba-taras-przed', 'Schody wejściowe przed remontem', mobile=False)}
      {img('ba-taras-po', 'Schody wejściowe po remoncie', cls='ba-po', mobile=False)}
      <span class="ba-tag l">Przed</span><span class="ba-tag r">Po</span>
      <span class="ba-line"></span><span class="ba-knob"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m9 6-6 6 6 6M15 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <input type="range" min="0" max="100" value="50" aria-label="Porównanie przed i po">
    </div>
  </div>
</section>
{final_cta()}'''
    return page('realizacje.html', f'Realizacje — łazienki, mozaiki, schody · {NAME}',
                f'Zdjęcia i filmy z realizacji DK-FLIZ: łazienki pod klucz, mozaiki z płytek, schody i tarasy. Maków Podhalański i Małopolska. Tel. {TEL}.', body, head)


# ---------------------------------------------------------------- kontakt
def kontakt():
    head = f'''<section class="pagehead slim">
  <div class="wrap pagehead-grid">
    <div class="pagehead-copy reveal">
      <span class="eyebrow">Kontakt</span>
      <h1 class="h1">Zadzwoń i&nbsp;porozmawiaj</h1>
      <p class="lead">Najszybciej ustalimy szczegóły w&nbsp;rozmowie telefonicznej. Możesz też opisać zlecenie w&nbsp;formularzu i&nbsp;dołączyć zdjęcia pomieszczenia lub motywu mozaiki.</p>
    </div>
  </div>
</section>
{shards('var(--dark)', 'var(--paper)')}
'''
    body = f'''<section class="sec" style="padding-top:clamp(40px,5vw,70px)">
  <div class="wrap contact-grid">
    <div class="reveal">
      <span class="eyebrow">Dane kontaktowe</span>
      <h2 class="h2" style="margin-top:1.2rem;font-size:clamp(1.9rem,1.3rem + 2vw,3rem)">DK-fliz Usługi Glazurnicze i&nbsp;Wykończeniowe</h2>
      <div class="c-items">
        <div class="c-item">{ICO_TEL}<div><small>Telefon — Patryk</small><a href="tel:{TEL_H}">{TEL}</a></div></div>
        <div class="c-item">{ICO_MAIL}<div><small>E-mail</small><a href="mailto:{MAIL}">{MAIL}</a></div></div>
        <div class="c-item">{ICO_PIN}<div><small>Siedziba</small><b>Maków Podhalański, małopolskie</b></div></div>
        <div class="c-item">{ICO_FB}<div><small>Facebook</small><a href="{FB}" target="_blank" rel="noopener">DK-fliz Usługi Glazurnicze i Wykończeniowe</a></div></div>
      </div>
      <p class="lead" style="margin-top:2rem">Obszar działania: województwo małopolskie.</p>
      <ul class="areas"><li>Maków Podhalański</li><li>Sucha Beskidzka</li><li>Wadowice</li><li>Kraków</li><li>okolice</li></ul>
    </div>
    <form class="form reveal" id="form" novalidate>
      <h2>Bezpłatna wycena</h2>
      <p class="muted">Odpowiadamy telefonicznie, zwykle tego samego dnia.</p>
      <div class="f-row">
        <div class="f-field"><label for="f-name">Imię</label><input id="f-name" name="imie" required autocomplete="given-name"></div>
        <div class="f-field"><label for="f-tel">Telefon</label><input id="f-tel" name="telefon" type="tel" required autocomplete="tel"></div>
      </div>
      <div class="f-row">
        <div class="f-field"><label for="f-city">Miejscowość</label><input id="f-city" name="miejscowosc" autocomplete="address-level2"></div>
        <div class="f-field"><label for="f-type">Rodzaj prac</label><select id="f-type" name="rodzaj"><option>Łazienka pod klucz</option><option>Mozaika z płytek</option><option>Schody lub taras</option><option>Wykończenie wnętrza</option><option>Inne</option></select></div>
      </div>
      <div class="f-field"><label for="f-msg">Opis zlecenia</label><textarea id="f-msg" name="opis" placeholder="Metraż, stan pomieszczenia, preferowany termin…"></textarea></div>
      <div class="f-field"><label for="f-files">Zdjęcia (opcjonalnie)</label><input id="f-files" name="zdjecia" type="file" accept="image/*" multiple></div>
      <label class="f-check"><input type="checkbox" name="rodo" required> Wyrażam zgodę na przetwarzanie moich danych w celu przygotowania wyceny i kontaktu w sprawie zlecenia.</label>
      <button class="pill" type="submit">Wyślij zapytanie</button>
      <p class="f-note" role="status"></p>
    </form>
  </div>
</section>
{final_cta()}'''
    return page('kontakt.html', f'Kontakt — bezpłatna wycena · {NAME}',
                f'Kontakt z DK-FLIZ: tel. {TEL}, {MAIL}. Łazienki pod klucz i mozaiki z płytek — Maków Podhalański i Małopolska.', body, head)


if __name__ == '__main__':
    with open(os.path.join(ROOT, 'img', 'favicon.svg'), 'w') as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#EEEAE3"/>'
                + MARK.split('aria-hidden="true">')[1].replace('</svg>', '').replace('/>', ' stroke="#EEEAE3" stroke-width="2.4"/>') + '</svg>')
    for fn, html in (('index.html', index()), ('mozaiki.html', mozaiki()), ('realizacje.html', realizacje()), ('kontakt.html', kontakt())):
        with open(os.path.join(ROOT, fn), 'w') as f:
            f.write(html)
        print(fn, len(html))
