# NVG-14 — A mesma partição pode ser raiz, ESP e home

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[app.rs:980](../../../rust/nvg-installer/src/app.rs#L980) e [install.rs:786–951, partition/format_fs/mount](../../../rust/nvg-installer/src/install.rs#L786).

O modo manual verifica existência de opções e seleção de ESP em UEFI, mas não exige dispositivos distintos. É possível selecionar uma ESP FAT de 512 MiB para as três funções. A formatação da raiz a converte para Btrfs/ext4/XFS; a etapa seguinte ainda a considera uma ESP preservada. O código pula a montagem separada de `/boot` quando boot e raiz são iguais. Isso destrói o conteúdo anterior da ESP e deixa um layout incompatível com a intenção apresentada.

## Evidência

`manual_aceita_raiz_esp_home_iguais_e_pequenos` passa a mesma ESP da fixture aos três seletores; ambas as validações aceitam. O plano conserva os três caminhos iguais e a formatação habilitada. [Resultado](evidencias/rust-probes.log).

## Limites da conclusão

A prova não executou mkfs. O conflito de funções e sua chegada ao plano são confirmados; o primeiro erro observado na instalação depende do sistema de arquivos e do tamanho. A ausência de checagem de capacidade agrava esse caso, mas não foi contada como outro achado.

## Direção da correção

Rejeitar sobreposição por identidade real do dispositivo, inclusive aliases. Validar tipo/capacidade da ESP e capacidade da raiz antes de qualquer escrita. Cobrir combinações manuais em VM com discos descartáveis.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
