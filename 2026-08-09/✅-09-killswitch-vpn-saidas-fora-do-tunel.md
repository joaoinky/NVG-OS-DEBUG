# Cadeia 09 - Kill-switch de VPN deixa saídas fora do túnel

> **Status: RESOLVIDO** na sexta rodada de 11/09/2026. Diagnóstico original preservado abaixo.

## Solução aplicada

- DNS UDP/TCP 53 é descartado após a aceitação do túnel e antes dos endpoints, DHCP e LAN. LAN sem DNS e DHCP continuam liberados.
- UDP irrestrito foi substituído por pares IP/porta. O comando descobre endpoints WireGuard ou exige `--endpoint IP:porta` (repetível, IPv6 entre colchetes). Falta de descoberta ou dados inválidos recusam antes de carregar regras.
- `neo-vpn.py` valida IPs literais e portas antes de gerar nft. A consulta reconhece o bloco variável; a aplicação confere endpoints pedidos contra os carregados antes de gravar cache.
- A referência JSON foi emitida em namespace, revisada e atualizada à mão; `@ENDPOINTS@` é normalizado junto de `@IFACE@`.
- Dez testes de tráfego passaram. O modelo antigo produziu cinco falhas, incluindo DNS UDP/TCP da LAN e UDP irrestrito. Testes de comandos e estado cobrem entradas inválidas, descoberta, IPv4/IPv6, exceções amplas e ordem errada.
- Limites: endpoints UDP, reaplicação após mudança de endpoint e DNS obrigatório pelo túnel. Endpoint na porta 53 fica bloqueado também. A ajuda explica a perda de resolução se a VPN não configurar DNS. Não houve VPN real ou alteração da rede do host.

Evidências finais: [sexta rodada](correcoes-06.md).

Erros: **NVG-10 e NVG-11**. Impacto: alto (NVG-10) e médio (NVG-11). Verificação: tráfego real em namespaces descartáveis, com o mesmo mecanismo de `scripts/test-nft-network.py`. Nenhuma regra foi carregada no firewall da máquina.

As linhas citadas são as da árvore de 11/09/2026 (`main` local `445eb7b`).

## Walkthrough

1. O usuário sobe uma VPN (WireGuard em `wg0`, por exemplo) e liga `neo-killswitch --vpn wg0`. O cabeçalho do comando promete que "nada sai desta máquina fora do túnel": [neo/bin/neo-killswitch:2](../../../neo/bin/neo-killswitch:2).
2. O comando troca `@IFACE@` pelo nome da interface e carrega o modelo: [neo/bin/neo-killswitch:36](../../../neo/bin/neo-killswitch:36). `network_apply_rules` confere que o ruleset carregado é igual à referência e grava o marcador: [neo/lib/neo-rede.sh:55](../../../neo/lib/neo-rede.sh:55). O `neo-status` passa a mostrar o kill-switch como verificado.
3. Na cadeia de saída, antes do descarte final, há três exceções para a interface física:
   - `udp dport { 51820, 1194 } accept`, para qualquer destino: [killswitch-vpn.nft.in:34](../../../neo/etc/nftables/killswitch-vpn.nft.in:34);
   - DHCP: [linha 35](../../../neo/etc/nftables/killswitch-vpn.nft.in:35);
   - `ip daddr { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 } accept`, sem restrição de porta: [linha 38](../../../neo/etc/nftables/killswitch-vpn.nft.in:38).
4. **NVG-10:** o resolvedor da máquina costuma ser o roteador (`192.168.1.1`, entregue pelo DHCP). Uma consulta DNS para ele casa com a exceção da rede local da linha 38 e sai pela interface física, fora do túnel. O roteador encaminha ao provedor, que vê os nomes consultados. Não há regra para a porta 53 neste arquivo.
5. **NVG-11:** a exceção da linha 34 existe para o handshake da VPN, mas não diz para onde. Qualquer processo pode mandar UDP para qualquer host nas portas 51820 e 1194, fora do túnel, com o IP real de origem.
6. A verificação do passo 2 compara o ruleset com a referência (`killswitch-vpn` em [network-policies.json](../../../neo/lib/network-policies.json)). Ela prova que as regras são as do arquivo; não prova que o arquivo cumpre a promessa. Por isso o painel mostra a proteção como confirmada.

## Evidência observada

Sonda com a interface do túnel simulada por uma `dummy` (`nvgvpn0`), um par veth para a "rede física" e um par que responde como eco em `192.168.1.1` e `198.18.0.2`:

| Tráfego pela interface física, com o kill-switch de VPN ligado | Resultado |
|---|---|
| DNS UDP para o resolvedor da LAN (`192.168.1.1:53`) | **sai** |
| DNS TCP para o resolvedor da LAN (`192.168.1.1:53`) | **sai** |
| UDP para a porta 51820 de um host qualquer (`198.18.0.2`) | **sai** |
| TCP para a porta 18080 de um host público | bloqueado |
| DNS UDP para um resolvedor público (`198.18.0.2:53`) | bloqueado |

O bloqueio geral funciona; o que escapa é exatamente o que as duas exceções permitem.

## O erro

A cadeia 06 (NVG-07) é o mesmo defeito no modo Tor, e o PR #1 o corrigiu em `tor.nft`, tratando a porta 53 antes da exceção de LAN. O `killswitch-vpn.nft.in` ficou de fora. O NVG-11 é uma exceção necessária (sem ela o túnel não sobe) que ficou mais larga do que o necessário: o destino legítimo é só o endereço do servidor da VPN.

`scripts/test-nft-network.py` não tem nenhum caso para o modo `killswitch-vpn`, e é por isso que nenhum teste acusou.

## Pontos de toque

- `neo-killswitch --vpn → killswitch-vpn.nft.in → network_apply_rules → network-policies.json → neo-status`.
- [Cadeia 06](✅-06-dns-fora-do-tor.md): mesmo vazamento de DNS no modo Tor, já corrigido.
- [Cadeia 05](✅-05-conexoes-anteriores-ao-bloqueio.md): aqui não se repete, porque a saída do kill-switch de VPN não aceita `ct state established,related`.
- [Cadeia 04](✅-04-firewall-e-painel.md): o painel confirma que as regras carregadas são as do arquivo, não que o arquivo não vaza.
- [Índice](README.md).
