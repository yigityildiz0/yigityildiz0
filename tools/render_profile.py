"""Render the GitHub profile (README.md, README.tr.md and the SVG assets).

Standard library only; no network. Run from anywhere:
    python tools/render_profile.py            # README + SVG assets
    python tools/render_profile.py --social   # also 1280x640 social preview SVGs in assets/social/
"""
from pathlib import Path
from html import escape
from xml.etree import ElementTree
import sys

ROOT = Path(__file__).resolve().parents[1]
GH = 'https://github.com/yigityildiz0/'
INK = '#17203B'
SANS = 'Trebuchet MS,Arial,sans-serif'
UI = 'Segoe UI,Arial,sans-serif'
MONO = 'Consolas,monospace'


def put(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.rstrip() + '\n', encoding='utf-8', newline='\n')


def svg(w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>')


ICONS = {
    # 48x36 line icons, stroke only.
    'gauge': '<path d="M6 30a18 18 0 1 1 36 0"/><path d="M24 30l9-11"/><circle cx="24" cy="30" r="2.5"/><path d="M10 30h4M34 30h4M24 12v4"/>',
    'band': '<rect x="2" y="4" width="44" height="12" rx="6"/><rect x="2" y="4" width="28" height="12" rx="6"/><path d="M4 26h40M4 32h26"/>',
    'office': '<rect x="3" y="20" width="42" height="5" rx="2"/><path d="M8 25v9M40 25v9"/><rect x="15" y="6" width="18" height="12" rx="2"/><path d="M24 18v2"/><circle cx="9" cy="10" r="4"/>',
    'orchestra': '<circle cx="24" cy="6" r="4"/><circle cx="7" cy="30" r="4"/><circle cx="24" cy="30" r="4"/><circle cx="41" cy="30" r="4"/><path d="M22 10L9 26M24 10v16M26 10l13 16"/>',
    'language': '<path d="M3 32L12 5l9 27M6.5 22h11"/><path d="M28 14h17M36.5 9v5M30 32c6-3 10-9 11-18M33 22c3 4 7 7 12 9"/>',
    'utility': '<rect x="2" y="2" width="44" height="32" rx="5"/><path d="M10 12l6 6-6 6M23 24h12"/>',
    'web': '<rect x="2" y="2" width="44" height="32" rx="5"/><path d="M2 11h44M8 7h1M14 7h1M10 18h12v10H10zM28 18h11M28 24h11"/>',
    'build': '<rect x="2" y="2" width="44" height="32" rx="5"/><path d="M10 12l6 6-6 6M23 24h12"/>',
    'question': '<path d="M2 18h10l5-12 9 26 7-17h12"/>',
    'connect': '<circle cx="22" cy="18" r="8"/><circle cx="3" cy="4" r="3"/><circle cx="43" cy="3" r="3"/><circle cx="43" cy="34" r="3"/><circle cx="3" cy="33" r="3"/><path d="M6 6l10 8M28 13l12-8M28 23l12 9M16 23L6 31"/>',
}


def icon(kind, x, y, color, scale=1.0, width=2.5):
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[kind]}</g>')


# repo, title, kicker EN, kicker TR, description EN, description TR, icon, background, accent, has README.tr.md
PROJECTS = [
    ('burette', 'Burette', 'WINDOWS APP · RUST', 'WINDOWS UYGULAMASI · RUST',
     'AI usage limits, measured.', 'YZ kotan ne kadar kaldı, tek bakışta.',
     'gauge', '#FFE8E1', '#A44431', True),
    ('orkestra', 'Orkestra', 'AGENT SKILL', 'AJANLAR İÇİN SKILL',
     'The right model and effort for every task.', 'Her işe doğru model, doğru efor.',
     'orchestra', '#E7EDFF', '#3157C8', True),
    ('claude-usage-band', 'Claude Usage Band', 'CLAUDE CODE MOD', 'CLAUDE CODE MODU',
     'Limits, forecast and context above the prompt.', 'Limit, tahmin ve bağlam istem kutusunda.',
     'band', '#DEFAED', '#126A51', True),
    ('claude-pixel-office', 'Claude Pixel Office', 'CLAUDE CODE MOD', 'CLAUDE CODE MODU',
     'Watch your agents work at their desks.', 'Ajanlarını masalarında çalışırken izle.',
     'office', '#F0E8FF', '#7547A3', True),
    ('turkce-usta', 'Türkçe Usta', 'AGENT SKILL', 'AJANLAR İÇİN SKILL',
     'Natural Turkish that follows TDK rules.', 'Doğal ve TDK kurallarına uygun Türkçe.',
     'language', '#FFF1CE', '#896015', False),
    ('betterdiscord-auto-repair-launcher', 'BetterDiscord Launcher', 'WINDOWS UTILITY', 'WINDOWS ARACI',
     'A clearer path from diagnosis to repair.', 'Tanıdan onarıma daha açık bir yol.',
     'utility', '#DBF3FF', '#24647D', True),
]


