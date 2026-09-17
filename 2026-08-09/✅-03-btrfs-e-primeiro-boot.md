# Cadeia 03 — Sistema instalado em @, boot aponta apenas para o volume

> **Status: RESOLVIDO**: corrigido no commit `3e0b344` (segunda rodada, `NVG-04`), presente na `main` do `neovanguard-os-dev`. O NVG-OS-DEBUG marca esta cadeia como ❌ pendente, mas está errado: a correção já estava no código. Detalhes em [reconciliação](reconciliacao-2026-09-11.md).

Erro: **NVG-04**. Impacto: alto, primeiro boot comprometido. Verificação: inconsistência confirmada no código; consequência de boot inferida, sem VM.

## Solução aplicada

Em Btrfs novo ou com a raiz reformatada, a entrada do systemd-boot passa a levar `rootflags=subvol=@` (função `root_mount_option`, em `rust/nvg-installer/src/install.rs`), e o kernel monta a mesma `@` usada na instalação. Uma raiz Btrfs **mantida** não recebe a opção, porque o instalador não criou os subvolumes dela e não pode presumir sua estrutura.

Validação: o teste `btrfs_novo_seleciona_o_subvolume_raiz_no_boot` passou em 11/09/2026 na árvore reconciliada. Não houve boot em VM. [Registro da rodada](correcoes-02.md).

O texto abaixo registra o problema original; as linhas citadas são as do commit auditado.

## Walkthrough

1. Em uma instalação com Btrfs recém-formatado, `mount()` cria os subvolumes `@`, `@home` e outros: [rust/nvg-installer/src/install.rs:806](../../../rust/nvg-installer/src/install.rs:806).
2. A raiz de instalação é montada com `subvol=@`. Portanto, os arquivos do sistema são colocados nesse subvolume, não no nível superior.
3. Ao escolher systemd-boot em UEFI, `bootloader()` constrói `root=UUID=...`, ou a raiz do mapeador LUKS, mas não inclui a seleção do subvolume: [rust/nvg-installer/src/install.rs:1186](../../../rust/nvg-installer/src/install.rs:1186).
4. A entrada gravada usa exatamente essa linha: [rust/nvg-installer/src/install.rs:1256](../../../rust/nvg-installer/src/install.rs:1256). Não há alteração do subvolume padrão no fluxo examinado.
5. Assim, a seleção do volume não identifica a árvore que recebeu o sistema. Em um Btrfs novo, a montagem sem seleção usa o nível superior, de ID 5. Essa semântica consta da [documentação oficial do Btrfs](https://btrfs.readthedocs.io/en/stable/btrfs-subvolume.html).

## O erro

O contrato entre a montagem da instalação e a montagem inicial do boot perde o identificador de `@`. A consequência esperada é não encontrar a raiz utilizável do sistema e interromper o boot. Isso se aplica ao caminho systemd-boot com Btrfs novo; não é uma conclusão sobre todas as instalações nem sobre a geração automática do GRUB.

## Pontos de toque

- `format_fs → mount → cópia/pacstrap → bootloader`: o produtor coloca o sistema em uma árvore específica e o consumidor não a seleciona.
- [Cadeia 02](✅-02-preservacao-e-luks.md) toca as mesmas funções de particionamento e montagem, por outra causa.
- [Índice](README.md).
