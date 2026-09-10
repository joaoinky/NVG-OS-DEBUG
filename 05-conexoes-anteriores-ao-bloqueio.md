# Cadeia 05 — Conexão direta anterior continua aceita no modo Tor

> **Status: RESOLVIDO** — corrigido na branch `fix/regras-nft-excecoes` (`NVG-06`).

Erro: **NVG-06**. Impacto: alto, tráfego direto permitido apesar do bloqueio anunciado. Verificação: análise das regras e da semântica oficial; sem captura de tráfego.

## Solução aplicada

As regras `tor.nft` e `killswitch-tor.nft` passaram a exigir `meta skuid 43` também para `ct state established,related`. Uma conexão direta preexistente não é mais aceita apenas por estar no conntrack; somente o processo Tor mantém essa exceção explícita.

Validação: sessões TCP/UDP IPv4/IPv6 abertas antes da troca foram bloqueadas nos testes de namespace; o controle positivo do proprietário Tor permaneceu funcionando.

## Walkthrough

1. Um aplicativo comum estabelece uma conexão direta antes da ativação do modo.
2. O usuário ativa `neo-killswitch --tor`. O arquivo substitui as regras, mas sua cadeia de saída aceita `ct state established,related` para qualquer usuário e interface: [neo/etc/nftables/killswitch-tor.nft:20](../neovanguard-os-dev/neo/etc/nftables/killswitch-tor.nft:20).
3. Os pacotes da conexão anterior satisfazem essa condição e são aceitos antes do descarte final. O filtro não exige que pertençam ao processo Tor.
4. `tor.nft` repete essa aceitação: [neo/etc/nftables/tor.nft:40](../neovanguard-os-dev/neo/etc/nftables/tor.nft:40). O redirecionamento NAT não migra automaticamente uma conexão já estabelecida: a associação NAT é definida no início do fluxo, conforme a [documentação do nftables](https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_%28NAT%29).

## O erro

A promessa de que só o Tor atravessa não vale para conexões diretas já rastreadas. A troca do conjunto de regras não encerra essas sessões nem inclui uma operação explícita de limpeza do rastreamento nos comandos examinados. A regra de aceitação é confirmada; a duração e o volume do tráfego dependem das conexões existentes.

A interpretação de `ct state` e da decisão `accept` segue o [manual oficial do nftables](https://netfilter.org/projects/nftables/manpage.html).

## Pontos de toque

- `neo-tor/neo-killswitch → saída nftables → estado de conexões preexistente`.
- [Cadeia 04](04-firewall-e-painel.md): o painel não detecta essa exceção, pois lê marcadores.
- [Cadeia 06](06-dns-fora-do-tor.md): outra saída direta, desta vez possível em consultas novas.
- [Índice](README.md).