def text_width(s, size):
    """Rough width estimate for Segoe UI/Trebuchet at a given size (no font metrics available)."""
    narrow = set('iljtfrI.,:;·’\'!|')
    wide = set('MWmwÜÖĞŞ@')
    units = sum(0.32 if c in narrow else 0.86 if c in wide else 0.29 if c == ' ' else 0.58 for c in s)
    return units * size


def hero(lang, dark):
    tr = lang == 'tr'
    bg = '#17203B' if dark else '#EDF1FF'
    fg = '#FFFFFF' if dark else INK
    sub = '#C5CCE5' if dark else '#4C5676'
    headline = 'Merakla başlar.' if tr else 'Built from curiosity.'
    subtitle = 'Yapay zekâ araçları, araştırma ve işe yarayan yazılım.' if tr else 'AI tools, research and useful software.'
    chips = [('build', 'ÜRET' if tr else 'BUILD', '#FFD166', 819, 43, 366, 5),
             ('question', 'SORGULA' if tr else 'QUESTION', '#76DFC1', 778, 178, 390, -4),
             ('connect', 'BAĞ KUR' if tr else 'CONNECT', '#B8A1F1', 850, 310, 348, 3)]
    chip_svg = ''.join(
        f'<g transform="translate({x} {y}) rotate({rot} {w // 2} 55)"><rect width="{w}" height="109" rx="21" fill="{c}"/>'
        f'{icon(k, 24, 34, INK, 1.1)}<text x="102" y="66" font-family="{SANS}" font-size="31" font-weight="700" fill="{INK}">{label}</text></g>'
        for k, label, c, x, y, w, rot in chips)
    body = f'''<defs><pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="{fg}" stroke-opacity=".06"/></pattern></defs>
<rect width="1280" height="460" rx="28" fill="{bg}"/><rect width="1280" height="460" rx="28" fill="url(#grid)"/>
<rect x="56" y="44" width="36" height="8" rx="4" fill="#FFD166"/><rect x="100" y="44" width="36" height="8" rx="4" fill="#76DFC1"/><rect x="144" y="44" width="36" height="8" rx="4" fill="#B8A1F1"/>
<text x="56" y="153" font-family="{SANS}" font-size="106" font-weight="700" letter-spacing="-5" fill="{fg}">Yiğit Yıldız<tspan fill="#4263EB">.</tspan></text>
<text x="60" y="220" font-family="{SANS}" font-size="39" font-weight="700" fill="{fg}">{headline}</text>
<text x="60" y="267" font-family="{UI}" font-size="24" fill="{sub}">{escape(subtitle)}</text>
<path d="M60 323H686" stroke="{fg}" stroke-opacity=".15"/>
<text x="60" y="375" font-family="{MONO}" font-size="19" letter-spacing="2" fill="{sub}">{'YZ × ARAŞTIRMA × YAZILIM' if tr else 'AI × RESEARCH × SOFTWARE'}</text>
{chip_svg}'''
    return svg(1280, 460, 'Yiğit Yıldız — ' + subtitle, body)


def button(label, bg, fg):
    w = round(17 + text_width(label, 15) + 44)
    ax = w - 24
    return w, svg(w, 48, label,
                  f'<rect x="1" y="1" width="{w - 2}" height="46" rx="12" fill="{bg}"/>'
                  f'<text x="17" y="30" font-family="{UI}" font-size="15" font-weight="650" fill="{fg}">{escape(label)}</text>'
                  f'<path d="M{ax} 18h7v7M{ax + 7} 18l-10 10" stroke="{fg}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')


