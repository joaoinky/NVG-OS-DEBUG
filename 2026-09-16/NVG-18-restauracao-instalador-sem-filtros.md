# NVG-18 — Restauração do instalador ignora a lista de arquivos permitidos

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[preparar_conta_nostr](../../../rust/nvg-installer/src/main.rs#L671), [conta_nostr](../../../rust/nvg-installer/src/install.rs#L1238), [configs::desempacotar](../../../rust/nvg-nostr/src/configs.rs#L388) e [pacote::instalar](../../../rust/nvg-nostr/src/pacote.rs#L235).

O instalador baixa/decifra o pacote e o entrega diretamente a `configs::desempacotar`. Essa função chama tar no home, sem passar pela lista de caminhos permitidos e pela validação de extração de `pacote::instalar`. Portanto as garantias do fluxo do cofre não se aplicam à restauração durante a instalação. O comando também usa `--keep-directory-symlink`, que segue diretórios simbólicos preexistentes, e não impõe nessa função o limite de saída descomprimida do extrator validado.

## Evidência

A prova `auditoria_instalador_extrai_arquivo_fora_da_lista` cria um tar.zst contendo `.ssh/authorized_keys` com texto fictício. Confirma que `pacote::na_lista()` o recusa, mas a função real usada pelo instalador o grava. [Resultado](evidencias/rust-probes.log). A semântica do argumento de symlink está no [manual GNU tar](https://www.gnu.org/software/tar/manual/html_node/Option-Summary.html).

## Limites da conclusão

Não foi criado acesso SSH utilizável. O teste confirma o desvio da lista; não executa bomba de descompressão. A criptografia/autoria do pacote continuam sendo barreiras: o cenário exige um pacote decifrável aceito pelo fluxo, por exemplo backup previamente produzido/comprometido. Não se afirma que qualquer atacante possa forjar NIP-44.

## Direção da correção

Unificar a restauração com a extração validada, aplicando limites antes e durante a descompressão e política de arquivos antes de escrever no home. Depois aplicar com a proteção de destino descrita no NVG-17.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
