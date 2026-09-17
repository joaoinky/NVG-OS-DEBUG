# Terceira rodada de correções

> **Substituída pela [quarta rodada](correcoes-04.md).** Esta versão (remover os marcadores dos outros modos antes de marcar o novo) continua no histórico, no commit `3e0b344`. O PR #3 do `neovanguard-os-dev` trocou o marcador-como-prova por verificação do ruleset no kernel, e, pela regra desta auditoria, prevalece o código de lá. O registro abaixo fica para não se perder o que foi feito e medido localmente.

Data: 09/09/2026. Escopo: NVG-05, a divergência entre o firewall carregado e o painel de rede.

## Alteração

Os modos Tor, kill-switch e firewall base substituem integralmente o ruleset. Cada comando agora remove os marcadores dos modos que deixou de aplicar antes de marcar o modo novo. Assim, o `neo-status` só mostra Tor total ou kill-switch quando o último ruleset carregado corresponde a esse estado.

## Evidência

- Reprodução isolada aprovada com `nft`, Tor e privilégios simulados.
- A sequência Tor → kill-switch → Tor → firewall base manteve somente o marcador do ruleset vigente em cada etapa.
- Sintaxe Bash e validação dos 55 comandos `neo-*` aprovadas.

Nenhuma regra foi carregada no firewall do host durante o teste.

## Pendências

NVG-06 a NVG-09 e a divergência do índice do repositório de pacotes locais continuam pendentes.