def card(p, lang):
    repo, title, k_en, k_tr, d_en, d_tr, kind, bg, accent, _ = p
    tr = lang == 'tr'
    kicker, desc = (k_tr, d_tr) if tr else (k_en, d_en)
    cta = 'PROJEYİ KEŞFET' if tr else 'EXPLORE PROJECT'
    assert text_width(desc, 18) < 540, (repo, lang, desc)
    assert text_width(title, 31) < 470, (repo, title)
    body = f'''<rect width="600" height="242" rx="22" fill="{bg}"/><circle cx="554" cy="27" r="88" fill="{accent}" opacity=".07"/>
<rect x="30" y="29" width="5" height="21" rx="2.5" fill="{accent}"/><text x="47" y="45" font-family="{MONO}" font-size="13" letter-spacing="1" fill="{accent}">{escape(kicker)}</text>
{icon(kind, 509, 32, accent, 1.1)}
<text x="30" y="101" font-family="{SANS}" font-size="31" font-weight="700" letter-spacing="-.6" fill="{INK}">{escape(title)}</text>
<text x="31" y="137" font-family="{UI}" font-size="18" fill="#414B65">{escape(desc)}</text>
<rect x="30" y="175" width="219" height="39" rx="11" fill="{accent}"/><text x="47" y="200" font-family="{UI}" font-size="13" font-weight="700" letter-spacing=".5" fill="#FFFFFF">{cta}</text><path d="M219 188h10v10M229 188l-11 11" stroke="#FFF" stroke-width="2" fill="none"/>
<path d="M276 195H563" stroke="{accent}" opacity=".17"/>'''
    return svg(600, 242, f'{title} — {desc}', body)


def social(p):
    """1280x640 repository social preview (English)."""
    repo, title, k_en, _, d_en, _, kind, bg, accent, _ = p
    size = 96 if text_width(title, 96) < 1000 else 78
    body = f'''<rect width="1280" height="640" fill="{bg}"/><circle cx="1180" cy="40" r="300" fill="{accent}" opacity=".07"/><circle cx="1210" cy="600" r="140" fill="{accent}" opacity=".05"/>
<rect x="80" y="86" width="9" height="36" rx="4.5" fill="{accent}"/><text x="108" y="114" font-family="{MONO}" font-size="26" letter-spacing="2" fill="{accent}">{escape(k_en)}</text>
{icon(kind, 1030, 90, accent, 3.2, 2.2)}
<text x="78" y="300" font-family="{SANS}" font-size="{size}" font-weight="700" letter-spacing="-2" fill="{INK}">{escape(title)}</text>
<text x="82" y="378" font-family="{UI}" font-size="40" fill="#414B65">{escape(d_en)}</text>
<path d="M82 470H1198" stroke="{accent}" opacity=".2"/>
<text x="82" y="540" font-family="{MONO}" font-size="28" fill="{accent}">github.com/yigityildiz0/{repo}</text>
<rect x="1046" y="506" width="152" height="48" rx="14" fill="{accent}"/><text x="1122" y="538" text-anchor="middle" font-family="{UI}" font-size="22" font-weight="700" fill="#FFFFFF">open source</text>'''
    return svg(1280, 640, f'{title} — {d_en}', body)


def link(p, lang):
    repo, *_, has_tr = p
    return GH + repo + ('/blob/main/README.tr.md' if lang == 'tr' and has_tr else '')


INSTALL = {
    'en': [
        ('Burette', 'Windows 10/11', 'Download the setup file from [Releases](https://github.com/yigityildiz0/burette/releases/latest)'),
        ('Orkestra', 'Claude Code (+ Codex, Antigravity)', 'Clone into `~/.claude/skills/orkestra`, then run `ork.py kur` ([steps](https://github.com/yigityildiz0/orkestra#install))'),
        ('Claude Usage Band', 'Claude Code', '`/plugin install kota-bandi --marketplace yigityildiz0/claude-usage-band`'),
        ('Claude Pixel Office', 'Claude Code', '`/plugin install piksel-ofis --marketplace yigityildiz0/claude-pixel-office`'),
        ('Türkçe Usta', 'Claude Code, Codex, Gemini CLI', 'Download [turkce-usta.zip](https://github.com/yigityildiz0/turkce-usta/releases/latest/download/turkce-usta.zip)'),
        ('BetterDiscord Launcher', 'Windows 10/11', 'Download from [Releases](https://github.com/yigityildiz0/betterdiscord-auto-repair-launcher/releases/latest)'),
    ],
    'tr': [
        ('Burette (Cetvel)', 'Windows 10/11', 'Kurulum dosyasını [Releases](https://github.com/yigityildiz0/burette/releases/latest) sayfasından indir'),
        ('Orkestra', 'Claude Code (+ Codex, Antigravity)', '`~/.claude/skills/orkestra` klasörüne klonla, sonra `ork.py kur` çalıştır ([adımlar](https://github.com/yigityildiz0/orkestra/blob/main/README.tr.md#kurulum))'),
        ('Claude Usage Band', 'Claude Code', '`/plugin install kota-bandi --marketplace yigityildiz0/claude-usage-band`'),
        ('Claude Pixel Office', 'Claude Code', '`/plugin install piksel-ofis --marketplace yigityildiz0/claude-pixel-office`'),
        ('Türkçe Usta', 'Claude Code, Codex, Gemini CLI', '[turkce-usta.zip](https://github.com/yigityildiz0/turkce-usta/releases/latest/download/turkce-usta.zip) dosyasını indir'),
        ('BetterDiscord Launcher', 'Windows 10/11', '[Releases](https://github.com/yigityildiz0/betterdiscord-auto-repair-launcher/releases/latest) sayfasından indir'),
    ],
}

