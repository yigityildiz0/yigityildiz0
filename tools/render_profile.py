"""Render the GitHub profile's colorful edition. Standard library; no network."""
from pathlib import Path
from html import escape
import re
from xml.etree import ElementTree
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/studio'
INK='#17203B'

def put(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf-8',newline='\n')
def svg(w,h,title,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>'
def icon(kind,x,y,color,scale=1):
    paths={
      'library':'<rect x="2" y="3" width="10" height="28" rx="2"/><rect x="16" y="3" width="10" height="28" rx="2"/><path d="M32 5l9-2 6 27-9 2z"/>',
      'health':'<path d="M2 18h10l5-12 9 26 7-17h12"/>',
      'memory':'<circle cx="22" cy="18" r="8"/><circle cx="3" cy="4" r="3"/><circle cx="43" cy="3" r="3"/><circle cx="43" cy="34" r="3"/><circle cx="3" cy="33" r="3"/><path d="M6 6l10 8M28 13l12-8M28 23l12 9M16 23L6 31"/>',
      'utility':'<rect x="2" y="2" width="44" height="32" rx="5"/><path d="M10 12l6 6-6 6M23 24h12"/>',
      'finance':'<path d="M3 2v33h43M11 24l9-10 9 5 14-14M34 5h9v9"/>',
      'web':'<rect x="2" y="2" width="44" height="32" rx="5"/><path d="M2 11h44M8 7h1M14 7h1M10 18h12v10H10zM28 18h11M28 24h11"/>'}
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{paths[kind]}</g>'

def hero(lang, dark):
    tr=lang=='tr';bg='#17203B' if dark else '#EDF1FF';fg='#FFFFFF' if dark else INK;sub='#C5CCE5' if dark else '#4C5676'
    headline='Merakla başlar.' if tr else 'Built from curiosity.'
    subtitle='AI iş akışları, araştırma ve işe yarayan yazılım.' if tr else 'AI workflows, research and useful software.'
    body=f'''<defs><pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="{fg}" stroke-opacity=".06"/></pattern></defs>
<rect width="1280" height="460" rx="28" fill="{bg}"/><rect width="1280" height="460" rx="28" fill="url(#grid)"/>
<rect x="56" y="44" width="36" height="8" rx="4" fill="#FFD166"/><rect x="100" y="44" width="36" height="8" rx="4" fill="#76DFC1"/><rect x="144" y="44" width="36" height="8" rx="4" fill="#B8A1F1"/>
<text x="56" y="153" font-family="Trebuchet MS,Arial,sans-serif" font-size="106" font-weight="700" letter-spacing="-5" fill="{fg}">Yiğit Yıldız<tspan fill="#4263EB">.</tspan></text>
<text x="60" y="220" font-family="Trebuchet MS,Arial,sans-serif" font-size="39" font-weight="700" fill="{fg}">{headline}</text>
<text x="60" y="267" font-family="Segoe UI,Arial,sans-serif" font-size="24" fill="{sub}">{subtitle}</text>
<path d="M60 323H686" stroke="{fg}" stroke-opacity=".15"/>
<text x="60" y="375" font-family="Consolas,monospace" font-size="19" letter-spacing="2" fill="{sub}">AI × RESEARCH × SOFTWARE</text>
<g transform="translate(819 43) rotate(5 190 100)"><rect width="366" height="109" rx="21" fill="#FFD166"/>{icon('utility',24,30,INK,1.1)}<text x="101" y="65" font-family="Trebuchet MS,Arial,sans-serif" font-size="31" font-weight="700" fill="{INK}">{'ÜRET' if tr else 'BUILD'}</text></g>
<g transform="translate(778 178) rotate(-4 190 55)"><rect width="390" height="109" rx="21" fill="#76DFC1"/>{icon('health',25,36,INK,1.15)}<text x="107" y="67" font-family="Trebuchet MS,Arial,sans-serif" font-size="31" font-weight="700" fill="{INK}">{'SORGULA' if tr else 'QUESTION'}</text></g>
<g transform="translate(850 310) rotate(3 170 55)"><rect width="348" height="105" rx="21" fill="#B8A1F1"/>{icon('memory',23,29,INK,1.1)}<text x="102" y="65" font-family="Trebuchet MS,Arial,sans-serif" font-size="31" font-weight="700" fill="{INK}">{'BAĞ KUR' if tr else 'CONNECT'}</text></g>'''
    return svg(1280,460,'Yiğit Yıldız — '+subtitle,body)

def button(label,bg,fg):
    return svg(140,48,label,f'<rect x="1" y="1" width="138" height="46" rx="12" fill="{bg}"/><text x="17" y="30" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="650" fill="{fg}">{escape(label)}</text><path d="M116 18h7v7M123 18l-10 10" stroke="{fg}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')

PROJECTS=[
('universal-ai-skill-library','Universal Skill Library','AI WORKFLOWS','35 workflows. One place to start.','35 iş akışı. Tek başlangıç noktası.','library','#E7EDFF','#3157C8'),
('physiotherapy-clinical-skills','Physiotherapy & Evidence','REHABILITATION','Evidence and drafts for clinician review.','Kanıt ve klinisyen kontrolündeki taslaklar.','health','#DEFAED','#126A51'),
('super-memory','Super Memory','PROJECT MEMORY','Pick up the project, not the pieces.','Projeye kaldığın yerden devam et.','memory','#F0E8FF','#7547A3'),
('betterdiscord-auto-repair-launcher','BetterDiscord Launcher','WINDOWS UTILITY','A clearer path from diagnosis to repair.','Tanıdan onarıma daha açık bir yol.','utility','#FFF1CE','#896015'),
('yigit-investment-copilot','Investment Research','FINANCE & DECISIONS','Evidence, scenarios and portfolio risk.','Kanıt, senaryolar ve portföy riski.','finance','#FFE8E1','#A44431'),
('iamyigit-site','Personal Site Starter','WEB DEVELOPMENT','A bilingual starting point for the web.','Web için iki dilli bir başlangıç.','web','#DBF3FF','#24647D')]

for lang in ('en','tr'):
    tr=lang=='tr'
    for theme in ('dark','light'):put(f'assets/studio/hero-{lang}-{theme}.svg',hero(lang,theme=='dark'))
    buttons=[('catalog','Skill kataloğu' if tr else 'Skill catalog','#4263EB','#FFFFFF','https://yigityildiz0.github.io/universal-ai-skill-library/'),('projects','Projeler' if tr else 'Projects','#FFD166',INK,'#projeler' if tr else '#projects'),('downloads','İndirmeler' if tr else 'Downloads','#76DFC1',INK,'https://github.com/yigityildiz0/universal-ai-skill-library/blob/main/DOWNLOADS.md'),('website','Web sitem' if tr else 'My website','#B8A1F1',INK,'https://iamyigit.com')]
    for key,label,bg,fg,url in buttons:put(f'assets/studio/button-{key}-{lang}.svg',button(label,bg,fg))
    for repo,title,kicker,en,trdesc,kind,bg,accent in PROJECTS:
        desc=trdesc if tr else en
        cta='PROJEYİ KEŞFET' if tr else 'EXPLORE PROJECT'
        body=f'''<rect width="600" height="242" rx="22" fill="{bg}"/><circle cx="554" cy="27" r="88" fill="{accent}" opacity=".07"/>
<rect x="30" y="29" width="5" height="21" rx="2.5" fill="{accent}"/><text x="47" y="45" font-family="Consolas,monospace" font-size="13" letter-spacing="1" fill="{accent}">{escape(kicker)}</text>
{icon(kind,509,32,accent,1.1)}
<text x="30" y="101" font-family="Trebuchet MS,Arial,sans-serif" font-size="31" font-weight="700" letter-spacing="-.6" fill="{INK}">{escape(title)}</text>
<text x="31" y="137" font-family="Segoe UI,Arial,sans-serif" font-size="18" fill="#414B65">{escape(desc)}</text>
<rect x="30" y="175" width="219" height="39" rx="11" fill="{accent}"/><text x="47" y="200" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700" letter-spacing=".5" fill="#FFFFFF">{cta}</text><path d="M219 188h10v10M229 188l-11 11" stroke="#FFF" stroke-width="2" fill="none"/>
<path d="M276 195H563" stroke="{accent}" opacity=".17"/></svg>'''
        # svg() supplies the closing root.
        put(f'assets/studio/{repo}-{lang}.svg',svg(600,242,title+' — '+desc,body.removesuffix('</svg>')))

# Keep the full directory from the previous edition, while making the first screen lighter.
for lang in ('en','tr'):
    tr=lang=='tr';path=ROOT/('README.tr.md' if tr else 'README.md');old=path.read_text('utf-8')
    match=re.search(r'<details>\s*<summary><strong>(?:All projects and collections|Tüm proje ve koleksiyonlar)</strong></summary>.*?</details>',old,re.S)
    if not match:raise RuntimeError('Existing full project directory is missing; refusing to drop it.')
    directory=match.group(0)
    intro='Merak ettiğim şeyleri araştırıyor, öğrendiklerimi işe yarayan araçlara dönüştürüyorum. Burada AI iş akışları, kaynak temelli araştırma ve pratik yazılım var.' if tr else 'I explore questions, connect ideas and turn what I learn into useful tools. This is where my AI workflows, source-led research and practical software live.'
    out=f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/studio/hero-{lang}-dark.svg">\n  <img src="assets/studio/hero-{lang}-light.svg" width="1280" alt="Yiğit Yıldız — AI, research and useful software">\n</picture>\n\n'
    out+='[English](README.md) · [Türkçe](README.tr.md)\n\n'
    out+='### '+('Fikirleri işe yarayan şeylere dönüştürmek.' if tr else 'Turning ideas into things you can use.')+'\n\n'+intro+'\n\n'
    out+='<p>\n'
    for key,label,bg,fg,url in buttons if lang=='tr' else [('catalog','Skill catalog','#4263EB','#FFFFFF','https://yigityildiz0.github.io/universal-ai-skill-library/'),('projects','Projects','#FFD166',INK,'#projects'),('downloads','Downloads','#76DFC1',INK,'https://github.com/yigityildiz0/universal-ai-skill-library/blob/main/DOWNLOADS.md'),('website','My website','#B8A1F1',INK,'https://iamyigit.com')]:
        out+=f'<a href="{url}"><img src="assets/studio/button-{key}-{lang}.svg" width="140" height="48" alt="{label}"></a>\n'
    out+='</p>\n\n'
    out+=('**Bir iş akışı mı arıyorsun?** Katalogda görevine göre ara; nasıl çalıştığını oku ve yalnız ihtiyacın olan skill’i seç.\n\n' if tr else '**Looking for a workflow?** Search by the job you want to do, see how it works, and pick only the skill you need.\n\n')
    out+='## '+('Projeler' if tr else 'Projects')+'\n\n'
    out+=('Her renk, farklı bir çalışma alanı. Kartlar doğrudan proje rehberine gider.\n\n' if tr else 'Different colors, different kinds of work. Each card opens the project and its guide.\n\n')
    cards=[]
    for repo,title,kicker,en,trdesc,kind,bg,accent in PROJECTS:
        url='https://github.com/yigityildiz0/'+repo+('/blob/main/README.tr.md' if tr else '')
        cards.append(f'[![{title} — {trdesc if tr else en}](assets/studio/{repo}-{lang}.svg)]({url})<br>**[{title}]({url})**')
    out+='| | |\n|---|---|\n'+'\n'.join(f'| {cards[i]} | {cards[i+1]} |' for i in range(0,len(cards),2))+'\n\n'
    out+='<details>\n<summary><strong>'+('🧭 Bana bir başlangıç noktası öner' if tr else '🧭 Help me choose a starting point')+'</strong></summary>\n\n'
    out+=('| İstediğin iş | Buradan başla |\n|---|---|\n| Kod, yazı, analiz veya araştırma | [Skill kataloğu](https://yigityildiz0.github.io/universal-ai-skill-library/) |\n| Rehabilitasyon kanıtı ve öğrenme | [Fizyoterapi koleksiyonu](https://github.com/yigityildiz0/physiotherapy-clinical-skills) |\n| Ajanlar arasında proje devri | [Super Memory](https://github.com/yigityildiz0/super-memory) |\n\n' if tr else '| Your next task | Start here |\n|---|---|\n| Code, writing, analysis or research | [Skill catalog](https://yigityildiz0.github.io/universal-ai-skill-library/) |\n| Rehabilitation evidence and learning | [Physiotherapy collection](https://github.com/yigityildiz0/physiotherapy-clinical-skills) |\n| Hand a project to another agent | [Super Memory](https://github.com/yigityildiz0/super-memory) |\n\n')
    out+='</details>\n\n'+directory+'\n\n'
    out+='<details>\n<summary><strong>'+('🛠️ Nasıl çalışıyorum ve kütüphane nasıl güncelleniyor?' if tr else '🛠️ How I work and how the library stays current')+'</strong></summary>\n\n'
    out+=('**Kaynak önce, açık sınırlar, yeniden kullanılabilir parçalar.** Kütüphane; 34 güncel kişisel master kökü ve Super Memory ile 35 giriş noktası içerir. Her skill için ayrı İngilizce/Türkçe rehber var; alan koleksiyonları aynı kaynağın seçilmiş görünümleridir. Eski topluluk kaynakları güncel/testli kapsamdan ayrı tutulur.\n\nMevcut host araçlarını, açık kaynakları ve yerel işlemi kullanırım; ek ücretli servis otomatik alternatif değildir. Paket üretimi, test ve gerçek hesapta aktivasyon farklı aşamalardır.\n\n' if tr else '**Source first, clear boundaries, reusable parts.** The library contains 35 entry points: 34 current personal-master roots plus Super Memory. Each has separate English/Turkish guides; domain collections are selected views of the same source. Historical community material is separate from the maintained/tested scope.\n\nI use existing host tools, open sources and local computation—not an automatic extra paid-service fallback. Packaging, testing and actual account activation are separate stages.\n\n')
    out+='[Architecture & maintenance](https://github.com/yigityildiz0/universal-ai-skill-library/blob/main/MAINTAINING.md) · [Downloads](https://github.com/yigityildiz0/universal-ai-skill-library/blob/main/DOWNLOADS.md)\n\n</details>\n\n---\n\n'
    out+=('Klinik ve yatırım çıktıları profesyonel değerlendirmenin yerine geçmez. Skill dosyası hesap yetkisi, API kredisi veya model sağlamaz.\n\n' if tr else 'Clinical and investment outputs do not replace professional judgment. A skill file does not provide account access, API credit or a model.\n\n')
    out+='[Website](https://iamyigit.com) · [All repositories](https://github.com/yigityildiz0?tab=repositories) · [Profile source](https://github.com/yigityildiz0/yigityildiz0)\n'
    put(path.relative_to(ROOT),out)
for p in OUT.glob('*.svg'):ElementTree.fromstring(p.read_bytes())
print('Profile refreshed: four real navigation buttons, six color-coded project cards, English/Turkish and theme-aware hero.')
