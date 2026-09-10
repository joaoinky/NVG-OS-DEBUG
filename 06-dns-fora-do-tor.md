# Cadeia 06 — Exceção de LAN deixa DNS escapar do Tor

> **Status: RESOLVIDO** — corrigido na branch `fix/regras-nft-excecoes` (`NVG-07`).

Erro: **NVG-07**. Impacto: alto para privacidade de consultas. Verificação: percurso estático de regras; nenhuma consulta externa realizada.

## Solução aplicada

Em `tor.nft`, UDP/53 e TCP/53 agora são tratados antes da exceção de redes privadas: UDP é redirecionado ao DNSPort 9053 e TCP ao TransPort 9040. O filtro também descarta DNS residual que chegaria à LAN sem redirecionamento, inclusive em fluxos anteriores.

Validação: DNS novo para resolvedores privados e públicos alcançou as portas locais esperadas; DNS TCP/UDP preexistente não escapou. LAN não-DNS e DHCP continuam permitidos.

## Walkthrough

1. A máquina usa um resolvedor em endereço privado, por exemplo o roteador `192.168.1.1`. Esse é o cenário necessário ao erro, não uma configuração observada na máquina do usuário.
2. O usuário ativa `neo-tor`, que anuncia tráfego pelo Tor.
3. Uma consulta UDP para `192.168.1.1:53` encontra primeiro a exceção para redes privadas na cadeia NAT: [neo/etc/nftables/tor.nft:52](../neovanguard-os-dev/neo/etc/nftables/tor.nft:52).
4. O `return` encerra a avaliação dessa cadeia antes da regra de redirecionamento DNS na linha 60.
5. Na cadeia de saída, a permissão geral para destinos privados aceita o pacote: [neo/etc/nftables/tor.nft:43](../neovanguard-os-dev/neo/etc/nftables/tor.nft:43).
6. A consulta chega diretamente ao resolvedor da LAN, sem atravessar o DNSPort do Tor.

## O erro

A exceção para rede local precede e neutraliza o tratamento de DNS nesse cenário. Os nomes consultados ficam visíveis ao resolvedor local; o eventual encaminhamento dele ao provedor depende da configuração desse resolvedor e não foi verificado.

A ordem de avaliação e o significado de `return` são descritos no [manual oficial do nftables](https://netfilter.org/projects/nftables/manpage.html). O achado decorre da aplicação dessa semântica às regras locais.

## Pontos de toque

- Configuração de DNS da conexão → `tor.nft/redirecionar` → `tor.nft/saida` → resolvedor local.
- [neo/etc/tor/torrc:10](../neovanguard-os-dev/neo/etc/tor/torrc:10) fornece o DNSPort, mas esse pacote não chega a ele.
- [Cadeia 05](05-conexoes-anteriores-ao-bloqueio.md): não depende de uma conexão anterior, ao contrário daquele caso.
- [Cadeia 04](04-firewall-e-painel.md): a indicação “Tor total” não verifica o percurso de DNS.
- [Índice](README.md).