DIAGRAM = {
    'en': '''```mermaid
flowchart LR
  B["Burette<br/>local quota service"] -->|"remaining limits"| U["Claude Usage Band"]
  B -->|"outside agents"| P["Claude Pixel Office"]
  B -->|"live quotas"| O["Orkestra"]
  O -->|"routes work to"| M["Claude · Codex · Antigravity"]
  U <-->|"one auto-compact setting"| P
  T["Türkçe Usta"] -.->|"works in any agent"| M
```''',
    'tr': '''```mermaid
flowchart LR
  B["Burette (Cetvel)<br/>yerel kota servisi"] -->|"kalan limitler"| U["Claude Usage Band"]
  B -->|"dış ajanlar"| P["Claude Pixel Office"]
  B -->|"canlı kota"| O["Orkestra"]
  O -->|"işi dağıtır"| M["Claude · Codex · Antigravity"]
  U <-->|"tek oto-sıkıştırma ayarı"| P
  T["Türkçe Usta"] -.->|"her ajanda çalışır"| M
```''',
}

TEXT = {
    'en': dict(
        tagline='### Turning ideas into things you can use.',
        intro='I build open tools for working with several AI models at once: see how much of your limits is left, send each task to the right model, watch your agents work, and get proper Turkish out of them. Everything here is free and open source.',
        projects='## Projects', projects_note='Each card opens the project and its guide.',
        also='Also here: [iamyigit-site](https://github.com/yigityildiz0/iamyigit-site), a bilingual Next.js personal-site starter (Turkish and English, light and dark themes, tests).',
        fit='## How they fit together',
        fit_note='Every project works on its own. Install Burette as well and the others get live data from it: the usage band and Orkestra read the remaining limits, and Pixel Office seats agents running in other terminals.',
        install='## Quick install', cols='| Project | Works with | Install |',
        ai='<summary><strong>Prefer to let your AI install it?</strong></summary>',
        ai_note='Paste this into Claude Code, Codex or Antigravity and replace the project name:',
        ai_prompt='Install https://github.com/yigityildiz0/<project> on my computer. Read its README and AGENTS.md first, follow the steps for my system, then run the checks it lists and tell me the result.',
        foot='Free and open source; each repository states its license. Not affiliated with Anthropic, OpenAI or Google.',
        links='[Website](https://iamyigit.com) · [All repositories](https://github.com/yigityildiz0?tab=repositories) · [Profile source](https://github.com/yigityildiz0/yigityildiz0)',
        buttons=[('projects', 'Projects', '#FFD166', INK, '#projects'),
                 ('install', 'Quick install', '#76DFC1', INK, '#quick-install'),
                 ('website', 'My website', '#B8A1F1', INK, 'https://iamyigit.com')]),
    'tr': dict(
        tagline='### Fikirleri işe yarayan şeylere dönüştürmek.',
        intro='Birden çok yapay zekâ modeliyle aynı anda çalışmak için açık araçlar yapıyorum: limitlerinden ne kaldığını gör, her işi doğru modele gönder, ajanlarını çalışırken izle, Türkçeyi düzgün yazdır. Buradaki her şey ücretsiz ve açık kaynak.',
        projects='## Projeler', projects_note='Her kart projeyi ve rehberini açar.',
        also='Ayrıca: [iamyigit-site](https://github.com/yigityildiz0/iamyigit-site/blob/main/README.tr.md), iki dilli (Türkçe ve İngilizce) Next.js kişisel site başlangıç projesi; açık/koyu tema ve testlerle.',
        fit='## Birlikte nasıl çalışır',
        fit_note='Her proje tek başına çalışır. Burette’i de kurarsan diğerleri ondan canlı veri alır: kota bandı ve Orkestra kalan limitleri okur, Pixel Office başka terminallerde çalışan ajanları da masaya oturtur.',
        install='## Kurulum', cols='| Proje | Nerede çalışır | Kurulum |',
        ai='<summary><strong>Kurulumu yapay zekâna mı bırakmak istersin?</strong></summary>',
        ai_note='Bunu Claude Code, Codex ya da Antigravity’ye yapıştır, proje adını değiştir:',
        ai_prompt='https://github.com/yigityildiz0/<proje> projesini bilgisayarıma kur. Önce README ve AGENTS.md dosyalarını oku, sistemime uygun adımları izle, sonra belgede yazan kontrolleri çalıştırıp sonucu bana söyle.',
        foot='Ücretsiz ve açık kaynak; her repo kendi lisansını belirtir. Anthropic, OpenAI ya da Google ile bağlantısı yoktur.',
        links='[Web sitem](https://iamyigit.com) · [Tüm repolar](https://github.com/yigityildiz0?tab=repositories) · [Profil kaynağı](https://github.com/yigityildiz0/yigityildiz0)',
        buttons=[('projects', 'Projeler', '#FFD166', INK, '#projeler'),
                 ('install', 'Kurulum', '#76DFC1', INK, '#kurulum'),
                 ('website', 'Web sitem', '#B8A1F1', INK, 'https://iamyigit.com')]),
}


