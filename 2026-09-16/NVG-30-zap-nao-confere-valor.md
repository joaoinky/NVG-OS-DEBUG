# NVG-30 — Zap não compara o valor da fatura com os sats solicitados

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-zap:73](../../../neo/bin/neo-zap#L73).

O comando valida os limites anunciados pelo LNURL e solicita `amount`, mas aceita o campo `pr` da resposta sem decodificar seu valor. Em seguida chama `lightning-cli pay <fatura>` ou `lncli payinvoice --force <fatura>`. O nó recebe a fatura, sem receber o limite de sats informado pelo usuário. Um destinatário/servidor LNURL desonesto pode emitir uma fatura maior que a solicitação.

## Evidência

O script completo pediu 1000 sats a um endpoint simulado. A resposta trouxe o vetor público BOLT11 de 2500 microBTC, equivalente a 250000 sats. A chamada registrada foi diretamente `lightning-cli pay <essa fatura>`, sem decodificação ou comparação. [Log](evidencias/probes-nostr-payment.log). O [LUD-06, fluxo LNURL-pay](https://github.com/lnurl/luds/blob/luds/06.md) exige conferir o valor; o vetor está no [BOLT11](https://github.com/lightning/bolts/blob/master/11-payment-encoding.md#examples).

## Limites da conclusão

O pagador foi substituído por um registrador; nenhum satoshi saiu. O vetor de teste está expirado e não demonstra liquidação real. Demonstra que o valor divergente atravessa a fronteira de autorização sem verificação; uma fatura atual válida pode usar o mesmo caminho. Não se trata da opção de pagar uma fatura direta, em que o próprio usuário fornece a fatura.

## Direção da correção

Decodificar/verificar BOLT11 e exigir igualdade exata em millisatoshis, além dos demais vínculos LNURL, antes de chamar o pagador. Rejeitar divergência e resposta inválida. Validar com nó regtest e fundos fictícios.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
