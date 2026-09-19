# NVG-20 - Limpeza de DMs anuncia envio sem publicar pedidos de exclusão

**Estado: corrigido no código em 19/09/2026; PR #31 aberto; validação em ISO e relay real pendente.** Gravidade original: **média**. Base da auditoria: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação). A evidência abaixo descreve o comportamento anterior à correção.

## Onde e como acontece

[neo-clean-dms:34](../../../neo/bin/neo-clean-dms#L34).

O laço chama `nvg-nostr agente assinar`, descarta a saída e incrementa o contador. Não chama a operação de publicação do relay. Mesmo com assinatura bem-sucedida, o evento não sai do processo, mas o comando termina informando que pedidos foram enviados ao relay local. A limpeza solicitada não é executada.

## Evidência

O script completo rodou com respostas e assinador simulados, confirmação `APAGAR` e registro de todas as chamadas. Houve consulta e assinatura, nenhuma chamada `neo-nostr-rpc publicar`, e retorno de sucesso com a mensagem de envio. [Log](evidencias/probes-shell.log), linha “clean-dms”.

## Limites da conclusão

Não se testou exclusão em um relay real. A ausência da publicação é suficiente para impedir o fluxo. Há ainda uma falha independente nas tags da CLI, registrada separadamente no [NVG-31](✅-31-assinatura-descarta-tags.md). Nem publicar corretamente garante que relays externos apaguem cópias.

## Direção da correção

Capturar o evento assinado, publicar explicitamente no relay pretendido e contar confirmações reais. Conferir autoria e semântica de exclusão dos kinds tratados antes de prometer remoção.

## Correção implementada

O [PR #31](https://github.com/NEOpisa/neovanguard-os-dev/pull/31), commit
[`1c2d7b4`](https://github.com/NEOpisa/neovanguard-os-dev/commit/1c2d7b4),
faz `neo-clean-dms` consultar a identidade ativa, fixar uma lista de alvos e
pedir confirmação antes de assinar. Cada pedido kind 5 é conferido quanto à
autoria, conteúdo, tags `e` e `k` e assinatura antes de ser publicado no relay
local. Só uma resposta `OK` positiva para o mesmo ID entra na contagem.

As consultas agora exigem EOSE da inscrição correta, distinguindo resultado
vazio de falha ou resposta incompleta. Eventos duplicados são consolidados e a
mesma lista é usada na confirmação e no processamento. Recusa do usuário ou do
agente, assinatura inválida, troca de identidade, ausência de confirmação e
falha parcial retornam erro sem anunciar sucesso indevido.

O escopo segue a NIP-09 para DMs kind 4 criadas pela identidade ativa e a
NIP-59 para envelopes kind 1059 destinados a ela. DMs kind 4 recebidas de
outros autores não são selecionadas. A consulta trata até 1000 eventos de cada
kind por execução.

## Validação da correção

A integração executou CLI, shell, RPC e validação criptográfica reais com
chaves descartáveis, socket Unix temporário e transporte WebSocket simulado.
Foram aprovados 16 cenários de limpeza e 12 de consulta/publicação. As suítes
`nvg-nostr` e `nvg-nostr-agent` também passaram, excluindo apenas o teste de GPU
já registrado no NVG-28. Formatação e Clippy passaram sem avisos.

Ainda é necessário validar na ISO os prompts do agente e o relay empacotado,
principalmente a exclusão de kind 1059 pelo destinatário. Uma confirmação
positiva aceita o pedido, mas não comprova remoção física nem apagamento de
cópias mantidas por outros relays.

[Registro da correção conjunta](correcoes-2026-09-19.md) · [PR #31](https://github.com/NEOpisa/neovanguard-os-dev/pull/31)

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
