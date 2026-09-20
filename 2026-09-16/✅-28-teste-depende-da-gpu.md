# NVG-28 - Teste do manifesto falha em hosts NVIDIA e bloqueia o check

**Estado: corrigido no código em 20/09/2026; PR #32 aberto; validação no sistema instalado pendente.** Gravidade original: **média** no cenário descrito. Base da auditoria: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[manifest.rs:297](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/rust/nvg-nostr/src/manifest.rs#L297), [hardware.rs](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/rust/nvg-nostr/src/hardware.rs#L13) e [PKGBUILD check](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/packaging/pkgbuilds/neovanguard-base/PKGBUILD#L79).

O teste pede GPU Intel e aceleração CUDA e espera sempre `nenhuma`. Contudo a implementação decide pela GPU detectada de verdade por `lspci`, deliberadamente prevalecendo sobre o manifesto. Em uma máquina NVIDIA, CUDA é resultado válido e a asserção falha. O teste integra `./check` e o `check()` do pacote base, tornando a aprovação dependente do hardware do construtor.

## Evidência

A execução original teve 55 sucessos e uma falha no crate. Repetiu-se apenas esse teste em processos separados com `lspci` simulado: NVIDIA retornou 101, `left: cuda`; Intel retornou 0. [Log comparativo](evidencias/probe-gpu.log).

## Limites da conclusão

Não é evidência de driver CUDA errado nem de falha do detector. O defeito confirmado é o teste não isolado; o build release completo do pacote não foi repetido, mas seu check chama o mesmo teste sem condicional.

## Direção da correção

Injetar a detecção de hardware ou separar a decisão pura, cobrindo explicitamente Intel/NVIDIA/AMD/nenhuma sem consultar a máquina que executa a suíte.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)

## Correção implementada em 20/09

[PR #32](https://github.com/NEOpisa/neovanguard-os-dev/pull/32), branch `fix/nvg-nostr-robustness`.
Commits de implementação: [`6e379b3`](https://github.com/NEOpisa/neovanguard-os-dev/commit/6e379b3), [`eca3a45`](https://github.com/NEOpisa/neovanguard-os-dev/commit/eca3a45).

Envelopes com tamanho inválido podiam abortar o processo, e o teste de aceleração dependia da GPU do host. A decifragem agora valida versão, tamanhos e quantidade de blocos, limita o pacote a 8 MiB e usa reserva falível. Os testes de aceleração cobrem Intel, NVIDIA, AMD e ausência de GPU sem consultar o hardware do executor.

## Validação e limites

`./check quick` aprovado: 198 testes Rust, formatação, Clippy e verificações de empacotamento. Regressões cobrem envelopes malformados, limites de blocos e pacote de 8 MiB. A entrada com `bruto=u64::MAX` também retornou erro em executável com `panic=abort`.

Não foi construída ISO. Falta conferir os binários empacotados e a restauração no sistema instalado.

As provas originais acima registram o comportamento anterior à correção. O PR ainda não foi integrado à `main`.

[Registro dos cinco grupos](correcoes-2026-09-20.md) · [PR #32](https://github.com/NEOpisa/neovanguard-os-dev/pull/32)
