from pathlib import Path
import os,subprocess,tempfile
root=Path.cwd()
with tempfile.TemporaryDirectory(prefix='nvg-audit-gpu-') as d:
    f=Path(d)/'lspci'
    env=dict(os.environ,PATH=d+':'+os.environ['PATH'])
    for vendor,expected in [('NVIDIA',101),('Intel',0)]:
        f.write_text('#!/bin/sh\nprintf "%s\\n" "01:00.0 VGA compatible controller: '+vendor+' Corporation"\n'); f.chmod(0o755)
        p=subprocess.run(['cargo','test','--locked','--offline','--manifest-path',str(root/'rust/Cargo.toml'),'-p','nvg-nostr','--lib','manifest::testes::aceleracao_so_com_a_gpu_certa','--','--exact'],env=env,text=True,capture_output=True,timeout=600)
        print('GPU simulada:',vendor,'exit:',p.returncode)
        print(p.stdout)
        assert p.returncode==expected,p.stderr
