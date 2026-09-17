"""Somente dados fictícios, transporte e pagador simulados; nenhum pagamento."""
from pathlib import Path
import asyncio, hashlib, json, os, runpy, subprocess, tempfile, types
ROOT = Path.cwd()
rpc = runpy.run_path(str(ROOT/'neo/bin/neo-nostr-rpc'))
event = {'id':'0'*64, 'pubkey':'a'*64, 'created_at':1, 'kind':0,
         'tags':[], 'content':json.dumps({'lud16':'impostor@example.invalid'}), 'sig':'0'*128}
encoded=json.dumps([0,event['pubkey'],event['created_at'],0,[],event['content']],separators=(',',':'),ensure_ascii=False)
assert hashlib.sha256(encoded.encode()).hexdigest() != event['id']
class Socket:
    async def __aenter__(self): return self
    async def __aexit__(self,*args): pass
    async def send(self,s):
        message=json.loads(s)
        if message[0]=='REQ': self.sub=message[1]; self.remaining=2
    async def recv(self):
        self.remaining-=1
        return json.dumps(['EVENT',self.sub,event] if self.remaining else ['EOSE',self.sub])
rpc['consultar_um'].__globals__['websockets']=types.SimpleNamespace(connect=lambda *a,**kw:Socket())
result=asyncio.run(rpc['consultar'](['ws://relay.invalid'],{'authors':['a'*64],'kinds':[0]},1))
assert result==[event]
print('CONFIRMADO RPC: evento de perfil com hash incorreto e assinatura zero é devolvido como válido ao chamador')

# Vetor público BOLT11, 2500 microBTC = 250000 sats, historicamente expirado.
# O nó é substituído; a prova verifica o despacho sem checagem do valor.
invoice='lnbc2500u1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5xysxxatsyp3k7enxv4jsxqzpu9qrsgquk0rl77nj30yxdy8j9vdx85fkpmdla2087ne0xh8nhedh8w27kyke0lp53ut353s06fv3qfegext0eh0ymjpf39tuven09sam30g4vgpfna3rh'
with tempfile.TemporaryDirectory(prefix='nvg-audit-payment-') as d:
    d=Path(d); b=d/'bin'; b.mkdir(); log=d/'calls.jsonl'
    dispatcher='''#!/usr/bin/python3
import json,os,sys
from pathlib import Path
name=Path(sys.argv[0]).name
with open(os.environ['AUDIT_LOG'],'a') as f: f.write(json.dumps([name,*sys.argv[1:]])+'\\n')
if name=='curl':
 if '.well-known/lnurlp/' in sys.argv[-1]: print(json.dumps({'callback':'https://example.invalid/cb','minSendable':1000,'maxSendable':1000000000}))
 else: print(json.dumps({'pr':os.environ['AUDIT_INVOICE']}))
elif name=='lightning-cli': print('{"status":"complete"}')
'''
    for name in ['curl','lightning-cli','systemctl']:
        f=b/name; f.write_text(dispatcher); f.chmod(0o755)
    common=d/'common.sh'; common.write_text((ROOT/'neo/bin/_neo-comum.sh').read_text()+'\nrefuse_in_vault() { :; }\n')
    bitcoin=d/'bitcoin.sh'; bitcoin.write_text((ROOT/'neo/bin/_neo-bitcoin.sh').read_text()+'\nneo_curl() { curl "$@"; }\n')
    code=(ROOT/'neo/bin/neo-zap').read_text().replace('/usr/lib/neovanguard/neo-comum.sh',str(common)).replace('/usr/lib/neovanguard/neo-bitcoin.sh',str(bitcoin))
    env=dict(os.environ,PATH=str(b)+':'+os.environ['PATH'],AUDIT_LOG=str(log),AUDIT_INVOICE=invoice)
    p=subprocess.run(['bash','-c',code,'neo-zap','alvo@example.invalid','1000'],env=env,text=True,capture_output=True,timeout=10)
    assert p.returncode==0,(p.stdout,p.stderr)
    calls=[json.loads(line) for line in log.read_text().splitlines()]
    assert ['lightning-cli','pay',invoice] in calls
    assert not any(c[0]=='lightning-cli' and c[1]!='pay' for c in calls)
    assert any('amount=1000000' in c[-1] for c in calls if c[0]=='curl')
    print('CONFIRMADO zap: solicitados 1000 sats; fatura de 250000 sats encaminhada ao pagador sem decodificar/comparar valor')
