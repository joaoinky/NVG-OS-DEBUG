# Cadeia 04 — Firewall muda, painel conserva o modo anterior

Erro: **NVG-05**. Impacto: alto, indicação de proteção incompatível com as regras. Verificação: sequência reproduzida com nft simulado e marcadores reais em diretório temporário.

## Walkthrough

1. `neo-tor` aplica `tor.nft` e cria o marcador `tor`: [neo/bin/neo-tor:38](../neovanguard-os-dev/neo/bin/neo-tor:38).
2. `neo-killswitch` aplica outro arquivo, que começa com `flush ruleset`, e cria `killswitch`. Não remove o marcador `tor`: [neo/bin/neo-killswitch:27](../neovanguard-os-dev/neo/bin/neo-killswitch:27).
3. Ao executar `neo-killswitch-off`, o script aplica `base.nft` e remove somente `killswitch`: [neo/bin/neo-killswitch-off:15](../neovanguard-os-dev/neo/bin/neo-killswitch-off:15).
4. O marcador `tor` permanece, embora o firewall base tenha saída liberada e não contenha o redirecionamento transparente: [neo/etc/nftables/base.nft:68](../neovanguard-os-dev/neo/etc/nftables/base.nft:68).
5. `neo-status` consulta os marcadores para decidir o texto e os valores JSON: [neo/bin/neo-status:25](../neovanguard-os-dev/neo/bin/neo-status:25). Pode anunciar “Tor total” com saída direta.

## Evidência observada

| Etapa simulada | Marcador tor | Marcador killswitch | Último arquivo solicitado ao nft |
|---|---|---|---|
| Após killswitch, com tor já marcado | presente | presente | killswitch-tor.nft |
| Após killswitch-off | presente | ausente | base.nft |

Ambos os scripts retornaram 0. A simulação confirmou chamadas e estados; não carregou regras no kernel. A sequência inversa com `neo-tor-off` também remove somente seu próprio marcador, embora substitua todas as regras.

## Pontos de toque

- `neo-tor/neo-killswitch → *.nft → marcadores → neo-status`.
- A substituição também remove o redirecionamento Tor ao ativar killswitch; os modos não se acumulam como os marcadores sugerem.
- [Cadeia 05](05-conexoes-anteriores-ao-bloqueio.md) e [Cadeia 06](06-dns-fora-do-tor.md) tratam das próprias permissões das regras, mesmo quando o marcador corresponde ao arquivo.
- [Cadeia 07](07-airgap-sucesso-sem-isolamento.md) compartilha a biblioteca de marcadores e o painel.
- [Índice](README.md).
