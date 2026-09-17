"""Teste existente, com binário fora de /tmp para não ser ocultado por PrivateTmp."""
from pathlib import Path
import json, runpy, shutil, subprocess, tempfile, types
root=Path.cwd()
source=runpy.run_path(str(root/'scripts/test-agent-service.py'))
with tempfile.TemporaryDirectory(prefix='.audit-agent-',dir=root) as d:
    def run(args,**kwargs):
        result=subprocess.run(args,**kwargs)
        if args[:2]==['cargo','test']:
            lines=[]
            for line in result.stdout.splitlines():
                item=json.loads(line)
                if item.get('executable'):
                    target=Path(d)/Path(item['executable']).name
                    shutil.copy2(item['executable'],target)
                    item['executable']=str(target)
                lines.append(json.dumps(item))
            result.stdout='\n'.join(lines)+'\n'
        return result
    source['main'].__globals__['subprocess']=types.SimpleNamespace(run=run)
    source['main']()
