# NVG-15 - O instalador aceita root como nova conta e falha depois da formatação

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[validate_account](../../../rust/nvg-installer/src/install.rs#L97), [run_all](../../../rust/nvg-installer/src/install.rs#L401) e [accounts](../../../rust/nvg-installer/src/install.rs#L1157).

A validação aceita nomes sintaticamente corretos que já pertencem ao sistema, como `root`. A conta só é criada na etapa de 74%, depois de preparar/formatar disco, copiar o sistema e configurar o alvo. `useradd` recusa uma conta existente e interrompe a instalação. O nome reservado pode ser rejeitado antes de qualquer operação destrutiva.

## Evidência

A prova Rust `contas_reservadas_passam_no_preflight` aceita `root` e `daemon` nas duas validações. Separadamente, o `useradd` real recebeu `--prefix` com passwd/group/shadow fictícios: `root` foi recusado com código **9**, por já existir. [Rust](evidencias/rust-probes.log) e [useradd](evidencias/probe-conta-reservada.log).

## Limites da conclusão

Nenhuma conta da máquina foi alterada. O caso conclusivo é `root`, que necessariamente existe no sistema alvo. Não se afirma que nomes longos sejam rejeitados: essa hipótese foi descartada ao conferir o useradd disponível.

## Direção da correção

Recusar nomes reservados e conflitos com as contas do payload/base antes de particionar. Distinguir criação de conta de uma eventual operação explícita de reutilização de conta existente.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
