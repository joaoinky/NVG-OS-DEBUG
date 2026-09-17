# NVG-22 — Sincronização deixa eventos offline antigos sem publicar

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **média** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-sync:34](../../../neo/bin/neo-sync#L34) e [relays_padrao/consultar](../../../neo/bin/neo-nostr-rpc#L45).

O cursor deveria representar o evento mais novo conhecido externamente, mas a consulta que calcula `ultimo` não informa `--relay`. A lista padrão inclui o relay local. Com duas notas somente locais, o timestamp da mais nova vira `since`; a mais antiga é excluída do upload. Repetir a sincronização não a recupera enquanto esse cursor prevalecer. Como o relay local é volátil, desligar a máquina pode perder a única cópia.

## Evidência

O script real recebeu um cenário simulado com eventos locais nos tempos 100 e 200, ausentes externamente. A consulta agregada devolveu 200; só esse evento chegou à publicação externa. O evento 100 foi omitido. [Log](evidencias/probes-shell.log).

## Limites da conclusão

Não foi contatado relay público. A omissão decorre do cursor observado e da composição da lista padrão. Mesmo retirar o relay local não torna um timestamp global suficiente para detectar todas as lacunas entre relays; isso é requisito para a correção, não outra falha contabilizada.

## Direção da correção

Comparar presença por IDs ou manter fila/estado de publicação por destino, com confirmações externas. Testar múltiplas notas offline, falhas parciais, relays divergentes e reinício.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
