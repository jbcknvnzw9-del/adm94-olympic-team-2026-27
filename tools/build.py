import csv,json,re,datetime
import os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'src')+'/'
DATA=os.path.join(ROOT,'data')+'/'
def rows(f): return list(csv.DictReader(open(DATA+f,encoding='utf-8')))
data={k:rows(k+'.csv') for k in ['roster','partite','tabellini','risultati_girone','tabellini_avversari']}
page=open(D+'dashboard.html',encoding='utf-8').read()
# inline support scripts
for f in ['logo.js','foto1.js','foto2.js']:
  page=page.replace(f'<script src="{f}"></script>','<script>'+open(D+f).read()+'</script>')
upd=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime('%d/%m/%Y %H:%M')
shim='''<script>
(function(){const RAW=%s;const calcs={},subs=[];
function get(id){if(RAW[id])return RAW[id];const c=calcs[id];if(!c)return[];if(!c.cache)c.cache=c.fn(...c.inputs.map(get));return c.cache;}
window.dash={data:id=>({status:'ok',data:get(id),meta:[],refreshing:false}),
 calc:(id,o)=>{calcs[id]=o;},onData:fn=>{subs.push(fn);fn();},setLink:n=>{try{history.replaceState(null,'','#'+n);}catch(e){}},
 colors:['#1f5fd9','#8fa3c7','#0e9f6e','#d97706','#7c3aed','#db2777','#0891b2','#65a30d'],
 params:()=>({}),setParams:()=>{},resetParams:()=>{},refresh:()=>{}};
let t;addEventListener('resize',()=>{clearTimeout(t);t=setTimeout(()=>subs.forEach(f=>f()),150);});})();
</script>'''%json.dumps(data,ensure_ascii=False)
css='''<style>
:root{--font-anthropic-sans:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--font-anthropic-serif:"Oswald","Inter",system-ui,sans-serif;
--color-fg:#0f172a;--color-fg-muted:#64748b;--color-bg:#f4f6fb;--color-panel:#ffffff;--color-border-line:#e2e8f0;--color-ok:#0e8a5f;--color-warn:#b45309;--color-bad:#dc2626;
--cds-chart-grid:#eef1f6;--cds-chart-axis:#cbd5e1;--cds-chart-muted:#b6c2d6;--cds-surface-popover:#fff;--cds-border:#e2e8f0;--cds-shadow-popover:0 6px 20px rgba(15,23,42,.14);--cds-text-secondary:#64748b;
--cds-font-size-caption:12px;--cds-font-size-body:14px;--cds-font-size-heading:16px;--cds-font-size-title:28px;--cds-font-weight-medium:600;
--cds-gap-xs:4px;--cds-gap-sm:8px;--cds-gap-md:14px;--cds-gap-lg:20px;--cds-gap-xl:28px;--cds-pad-xs:4px;--cds-pad-sm:8px;--cds-pad-md:12px;--cds-pad-lg:16px;--cds-pad-xl:24px;--cds-radius:10px;--cds-dur-slow:.3s}
@media (prefers-color-scheme:dark){:root{--color-fg:#e8edf7;--color-fg-muted:#93a1ba;--color-bg:#0a1020;--color-panel:#121a2e;--color-border-line:#223050;--color-ok:#34d399;--color-bad:#f87171;
--cds-chart-grid:#1c2742;--cds-chart-axis:#33446b;--cds-chart-muted:#4a5a7d;--cds-surface-popover:#172140;--cds-border:#2b3a62;--cds-text-secondary:#93a1ba}}
html,body{margin:0;background:var(--color-bg);color:var(--color-fg);font-family:var(--font-anthropic-sans);-webkit-text-size-adjust:100%}
#dash-root{max-width:1100px;margin:0 auto;padding:16px}
.dash-skeleton{min-height:1em}
.site-foot{max-width:1100px;margin:0 auto;padding:0 16px 24px;font-size:12px;color:var(--color-fg-muted)}
</style>'''
html=f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow,noimageindex"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ADM 94 Olympic Team · Statistiche DR4</title>
<meta name="description" content="Risultati, statistiche e classifica dell'ADM 94 Olympic Team Milano - DR4 Lombardia 2026/27">
<link rel="icon" href="{json.loads(re.search(r'window.ADM_LOGO=(".*?");',open(D+'logo.js').read()).group(1))}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Oswald:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
{css}</head><body><div id="dash-root">{shim}{page}</div>
<div class="site-foot">Aggiornato il {upd} · Fonte: referti ufficiali e <a href="https://fip.it/risultati/?group=campionati-regionali&amp;regione_codice=LO&amp;comitato_codice=RLO&amp;sesso=M&amp;codice_campionato=2DM&amp;codice_fase=1&amp;codice_girone=85815" style="color:inherit">fip.it</a></div>
</body></html>'''
open(os.path.join(ROOT,'index.html'),'w',encoding='utf-8').write(html)
print(len(html))
