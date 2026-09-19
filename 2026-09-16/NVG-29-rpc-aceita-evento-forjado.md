# NVG-29 — Cliente Nostr aceita perfil com hash e assinatura inválidos

**Estado: corrigido e integrado à main em 18/09/2026; validação em ISO/VM pendente.** Gravidade original: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[consultar_um/consultar](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/neo-nostr-rpc#L65), [neo-nostr-profile](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/neo-nostr-profile) e [resolução de destino do zap](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/neo-zap#L44).

O helper Python acrescenta qualquer objeto recebido em uma mensagem EVENT, deduplica pelo `id` declarado e devolve conteúdo sem validar hash, assinatura ou correspondência ao filtro. `neo-nostr-profile` usa esse conteúdo e `neo-zap` extrai `lud16`/`lud06` como destino. Um relay malicioso consultado pode atribuir à chave desejada um endereço de pagamento controlado por ele, sem possuir essa chave.

## Evidência

Executou-se `consultar()` real com transporte WebSocket simulado. Um perfil com ID zerado comprovadamente diferente do hash calculado e assinatura zerada foi devolvido intacto. Seu conteúdo continha um endereço fictício de impostor. [Prova e log](evidencias/probes-nostr-payment.log). O vínculo entre conteúdo, ID e assinatura é definido pelo [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md).

## Limites da conclusão

Não se comprometeu relay nem se realizou pagamento. O cenário exige uma resposta desonesta em algum relay consultado. O achado é do helper Python; não se estende automaticamente ao cliente Rust/SDK, que possui outro caminho de validação.

## Direção da correção

Validar estrutura, hash, assinatura, autor, kind e filtro antes de deduplicar/selecionar eventos. Preferir implementação Nostr já usada e testada pelo projeto. Testar perfis forjados e eventos válidos fora do filtro.

## Correção e regressão — 2026-09-18

O helper só aceita envelopes EVENT/EOSE da inscrição ativa. Antes de deduplicar
ou ordenar, envia os candidatos ao novo comando `nvg-nostr eventos-verificar`,
que usa o SDK Nostr já presente para desserializar os eventos, verificar hash e
assinatura Schnorr e conferir autor, kind, IDs, tags e intervalo temporal do
filtro. Eventos inválidos são descartados individualmente; ausência, erro ou
timeout do verificador aborta a consulta sem devolver conteúdo não verificado.
Não há implementação própria de criptografia nem nova biblioteca de produção.
O helper e o pacote `neovanguard-base` devem ser atualizados juntos.

Regressão reproduzível, sem relay público nem pagamentos:

```sh
cd rust
cargo test --locked -p nvg-nostr --test rpc_eventos
```

O teste Rust gera eventos assinados e executa nove testes Python sobre o helper
real e o binário compilado, com WebSocket simulado. Cobre hash/assinatura
inválidos, estruturas malformadas, autor/kind fora do filtro, ID/tags/tempo,
listas de restrição vazias, inscrições incorretas, Unicode, ordenação,
deduplicação entre relays e indisponibilidade do verificador. Inclui a tentativa
de enviar conteúdo forjado com o ID de um perfil legítimo antes da cópia válida.

Validação nesta máquina: regressão acima passou; `cargo fmt --all --check` e
`cargo clippy --locked --offline -p nvg-nostr --all-targets -- -D warnings`
passaram. A suíte do pacote passou com 55 testes unitários e duas integrações
(uma delas contém os nove casos Python), excluindo apenas
`manifest::testes::aceleracao_so_com_a_gpu_certa`, cuja falha foi reproduzida e
já está documentada no NVG-28. O teste de relay local exigiu sockets liberados
fora do sandbox. `check-neo-cli.py` passou; `check-neo-refs.py` reproduziu o
falso alarme de pacote `systemd` descrito no NVG-32. Não foi construída uma ISO.

Implementação: [`1917f0d`](https://github.com/NEOpisa/neovanguard-os-dev/commit/1917f0d) · [PR #9 — integrado](https://github.com/NEOpisa/neovanguard-os-dev/pull/9). Consulte o [registro da rodada](correcoes-2026-09-18.md) para os commits de merge e as pendências.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
