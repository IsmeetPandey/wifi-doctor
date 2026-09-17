from __future__ import annotations

import platform
import re
import socket
import statistics
import subprocess
import time

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Wi-Fi Doctor", version="0.2.0")
HTML='''<!doctype html><html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wi-Fi Doctor</title><style>body{font-family:system-ui;background:#0b0f14;color:#eef;margin:0}main{max-width:900px;margin:45px auto;padding:24px}button{padding:14px 18px;border:0;border-radius:10px;cursor:pointer}section{margin-top:18px;padding:20px;border:1px solid #293341;border-radius:14px;background:#121820}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.card{padding:16px;border:1px solid #293341;border-radius:12px}.ok{color:#8ff0c0}.warn{color:#ffd37d}.bad{color:#ff9a9a}.muted{color:#8e9aaa}@media(max-width:700px){.grid{grid-template-columns:1fr}}</style><main><small>WI-FI DOCTOR / MVP</small><h1>Find out where the connection breaks.</h1><p class=muted>Runs local gateway, DNS, internet reachability and latency checks on the machine hosting this app.</p><button id=b>Run diagnosis</button><div id=o></div></main><script>const b=document.querySelector('#b'),o=document.querySelector('#o');const e=x=>String(x??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));b.onclick=async()=>{b.disabled=true;o.innerHTML='<section>Running checks…</section>';try{const r=await fetch('/api/diagnose',{method:'POST'}),d=await r.json();if(!r.ok)throw Error(d.detail||'Diagnosis failed');o.innerHTML=`<section><div class=grid>${Object.entries(d.checks).map(([k,v])=>`<div class=card><b>${e(k)}</b><div class=${e(v.status)}>${e(v.value)}</div><small class=muted>${e(v.detail||'')}</small></div>`).join('')}</div><p>${e(d.summary)}</p></section>`}catch(x){o.innerHTML='<section>'+e(x.message)+'</section>'}finally{b.disabled=false}};</script>'''

class Empty(BaseModel):
    pass


def ping(host: str, count: int = 4) -> list[float]:
    count = max(1, min(count, 8))
    cmd = ["ping", "-n" if platform.system().lower().startswith("win") else "-c", str(count), host]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=max(3, count * 2))
    except (OSError, subprocess.TimeoutExpired):
        return []
    if p.returncode != 0:
        return []
    vals = re.findall(r"time\s*[=<]\s*([0-9]+(?:\.[0-9]+)?)", p.stdout.lower())
    return [float(v) for v in vals]


def gateway() -> str | None:
    try:
        if platform.system().lower().startswith("win"):
            out = subprocess.run(["ipconfig"], capture_output=True, text=True, timeout=3).stdout
            match = re.search(r"Default Gateway[^:]*:\s*([0-9.]+)", out, re.IGNORECASE)
            return match.group(1) if match else None
        out = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True, timeout=3).stdout
        parts = out.split()
        return parts[parts.index("via") + 1] if "via" in parts else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


@app.get('/', response_class=HTMLResponse)
async def index(): return HTML

@app.get('/health')
async def health(): return {'status':'ok'}

@app.post('/api/diagnose')
async def diagnose(_: Empty | None = None):
    gw = gateway()
    checks = {}
    if gw:
        samples = ping(gw)
        checks['Gateway']={'status':'ok' if samples else 'bad','value':f'{statistics.mean(samples):.1f} ms avg' if samples else 'Unreachable','detail':gw}
    else:
        checks['Gateway']={'status':'warn','value':'Not detected','detail':'Default gateway could not be resolved on this OS.'}
    t0=time.perf_counter()
    try:
        socket.getaddrinfo('example.com',443)
        dns_ms=(time.perf_counter()-t0)*1000
        checks['DNS']={'status':'ok' if dns_ms<150 else 'warn','value':f'{dns_ms:.1f} ms','detail':'example.com resolution'}
    except socket.gaierror:
        checks['DNS']={'status':'bad','value':'Failed','detail':'DNS lookup failed.'}
    samples=ping('1.1.1.1')
    replies=len(samples)
    checks['Internet']={'status':'ok' if replies else 'bad','value':f'{replies}/4 replies' if replies else 'No replies','detail':'ICMP reachability to a public resolver'}
    if samples:
        avg=statistics.mean(samples); jitter=statistics.pstdev(samples) if len(samples)>1 else 0
        checks['Latency']={'status':'ok' if avg<60 else 'warn','value':f'{avg:.1f} ms','detail':f'jitter {jitter:.1f} ms'}
        checks['Stability']={'status':'ok' if replies==4 else 'warn','value':f'{100*replies/4:.0f}% replies','detail':'Packet-loss proxy from 4 ICMP probes'}
    else:
        checks['Latency']={'status':'bad','value':'Unavailable','detail':'No successful probes'}; checks['Stability']={'status':'bad','value':'Unavailable','detail':'No successful probes'}
    bad=sum(v['status']=='bad' for v in checks.values()); warn=sum(v['status']=='warn' for v in checks.values())
    summary='Connection looks healthy based on the available local checks.' if not bad and not warn else f'{bad} failing check(s) and {warn} warning(s) detected. Check the detailed evidence before changing settings.'
    return {'checks':checks,'summary':summary}
