# NVG-16 - A entrada Cold Vault perde parâmetros necessários para Btrfs e LUKS

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-install-vault-boot:29 e 45](../../../neo/bin/neo-install-vault-boot#L29).

O gerador lê a linha `options` do sistema instalado, extrai somente `root=...` e monta outra linha. Assim descarta `rootflags=subvol=@` e `cryptdevice=UUID=...:nvgroot`. A entrada normal corrigida pelo NVG-04 pode funcionar enquanto a nova entrada Vault deixa de selecionar a raiz correta ou de fornecer o mapeamento LUKS esperado pelo hook `encrypt`.

## Evidência

O script completo foi executado com `bootctl` simulado e ESP temporária, para modelos Btrfs simples e Btrfs/LUKS. Em ambos retornou sucesso; as opções geradas perderam `rootflags`, e no segundo caso também `cryptdevice`. [Log](evidencias/probes-shell.log), linhas “vault”.

## Limites da conclusão

A perda de parâmetros foi reproduzida. Não houve boot. O sintoma exato no initramfs e eventuais configurações alternativas de desbloqueio exigem VM. É um gerador diferente daquele corrigido no NVG-04; não reabre o defeito da entrada normal.

## Direção da correção

Preservar os parâmetros de armazenamento necessários da entrada válida e acrescentar somente as opções próprias do Vault. Testar boot normal e Vault com Btrfs, ext4 e LUKS.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
