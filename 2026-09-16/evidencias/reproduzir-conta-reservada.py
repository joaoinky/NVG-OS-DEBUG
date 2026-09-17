"""useradd --prefix somente em árvore descartável; não altera contas reais."""
from pathlib import Path
import subprocess, tempfile
with tempfile.TemporaryDirectory(prefix='nvg-audit-useradd-') as d:
    etc=Path(d)/'etc'; etc.mkdir()
    (etc/'passwd').write_text('root:x:0:0:root:/root:/bin/bash\n')
    (etc/'group').write_text('root:x:0:\n')
    (etc/'shadow').write_text('root:!:1:0:99999:7:::\n')
    p=subprocess.run(['useradd','--prefix',d,'-N','root'],text=True,capture_output=True,timeout=10)
    print('useradd --prefix <temporário> -N root: exit',p.returncode)
    print(p.stderr)
    assert p.returncode==9
    print('CONFIRMADO: usuário root aceito pelo preflight é recusado pelo useradd por já existir')
