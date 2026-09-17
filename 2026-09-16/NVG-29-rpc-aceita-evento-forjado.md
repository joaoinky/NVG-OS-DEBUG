# NVG-29 — Cliente Nostr aceita perfil com hash e assinatura inválidos

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[consultar_um/consultar](../../../neo/bin/neo-nostr-rpc#L65), [neo-nostr-profile](../../../neo/bin/neo-nostr-profile) e [resolução de destino do zap](../../../neo/bin/neo-zap#L44).

O helper Python acrescenta qualquer objeto recebido em uma mensagem EVENT, deduplica pelo `id` declarado e devolve conteúdo sem validar hash, assinatura ou correspondência ao filtro. `neo-nostr-profile` usa esse conteúdo e `neo-zap` extrai `lud16`/`lud06` como destino. Um relay malicioso consultado pode atribuir à chave desejada um endereço de pagamento controlado por ele, sem possuir essa chave.

## Evidência

Executou-se `consultar()` real com transporte WebSocket simulado. Um perfil com ID zerado comprovadamente diferente do hash calculado e assinatura zerada foi devolvido intacto. Seu conteúdo continha um endereço fictício de impostor. [Prova e log](evidencias/probes-nostr-payment.log). O vínculo entre conteúdo, ID e assinatura é definido pelo [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md).

## Limites da conclusão

Não se comprometeu relay nem se realizou pagamento. O cenário exige uma resposta desonesta em algum relay consultado. O achado é do helper Python; não se estende automaticamente ao cliente Rust/SDK, que possui outro caminho de validação.

## Direção da correção

Validar estrutura, hash, assinatura, autor, kind e filtro antes de deduplicar/selecionar eventos. Preferir implementação Nostr já usada e testada pelo projeto. Testar perfis forjados e eventos válidos fora do filtro.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
