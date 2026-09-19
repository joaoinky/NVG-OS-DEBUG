# NVG-20 - Limpeza de DMs anuncia envio sem publicar pedidos de exclusão

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **média** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-clean-dms:34](../../../neo/bin/neo-clean-dms#L34).

O laço chama `nvg-nostr agente assinar`, descarta a saída e incrementa o contador. Não chama a operação de publicação do relay. Mesmo com assinatura bem-sucedida, o evento não sai do processo, mas o comando termina informando que pedidos foram enviados ao relay local. A limpeza solicitada não é executada.

## Evidência

O script completo rodou com respostas e assinador simulados, confirmação `APAGAR` e registro de todas as chamadas. Houve consulta e assinatura, nenhuma chamada `neo-nostr-rpc publicar`, e retorno de sucesso com a mensagem de envio. [Log](evidencias/probes-shell.log), linha “clean-dms”.

## Limites da conclusão

Não se testou exclusão em um relay real. A ausência da publicação é suficiente para impedir o fluxo. Há ainda uma falha independente nas tags da CLI, registrada separadamente no [NVG-31](❌-31-assinatura-descarta-tags.md). Nem publicar corretamente garante que relays externos apaguem cópias.

## Direção da correção

Capturar o evento assinado, publicar explicitamente no relay pretendido e contar confirmações reais. Conferir autoria e semântica de exclusão dos kinds tratados antes de prometer remoção.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
