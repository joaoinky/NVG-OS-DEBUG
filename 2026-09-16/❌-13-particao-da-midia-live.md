# NVG-13 - Partições da mídia Live são aceitas como destino manual

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[disk.rs:218](../../../rust/nvg-installer/src/disk.rs#L218), [app.rs:733 e validação de disco](../../../rust/nvg-installer/src/app.rs#L733), [install.rs:158 e partition](../../../rust/nvg-installer/src/install.rs#L158).

`all_partitions()` inclui as partições de discos identificados como `is_live_media`. A tela manual usa essa lista inteira. A recusa da mídia Live existe apenas no modo de apagar o disco; a validação final do plano também não a verifica. Uma partição da mídia de origem pode ser escolhida como raiz com formatação habilitada. `partition()` tenta desmontá-la e o fluxo segue para LUKS/formatação conforme as escolhas. A proteção documentada para a mídia não cobre esse caminho.

## Evidência

A prova Rust `manual_aceita_particao_da_midia_live` usa a mídia Live da fixture real do instalador e modo MBN. Confirma que ela aparece no seletor, passa em `App::validate()` e `Plan::validate_before_install()` e conserva `format_root=true`. [Resultado](evidencias/rust-probes.log).

## Limites da conclusão

Não foi formatada nenhuma mídia. A aceitação e o encaminhamento ao fluxo destrutivo estão demonstrados; a escrita efetiva depende de a mídia estar gravável e de desmontagem/bloqueios das ferramentas. Uma recusa tardia por dispositivo ocupado não substitui a proteção na seleção e no plano.

## Direção da correção

Excluir a mídia de origem dos seletores e revalidar os dispositivos concretos imediatamente antes das operações. Preservar a relação entre partição e disco; testar todas as funções de raiz, ESP e home.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
