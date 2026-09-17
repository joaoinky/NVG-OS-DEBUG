# NVG-17 — Aplicação privilegiada do cofre segue links no home e no temporário

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[pacote::aplicar](../../../rust/nvg-nostr/src/pacote.rs#L324), [dono](../../../rust/nvg-nostr/src/pacote.rs#L360) e [chamada privilegiada](../../../rust/nvg-nostr/src/main.rs#L1285).

A validação da extração protege o conteúdo de origem, mas `aplicar()` confia no caminho de destino dentro do home. `create_dir_all`, `chown`, `set_permissions` e `copy` seguem links existentes. O temporário tem nome previsível (`kwinrc.nvg-tmp`) e não é criado com exclusividade/recusa de symlink. Um usuário ou processo que prepare esses links no home pode redirecionar a aplicação executada com sudo para outro local, incluindo alterações de conteúdo, dono e permissões com os privilégios do processo.

## Evidência

A prova `auditoria_aplicacao_do_cofre_segue_link_no_home` instala um pacote permitido com `.config/kwinrc`. Primeiro faz `.config` apontar a outro diretório; depois usa um `.config` normal e um temporário simbólico apontando a um arquivo sentinela. Nas duas variantes o arquivo fora do home foi sobrescrito pela função real. [Resultado](evidencias/rust-probes.log).

## Limites da conclusão

Tudo ocorreu como usuário comum e em diretórios descartáveis. Não foi escrito nenhum arquivo privilegiado real. A ampliação do impacto sob root decorre da mesma rotina e de `chown`; requer que o destino contenha links controlados antes da aplicação. Não depende de vencer uma corrida para reproduzir.

## Direção da correção

Ancorar operações em descritores de diretório, recusar symlinks em todos os componentes e criar temporários exclusivos sem seguir links. Evitar chown/chmod por caminhos controláveis. Testar também trocas concorrentes de diretórios.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
