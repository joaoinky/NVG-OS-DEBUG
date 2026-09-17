"""Somente consultas pacman; depende de conflito de versões no host."""
import subprocess
info=subprocess.run(['pacman','-Si','systemd'],text=True,capture_output=True)
resolve=subprocess.run(['pacman','-Sp','--print-format','%n','systemd'],text=True,capture_output=True)
check=subprocess.run(['python3','scripts/check-neo-refs.py'],text=True,capture_output=True)
print('pacman -Si systemd:',info.returncode)
print('pacman -Sp systemd:',resolve.returncode)
print(resolve.stdout)
print(resolve.stderr)
print('check-neo-refs:',check.returncode)
print(check.stdout)
if info.returncode==0 and resolve.returncode!=0 and 'systemd' in check.stdout:
    print('CONFIRMADO neste host: pacote existente é anunciado como inexistente por conflito de dependências da instalação local')
else:
    print('Cenário não reproduzido neste host; consultar log original e condições do relatório NVG-32')
