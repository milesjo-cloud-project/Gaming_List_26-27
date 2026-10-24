import json, html
from pathlib import Path

root = Path(__file__).resolve().parent
data = json.loads((root / 'gaming-catalog.json').read_text(encoding='utf-8'))
releases, demos = data['releases'], data['demos']
releases.sort(key=lambda r: (r['date'], r['title'].casefold()))
demos.sort(key=lambda r: (r['title'].casefold(), r['event']))
sources = list(dict.fromkeys(s for r in releases + demos for s in r['source'].split(' | ')))
ids = {s: i+1 for i,s in enumerate(sources)}
def cite(r):
    return ', '.join(f'[S{ids[s]}](#s{ids[s]})' for s in r['source'].split(' | '))
def clean(s):
    return str(s).replace('|','/').replace('\n',' ')
lines = ['# Gaming catalog · 2026–2027', '', '**Snapshot: October 24, 2026 · PC and major consoles**', '',
         f"{len(releases)} release records and {len(demos)} demo records. Counts are records, not unique games: ports and demos can overlap.", '',
         data['metadata']['coverage'], '',
         '## How to read this list', '',
         '- Past dates are calendar records unless a publisher launch announcement is cited.',
         '- A year, half-year, quarter, or month is a release window, not an exact day.',
         '- Platforms are those listed by the source. Unless explicitly verified, the date may apply to only some of those platforms.',
         '- Not checked means demo availability is unknown. It does not mean no demo exists.',
         '- Xbox Series means Xbox Series X/S. PC includes Windows; Mac and Linux are named when present in the source.',
         '- Historical demo records do not establish when a demo first launched or whether it remains downloadable.', '',
         '## Release catalog', '', '| Game | Date / window | Listed platforms | Type | Demo evidence | Source |', '|---|---|---|---|---|---|']
for r in releases:
    lines.append('| ' + ' | '.join(clean(r[k]) for k in ['title','date','platforms','type','demo']) + ' | ' + cite(r) + ' |')
lines += ['', '## Demo catalog', '', '| Game | Demo period / announcement | Demo platform | Availability evidence | Source |', '|---|---|---|---|---|']
for r in demos:
    lines.append('| '+' | '.join(clean(r[k]) for k in ['title','event','platforms','status'])+' | '+cite(r)+' |')
lines += ['', '## Entry notes', '']
for r in releases+demos:
    if r.get('note'):
        lines.append(f"- **{r['title']}** ({r.get('date',r.get('event'))}): {r['note']}")
lines += ['', '## Sources and larger catalogs', '',
          'These linked catalogs contain additional entries beyond this research snapshot. None should be assumed to be exhaustive or error-free.', '']
for s,i in ids.items():
    lines.append(f'<a id="s{i}"></a> **S{i}** — [{s}]({s})\n')
lines += ['- [Steam Next Fest](https://store.steampowered.com/sale/nextfest)',
          '- [Steam demo catalog](https://store.steampowered.com/demos/)',
          '- [2026 release index](https://en.wikipedia.org/wiki/List_of_video_games_released_in_2026)',
          '- [2027 release index](https://en.wikipedia.org/wiki/List_of_video_games_released_in_2027)']
(root/'Gaming List 2026-2027.md').write_text('\n'.join(lines),encoding='utf-8')

