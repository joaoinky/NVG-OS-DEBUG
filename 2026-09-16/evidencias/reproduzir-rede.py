"""Prova de regressão IPv6, restrita a namespaces descartáveis."""
import os, runpy, socket, subprocess, sys, unittest
from pathlib import Path

if len(sys.argv)==1:
    raise SystemExit(subprocess.call(['unshare','-rn',sys.executable,__file__,os.readlink('/proc/self/ns/net')]))
if len(sys.argv)!=2 or os.readlink('/proc/self/ns/net')==sys.argv[1] or socket.if_nameindex()!=[(1,'lo')]:
    raise SystemExit('Recusado: namespace não é descartável')

source=runpy.run_path(str(Path.cwd()/'scripts/test-nft-network.py'),run_name='audit_fixture')
Fixture=source['VpnTraffic']
run=source['run']

class Prova(Fixture):
    @classmethod
    def stop_peer(cls):
        cls.peer.stdin.close()
        cls.peer.wait(timeout=5)
        cls.peer.stdout.close()
        run('nft','flush','ruleset')
        # Destruir o namespace do peer já pode ter removido o par veth.
        subprocess.run(['ip','link','delete','nvg0'],capture_output=True)

    def test_auditoria_endpoint_ipv6_sem_cache(self):
        self.vpn([('2001:db8::2',1194)])
        self.exchange(self.connect('2001:db8::2',socket.SOCK_DGRAM,1194))
        print('Controle: endpoint funciona com vizinho IPv6 previamente resolvido',flush=True)
        run('ip','-6','neigh','flush','dev','nvg0')
        with self.assertRaises((socket.timeout,PermissionError)):
            self.exchange(self.connect('2001:db8::2',socket.SOCK_DGRAM,1194))
        print('CONFIRMADO: mesmo endpoint para de funcionar depois de esvaziar a tabela de vizinhos',flush=True)
        run('nft','insert','rule','inet','neovanguard','saida','meta','l4proto','ipv6-icmp','icmpv6','type','{','nd-neighbor-solicit',',','nd-neighbor-advert','}','accept')
        run('nft','insert','rule','inet','neovanguard','entrada','meta','l4proto','ipv6-icmp','icmpv6','type','{','nd-neighbor-solicit',',','nd-neighbor-advert','}','accept')
        run('ip','-6','neigh','flush','dev','nvg0')
        # O cache do peer também pode vencer. O controle permite apenas NDP.
        sock=self.connect('2001:db8::2',socket.SOCK_DGRAM,1194); sock.settimeout(3)
        self.exchange(sock)
        print('Controle: somente liberar NDP restaura o mesmo endpoint',flush=True)

suite=unittest.TestSuite([Prova('test_auditoria_endpoint_ipv6_sem_cache')])
raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())
