# NVG-22 - Sincronização deixa eventos offline antigos sem publicar

**Estado: corrigido no código em 20/09/2026; PR #34 aberto; validação no sistema instalado pendente.** Gravidade original: **média** no cenário descrito. Base da auditoria: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-sync:34](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/neo-sync#L34) e [relays_padrao/consultar](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/neo-nostr-rpc#L45).

O cursor deveria representar o evento mais novo conhecido externamente, mas a consulta que calcula `ultimo` não informa `--relay`. A lista padrão inclui o relay local. Com duas notas somente locais, o timestamp da mais nova vira `since`; a mais antiga é excluída do upload. Repetir a sincronização não a recupera enquanto esse cursor prevalecer. Como o relay local é volátil, desligar a máquina pode perder a única cópia.

## Evidência

O script real recebeu um cenário simulado com eventos locais nos tempos 100 e 200, ausentes externamente. A consulta agregada devolveu 200; só esse evento chegou à publicação externa. O evento 100 foi omitido. [Log](evidencias/probes-shell.log).

## Limites da conclusão

Não foi contatado relay público. A omissão decorre do cursor observado e da composição da lista padrão. Mesmo retirar o relay local não torna um timestamp global suficiente para detectar todas as lacunas entre relays; isso é requisito para a correção, não outra falha contabilizada.

## Direção da correção

Comparar presença por IDs ou manter fila/estado de publicação por destino, com confirmações externas. Testar múltiplas notas offline, falhas parciais, relays divergentes e reinício.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)

## Correção implementada em 20/09

[PR #34](https://github.com/NEOpisa/neovanguard-os-dev/pull/34), branch `fix/nvg-22-sync-cursor`.
Commits de implementação: [`a0a1974`](https://github.com/NEOpisa/neovanguard-os-dev/commit/a0a1974).

O timestamp agregado incluía o relay local e omitia notas offline antigas. A sincronização compara IDs por destino externo, consulta as notas locais sem o corte de 500 eventos e exige EOSE e confirmação positiva do ID publicado. Falhas parciais retornam erro e são reconciliadas na próxima execução, sem cursor persistido. A atualização das 200 notas recentes por destino e o fluxo Bitcoin são preservados.

## Validação e limites

22 cenários aprovados na integração `cargo test --locked -p nvg-nostr --test rpc_eventos`: 12 de RPC e 10 de sincronização, com eventos assinados e verificador Rust real. Cobertura inclui 501 notas no mesmo timestamp, relays divergentes, ACK incorreto, falha parcial e retomada. Formatação, Clippy, sintaxe shell e verificação dos comandos aprovados.

Transporte simulado; falta validar com o relay empacotado e dois relays reais. A retomada depende de os eventos ainda existirem no relay local, cujo armazenamento é volátil. `./check quick` completo não foi repetido. Compartilha mudanças de EOSE/ACK em `neo-nostr-rpc` e testes com o PR #31; revisar essa sobreposição ao integrar.

As provas originais acima registram o comportamento anterior à correção. O PR ainda não foi integrado à `main`.

[Registro dos cinco grupos](correcoes-2026-09-20.md) · [PR #34](https://github.com/NEOpisa/neovanguard-os-dev/pull/34)
