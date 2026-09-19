# NVG-28 - Teste do manifesto falha em hosts NVIDIA e bloqueia o check

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **média** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[manifest.rs:297](../../../rust/nvg-nostr/src/manifest.rs#L297), [hardware.rs](../../../rust/nvg-nostr/src/hardware.rs#L13) e [PKGBUILD check](../../../neo/packaging/pkgbuilds/neovanguard-base/PKGBUILD#L79).

O teste pede GPU Intel e aceleração CUDA e espera sempre `nenhuma`. Contudo a implementação decide pela GPU detectada de verdade por `lspci`, deliberadamente prevalecendo sobre o manifesto. Em uma máquina NVIDIA, CUDA é resultado válido e a asserção falha. O teste integra `./check` e o `check()` do pacote base, tornando a aprovação dependente do hardware do construtor.

## Evidência

A execução original teve 55 sucessos e uma falha no crate. Repetiu-se apenas esse teste em processos separados com `lspci` simulado: NVIDIA retornou 101, `left: cuda`; Intel retornou 0. [Log comparativo](evidencias/probe-gpu.log).

## Limites da conclusão

Não é evidência de driver CUDA errado nem de falha do detector. O defeito confirmado é o teste não isolado; o build release completo do pacote não foi repetido, mas seu check chama o mesmo teste sem condicional.

## Direção da correção

Injetar a detecção de hardware ou separar a decisão pura, cobrindo explicitamente Intel/NVIDIA/AMD/nenhuma sem consultar a máquina que executa a suíte.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
