# Cadeia 04 — Firewall muda, painel conserva o modo anterior

> **Status: RESOLVIDO**: corrigido na branch `fix/04-07-marcadores` (PR #3, `NVG-05`), que chegou à `main` pelo PR #4. A correção local da terceira rodada ([correcoes-03](correcoes-03.md)) foi **substituída** por esta, conforme a regra de que prevalece o código do `neovanguard-os-dev`.

Erro: **NVG-05**. Impacto: alto, indicação de proteção incompatível com as regras. Verificação: sequência reproduzida com nft simulado e marcadores reais em diretório temporário.

## Solução aplicada

Os comandos de troca de firewall agora invalidam os caches antes da mudança e só gravam um marcador depois de confirmar o ruleset carregado no kernel. O `neo-status` faz uma consulta nova, em vez de confiar na existência do arquivo; assim, voltar ao firewall base não preserva uma indicação Tor antiga. A verificação e a gravação são serializadas por lock, e o cache guarda a evidência JSON observada.

Validação: testes de troca de modos, marcador órfão, regras sem marcador e alteração externa passaram (14 em `test-network-modes.py`, 16 em `test-network-state.py`, reexecutados em 11/09/2026). [Registro da rodada](correcoes-04.md).

O texto abaixo registra o problema original; as linhas citadas são as do commit auditado.

## Walkthrough

1. `neo-tor` aplica `tor.nft` e cria o marcador `tor`: [neo/bin/neo-tor:38](../../../neo/bin/neo-tor:38).
2. `neo-killswitch` aplica outro arquivo, que começa com `flush ruleset`, e cria `killswitch`. Não remove o marcador `tor`: [neo/bin/neo-killswitch:27](../../../neo/bin/neo-killswitch:27).
3. Ao executar `neo-killswitch-off`, o script aplica `base.nft` e remove somente `killswitch`: [neo/bin/neo-killswitch-off:15](../../../neo/bin/neo-killswitch-off:15).
4. O marcador `tor` permanece, embora o firewall base tenha saída liberada e não contenha o redirecionamento transparente: [neo/etc/nftables/base.nft:68](../../../neo/etc/nftables/base.nft:68).
5. `neo-status` consulta os marcadores para decidir o texto e os valores JSON: [neo/bin/neo-status:25](../../../neo/bin/neo-status:25). Pode anunciar “Tor total” com saída direta.

## Evidência observada

| Etapa simulada | Marcador tor | Marcador killswitch | Último arquivo solicitado ao nft |
|---|---|---|---|
| Após killswitch, com tor já marcado | presente | presente | killswitch-tor.nft |
| Após killswitch-off | presente | ausente | base.nft |

Ambos os scripts retornaram 0. A simulação confirmou chamadas e estados; não carregou regras no kernel. A sequência inversa com `neo-tor-off` também remove somente seu próprio marcador, embora substitua todas as regras.

## Pontos de toque

- `neo-tor/neo-killswitch → *.nft → marcadores → neo-status`.
- A substituição também remove o redirecionamento Tor ao ativar killswitch; os modos não se acumulam como os marcadores sugerem.
- [Cadeia 05](✅-05-conexoes-anteriores-ao-bloqueio.md) e [Cadeia 06](✅-06-dns-fora-do-tor.md) tratam das próprias permissões das regras, mesmo quando o marcador corresponde ao arquivo.
- [Cadeia 07](✅-07-airgap-sucesso-sem-isolamento.md) compartilha a biblioteca de marcadores e o painel.
- [Índice](README.md).
