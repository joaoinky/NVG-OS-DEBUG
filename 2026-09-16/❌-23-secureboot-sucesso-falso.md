# NVG-23 - Setup de Secure Boot anuncia cadeia assinada após falha

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-secureboot:86](../../../neo/bin/neo-secureboot#L86).

O ramo `setup` executa `"$0" sign` e ignora o código de saída. O script usa `set -uo pipefail`, sem interrupção automática por esse erro. Embora `sign` reconheça a falha de `sbctl sign`, o processo pai continua e imprime que as chaves foram inscritas e a cadeia assinada, retornando sucesso. Seguir essa indicação e ativar Secure Boot pode deixar componentes necessários sem assinatura.

## Evidência

Executou-se uma cópia do script completo com `/boot` e `/efi` redirecionados a temporários. `sbctl status` simulou Setup Mode e `sbctl sign` retornou 1. O filho informou erro de assinatura, mas `setup` terminou com código 0 e a mensagem de cadeia assinada. [Log](evidencias/probes-shell.log).

## Limites da conclusão

Nenhuma chave de firmware foi criada/inscrita; nenhuma configuração de Secure Boot foi alterada. O falso sucesso é confirmado. A recusa do boot depende das imagens e da política do firmware e precisa de OVMF/hardware.

## Direção da correção

Propagar falha de assinatura e verificar todos os componentes esperados antes da mensagem de sucesso. Testar também nenhum alvo encontrado, falha parcial e atualização de kernel.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