payload=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gaming catalog · 2026–2027</title>
<style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#10151d;color:#e7edf5}*{box-sizing:border-box}body{margin:0}header,main{max-width:1500px;margin:auto;padding:30px}header{padding-bottom:12px}.eyebrow{color:#81e0bf;letter-spacing:.14em;font-size:12px;font-weight:700}h1{font-size:clamp(30px,5vw,54px);margin:12px 0}p{line-height:1.6;color:#b8c4d5;max-width:1050px}a{color:#81c8ff}button,input,select{font:inherit;background:#1c2737;color:#e7edf5;border:1px solid #425269;border-radius:8px;padding:10px}button{cursor:pointer}button[aria-pressed=true]{background:#81e0bf;color:#10251f;border-color:#81e0bf}nav,.filters{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}label{display:flex;flex-direction:column;gap:6px;font-size:13px}input{min-width:290px}.stats{font-weight:650;color:#81e0bf}.tablewrap{overflow:auto;border:1px solid #354154;border-radius:12px;max-height:70vh}table{border-collapse:collapse;width:100%;font-size:14px}th{text-align:left;position:sticky;top:0;background:#233147;white-space:nowrap}th,td{padding:14px;vertical-align:top;border-bottom:1px solid #2a3648}tbody tr:nth-child(even){background:#151e2b}td:first-child{min-width:220px;font-weight:650}td{min-width:110px}small{display:block;color:#a9b6c9;font-weight:400;line-height:1.5;margin-top:7px}.note{padding:18px;background:#192434;border-left:3px solid #81e0bf;border-radius:5px}details{margin:18px 0}summary{cursor:pointer;color:#81e0bf}footer{padding:20px 0;font-size:13px;color:#a9b6c9}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #f6c875;outline-offset:3px}@media(max-width:600px){header,main{padding:18px}input{min-width:0;width:100%}.filters label{width:100%}}
</style><header><div class="eyebrow">PC · PLAYSTATION · XBOX · NINTENDO</div><h1>Your gaming catalog<br>2026 → 2027</h1><p>Release dates, announced windows, and documented demos. Research snapshot: <strong>October 24, 2026.</strong></p><div class="stats" id="total"></div><details><summary>Coverage and confidence</summary><p class="note" id="coverage"></p><p>Past calendar dates do not independently prove a game shipped. Listed platforms may include later ports. “Not checked” means unknown, not unavailable. Demo downloads have not been tested. Counts include separate platform releases and demo records for the same game.</p></details></header>
<main><nav aria-label="Catalog"><button id="games" aria-pressed="true">Game releases</button><button id="demos" aria-pressed="false">Demos</button></nav>
<div class="filters"><label>Search<input id="q" placeholder="Game, platform, or event…" type="search"></label><label>Period<select id="period"><option value="">All dates</option><option value="past">2026 past release dates</option><option value="upcoming">2026 upcoming / unresolved</option><option value="2027">2027 announcements</option></select></label><label>Platform<select id="platform"><option value="">All platforms</option><option>PC</option><option>PS5</option><option>PS4</option><option>Xbox</option><option>Switch 2</option><option>Switch</option><option>Mac</option><option>Linux</option></select></label><label>Demo evidence<select id="evidence"><option value="">Any</option><option value="yes">Documented</option><option value="unknown">Not checked</option></select></label></div>
<p id="count" role="status" aria-live="polite"></p><div class="tablewrap"><table><thead id="head"></thead><tbody id="body"></tbody></table></div><footer>Sources are linked on every row. <a href="Gaming%20List%202026-2027.md">Readable Markdown list</a> · <a href="gaming-catalog.json" download>Download structured data</a><br>Broader discovery: <a href="https://store.steampowered.com/sale/nextfest">Steam Next Fest</a> · <a href="https://store.steampowered.com/demos/">Steam demos</a> · <a href="https://en.wikipedia.org/wiki/List_of_video_games_released_in_2026">2026 release index</a> · <a href="https://en.wikipedia.org/wiki/List_of_video_games_released_in_2027">2027 release index</a></footer></main>
<script id="data" type="application/json">PAYLOAD</script><script>
const data=JSON.parse(document.getElementById('data').textContent);let mode='games';const $=id=>document.getElementById(id);const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
$('total').textContent=data.releases.length+' release records · '+data.demos.length+' demo records';$('coverage').textContent=data.metadata.coverage;
function render(){const q=$('q').value.toLowerCase(),p=$('platform').value,period=$('period').value,e=$('evidence').value;let list=mode==='games'?data.releases:data.demos;list=list.filter(r=>{if(q&&!JSON.stringify(r).toLowerCase().includes(q))return false;if(p&&!r.platforms.includes(p))return false;if(mode==='games'){if(period==='past'&&!r.status.startsWith('2026 past'))return false;if(period==='upcoming'&&!(r.status==='2026 upcoming'||r.status==='2026 date unresolved'))return false;if(period==='2027'&&!r.date.startsWith('2027'))return false;if(e==='yes'&&r.demo==='Not checked')return false;if(e==='unknown'&&r.demo!=='Not checked')return false;}return true});list=[...list].sort((a,b)=>mode==='games'?(a.date.localeCompare(b.date)||a.title.localeCompare(b.title)):a.title.localeCompare(b.title));const headers=mode==='games'?['Game','Date / window','Listed platforms','Release type','Demo evidence','Confidence / source']:['Game','Demo period','Demo platform','Availability evidence','Source'];$('head').innerHTML='<tr>'+headers.map(x=>'<th scope="col">'+x+'</th>').join('')+'</tr>';$('body').innerHTML=list.map(r=>{const links=r.source.split(' | ').map((s,i)=>'<a href="'+esc(s)+'" target="_blank" rel="noopener noreferrer">Source'+(i?' '+(i+1):'')+'</a>').join(' · ');const cells=mode==='games'?[esc(r.title)+(r.note?'<small>'+esc(r.note)+'</small>':''),esc(r.date)+'<small>'+esc(r.status)+'</small>',esc(r.platforms),esc(r.type),esc(r.demo),esc(r.confidence)+'<small>'+links+'</small>']:[esc(r.title)+(r.note?'<small>'+esc(r.note)+'</small>':''),esc(r.event),esc(r.platforms),esc(r.status),links];return '<tr>'+cells.map(x=>'<td>'+x+'</td>').join('')+'</tr>'}).join('');$('count').textContent=list.length+' matching '+(mode==='games'?'release records':'demo records');}
for(const id of ['q','period','platform','evidence'])$(id).addEventListener('input',render);for(const id of ['games','demos'])$(id).addEventListener('click',()=>{mode=id;$('games').setAttribute('aria-pressed',id==='games');$('demos').setAttribute('aria-pressed',id==='demos');$('period').disabled=id==='demos';$('evidence').disabled=id==='demos';render()});render();
</script></html>'''.replace('PAYLOAD',payload)
(root/'Gaming List 2026-2027.html').write_text(page,encoding='utf-8')
assert len({(r['title'].casefold(),r['date'],r['platforms']) for r in releases})==len(releases)
assert all(r['title'] and r['source'].startswith('https://') for r in releases+demos)
assert all(r['date'].startswith(('2026','2027')) for r in releases)
print(json.dumps({'releases':len(releases),'demos':len(demos),'unique_sources':len(sources),'files':['Gaming List 2026-2027.html','Gaming List 2026-2027.md','gaming-catalog.json']},indent=2))
