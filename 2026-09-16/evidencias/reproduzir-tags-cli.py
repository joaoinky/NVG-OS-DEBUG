"""Executa a CLI contra um socket descartável; nenhum agente/chave real."""
from pathlib import Path
import json, os, socket, subprocess, tempfile, threading
root=Path.cwd()
binary=Path(os.environ.get('NVG_AUDIT_BINARY',str(root/'rust/target/debug/nvg-nostr')))
with tempfile.TemporaryDirectory(prefix='nvg-audit-tags-') as d:
    server=socket.socket(socket.AF_UNIX)
    server.bind(d+'/nvg-nostr.sock'); server.listen(1); server.settimeout(10)
    requests=[]
    def receive():
        stream,_=server.accept()
        with stream,stream.makefile('rwb') as f:
            request=json.loads(f.readline()); requests.append(request)
            f.write(b'{"ok":true,"resultado":{"evento":"SIMULADO"}}\n'); f.flush()
    thread=threading.Thread(target=receive,daemon=True); thread.start()
    p=subprocess.run([str(binary),'agente','assinar','--kind','5','--conteudo','teste','--tag','e='+'a'*64],env=dict(os.environ,XDG_RUNTIME_DIR=d),text=True,capture_output=True,timeout=10)
    thread.join(10); server.close()
    assert p.returncode==0,(p.stdout,p.stderr)
    assert requests[0]['evento']['tags']==[]
    print('CONFIRMADO: CLI real recebeu --tag e=<id>, retornou sucesso e enviou tags=[] ao socket simulado')