def readme(lang):
    t = TEXT[lang]
    out = (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/studio/hero-{lang}-dark.svg">\n'
           f'  <img src="assets/studio/hero-{lang}-light.svg" width="1280" alt="Yiğit Yıldız — '
           + ('yapay zekâ araçları, araştırma ve işe yarayan yazılım' if lang == 'tr' else 'AI tools, research and useful software')
           + '">\n</picture>\n\n')
    out += '[English](README.md) · [Türkçe](README.tr.md)\n\n'
    out += t['tagline'] + '\n\n' + t['intro'] + '\n\n<p>\n'
    for key, label, bg, fg, url in t['buttons']:
        w, s = button(label, bg, fg)
        put(f'assets/studio/button-{key}-{lang}.svg', s)
        out += f'<a href="{url}"><img src="assets/studio/button-{key}-{lang}.svg" width="{w}" height="48" alt="{label}"></a>\n'
    out += '</p>\n\n' + t['projects'] + '\n\n' + t['projects_note'] + '\n\n'
    cells = []
    for p in PROJECTS:
        repo, title = p[0], p[1]
        desc = p[5] if lang == 'tr' else p[4]
        put(f'assets/studio/{repo}-{lang}.svg', card(p, lang))
        url = link(p, lang)
        cells.append(f'[![{title} — {desc}](assets/studio/{repo}-{lang}.svg)]({url})<br>**[{title}]({url})**')
    out += '| | |\n|---|---|\n' + '\n'.join(f'| {cells[i]} | {cells[i + 1]} |' for i in range(0, len(cells), 2)) + '\n\n'
    out += t['also'] + '\n\n'
    out += t['fit'] + '\n\n' + t['fit_note'] + '\n\n' + DIAGRAM[lang] + '\n\n'
    out += t['install'] + '\n\n' + t['cols'] + '\n|---|---|---|\n'
    out += '\n'.join(f'| **{n}** | {w} | {i} |' for n, w, i in INSTALL[lang]) + '\n\n'
    out += '<details>\n' + t['ai'] + '\n\n' + t['ai_note'] + '\n\n```text\n' + t['ai_prompt'] + '\n```\n\n</details>\n\n'
    out += '---\n\n' + t['foot'] + '\n\n' + t['links'] + '\n'
    put('README.tr.md' if lang == 'tr' else 'README.md', out)


for lang in ('en', 'tr'):
    for theme in ('dark', 'light'):
        put(f'assets/studio/hero-{lang}-{theme}.svg', hero(lang, theme == 'dark'))
    readme(lang)

if '--social' in sys.argv:
    for p in PROJECTS:
        put(f'assets/social/{p[0]}.svg', social(p))

# Every SVG must parse; every asset the READMEs reference must exist; nothing unreferenced stays behind.
used = set()
for name in ('README.md', 'README.tr.md'):
    text = (ROOT / name).read_text('utf-8')
    for part in text.split('assets/')[1:]:
        used.add('assets/' + part.split(')')[0].split('"')[0])
for p in (ROOT / 'assets').rglob('*.svg'):
    ElementTree.fromstring(p.read_bytes())
missing = [u for u in used if not (ROOT / u).exists()]
stale = [str(p.relative_to(ROOT)).replace('\\', '/') for p in (ROOT / 'assets' / 'studio').glob('*.svg')
         if str(p.relative_to(ROOT)).replace('\\', '/') not in used]
if missing:
    raise SystemExit(f'Missing assets: {missing}')
print(f'Profile rendered: {len(PROJECTS)} cards, {len(used)} assets in use.')
if stale:
    print('Unreferenced assets (safe to delete):', *stale, sep='\n  ')
