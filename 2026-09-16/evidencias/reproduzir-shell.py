"""Provas inofensivas: scripts reais em cópias temporárias e comandos simulados.
Passar significa reproduzir o defeito, não aprovar o produto.
"""
from pathlib import Path
import json, os, re, subprocess, tempfile

ROOT = Path.cwd()

def function(path, name):
    return re.search(r'^' + re.escape(name) + r'\(\) \{.*?^\}',
                     (ROOT/path).read_text(), re.M|re.S)[0]

with tempfile.TemporaryDirectory(prefix='nvg-shell-audit-') as tmp:
    base = Path(tmp)
    common = base/'common.sh'
    common.write_text((ROOT/'neo/bin/_neo-comum.sh').read_text() + '\nneed_root() { :; }\n')
    fake = base/'bin'; fake.mkdir()
    log = base/'calls.jsonl'
    dispatcher = r'''#!/usr/bin/python3
from pathlib import Path
import os,sys,json
name=Path(sys.argv[0]).name; args=sys.argv[1:]
with open(os.environ['AUDIT_LOG'],'a') as f: f.write(json.dumps([name,*args])+'\n')
if name=='bootctl': print(os.environ['AUDIT_ESP'])
elif name=='systemctl': sys.exit(0)
elif name=='nvg-nostr':
 if args[:2]==['chave','hex']: print('a'*64)
 else: print('{"id":"assinatura-simulada","kind":5,"tags":[]}')
elif name=='neo-nostr-rpc':
 if args[0]=='consultar':
  # O relay local tem nota antiga que falta externamente e nota nova.
  # A consulta sem --relay usa LOCAL + externos, como o código de produção.
  if '--relay' not in args: print(json.dumps({'id':'nova-local','created_at':200}))
  else:
   query=json.loads(args[args.index('--filtro')+1]); since=query.get('since',0)
   for ev in [{'id':'antiga-offline','created_at':100},{'id':'nova-local','created_at':200}]:
    if ev['created_at']>=since: print(json.dumps(ev))
elif name=='sbctl':
 if args==['status']: print('Setup Mode: Enabled')
 elif args[:1]==['sign']: sys.exit(1)
elif name=='sudo': print('SUDO_ARGV='+json.dumps(args))
'''
    for name in ['bootctl','systemctl','nvg-nostr','neo-nostr-rpc','sbctl','sudo']:
        f=fake/name; f.write_text(dispatcher); f.chmod(0o755)
    env=dict(os.environ,PATH=f'{fake}:'+os.environ['PATH'],AUDIT_LOG=str(log),NEO_ETC=str(base/'etc'))
    (base/'etc').mkdir()
    (base/'etc/identidade.conf').write_text('npub=IDENTIDADE-SINTETICA\n')

    def run_code(code, *args, data=''):
        log.write_text('')
        p=subprocess.run(['bash','-c',code,'auditoria',*args],input=data,
                         text=True,capture_output=True,env=env,timeout=15)
        calls=[json.loads(l) for l in log.read_text().splitlines()]
        return p,calls

    def script(name):
        text=(ROOT/name).read_text().replace('/usr/lib/neovanguard/neo-comum.sh',str(common))
        text=text.replace('source /usr/lib/neovanguard/neo-bitcoin.sh', ': # biblioteca sem uso neste cenário')
        return text

    pergunta=function('neo/wizard/neo-first-boot','pergunta')
    p,_=run_code(f'source "{common}"\n'+pergunta+'\nPERFIL="$(pergunta "Pergunta de teste" hot "hot:Hot:online" "cold:Cold:offline")"\n[[ "$PERFIL" == cold ]]\nprintf "igual_a_cold=%s\\nvalor=%s\\n" "$?" "$PERFIL"',data='2\n')
    assert 'igual_a_cold=1' in p.stdout and p.stdout.rstrip().endswith('cold')
    print('CONFIRMADO wizard: seleção cold vem junto com menu e não corresponde ao case cold')

    (base/'etc/profile.conf').write_text('profile=cold\nno=nenhum\nrede=airgap\n')
    p,_=run_code(f'source "{common}"\nprofile')
    assert p.stdout.strip()=='hot'
    print('CONFIRMADO profile: profile.conf com profile=cold é lido como hot pela biblioteca')

    esp=base/'esp'; entries=esp/'loader/entries'; entries.mkdir(parents=True)
    env['AUDIT_ESP']=str(esp)
    for label,options in [('btrfs','root=UUID=TESTE rw rootflags=subvol=@'),
                          ('luks','cryptdevice=UUID=TESTE:nvgroot root=/dev/mapper/nvgroot rootflags=subvol=@')]:
        (entries/'neovanguard.conf').write_text('title Teste\nlinux /vmlinuz-linux-zen\ninitrd /initramfs-linux-zen.img\noptions '+options+'\n')
        p,_=run_code(script('neo/bin/neo-install-vault-boot'))
        assert p.returncode==0,p.stderr
        result=(entries/'neovanguard-vault.conf').read_text()
        assert 'rootflags=' not in result and 'cryptdevice=' not in result
        print(f'CONFIRMADO vault {label}: '+next(l for l in result.splitlines() if l.startswith('options')))

    p,calls=run_code(script('neo/bin/neo-clean-dms'),'30',data='APAGAR\n')
    assert p.returncode==0 and 'enviados ao relay local' in p.stdout
    assert any(c[:3]==['nvg-nostr','agente','assinar'] for c in calls)
    assert not any(c[:2]==['neo-nostr-rpc','publicar'] for c in calls)
    print('CONFIRMADO clean-dms: anuncia envio, mas só consulta e assina; nenhuma publicação')

    # A função real consome todos os argumentos antes de need_root.
    flash=function('neo/bin/neo-flash','cmd_seedsigner')
    p,_=run_code(f'source "{common}"\n'+flash+'\nconfere_alvo_basico() { :; }\nneed_root() { printf "argumentos_na_elevacao=%s\\n" "$#"; exit; }\ncmd_seedsigner --para /dev/TESTE --modelo pi02w')
    assert 'argumentos_na_elevacao=0' in p.stdout
    print('CONFIRMADO flash: comando, destino e modelo perdidos antes da elevação')

    for mode in ['bluetooth_pan', 'wifi_direct']:
        f=function('neo/bin/neo-mesh',mode)
        p,_=run_code(f'source "{common}"\n'+f+'\nneed_root() { printf "argumentos_na_elevacao=%s\\n" "$#"; exit; }\n'+mode)
        assert 'argumentos_na_elevacao=0' in p.stdout
    print('CONFIRMADO mesh: bluetooth_pan e wifi_direct perdem o seletor antes da elevação')

    p,calls=run_code(script('neo/bin/neo-sync'),'--nostr')
    published=[c[c.index('--evento')+1] for c in calls if c[:2]==['neo-nostr-rpc','publicar'] and '--relay' not in c]
    assert published and all('antiga-offline' not in ev for ev in published)
    assert 'nova-local' in published[0]
    print('CONFIRMADO sync: consulta inclui o relay local e deixa nota offline antiga sem publicar')

    # Cópia real do secureboot com /boot e /efi confinados ao temporário.
    boot=base/'boot'; boot.mkdir(); (boot/'vmlinuz-linux').write_text('DUMMY')
    secure=base/'neo-secureboot'
    secure.write_text(script('neo/bin/neo-secureboot').replace('/boot/',str(boot)+'/').replace('/efi/',str(base/'efi')+'/'))
    secure.chmod(0o755)
    log.write_text('')
    p=subprocess.run([str(secure),'setup'],env=env,text=True,capture_output=True,timeout=15)
    assert p.returncode==0 and 'keys enrolled and the chain signed' in p.stdout and 'could not sign' in p.stderr
    print('CONFIRMADO secureboot: falha em sign, mas setup retorna 0 e anuncia cadeia assinada')

    # Executa o gerador PostScript real, sem impressora ou seed.
    # Intercepta só ps2pdf para guardar o fonte exato que seria impresso.
    ps=fake/'ps2pdf'; ps.write_text('#!/bin/sh\ncp -- "$1" "$2"\n'); ps.chmod(0o755)
    out=base/'paper.ps'
    p,_=run_code(script('neo/bin/neo-paper'),'--palavras','24','--saida',str(out))
    assert p.returncode==0,p.stderr
    rects=re.findall(r'(-?\d+) mm (-?\d+) mm 7 mm 6 mm rectstroke',out.read_text())
    outside=sum(int(y)+6<0 for _,y in rects)
    assert outside==24,(outside,rects)
    print('CONFIRMADO paper: 24 das 96 células de aço ficam inteiramente abaixo da página (palavras 19–24)')
