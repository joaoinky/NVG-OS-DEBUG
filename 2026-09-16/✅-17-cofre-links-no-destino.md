# NVG-17 - Aplicação privilegiada do cofre segue links no home e no temporário

**Estado: corrigido e integrado à main em 18/09/2026; validação em ISO/VM pendente.** Gravidade original: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[pacote::aplicar](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/rust/nvg-nostr/src/pacote.rs#L324), [dono](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/rust/nvg-nostr/src/pacote.rs#L360) e [chamada privilegiada](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/rust/nvg-nostr/src/main.rs#L1285).

A validação da extração protege o conteúdo de origem, mas `aplicar()` confia no caminho de destino dentro do home. `create_dir_all`, `chown`, `set_permissions` e `copy` seguem links existentes. O temporário tem nome previsível (`kwinrc.nvg-tmp`) e não é criado com exclusividade/recusa de symlink. Um usuário ou processo que prepare esses links no home pode redirecionar a aplicação executada com sudo para outro local, incluindo alterações de conteúdo, dono e permissões com os privilégios do processo.

## Evidência

A prova `auditoria_aplicacao_do_cofre_segue_link_no_home` instala um pacote permitido com `.config/kwinrc`. Primeiro faz `.config` apontar a outro diretório; depois usa um `.config` normal e um temporário simbólico apontando a um arquivo sentinela. Nas duas variantes o arquivo fora do home foi sobrescrito pela função real. [Resultado](evidencias/rust-probes.log).

## Limites da conclusão

Tudo ocorreu como usuário comum e em diretórios descartáveis. Não foi escrito nenhum arquivo privilegiado real. A ampliação do impacto sob root decorre da mesma rotina e de `chown`; requer que o destino contenha links controlados antes da aplicação. Não depende de vencer uma corrida para reproduzir.

## Direção da correção

Ancorar operações em descritores de diretório, recusar symlinks em todos os componentes e criar temporários exclusivos sem seguir links. Evitar chown/chmod por caminhos controláveis. Testar também trocas concorrentes de diretórios.

## Correção e validação

Branch: `fix/NVG-17-cofre-links-destino`, baseada em `4d58b74`.
A evidência original abaixo descreve o comportamento anterior à correção.

`pacote::aplicar` usa agora [pacote_destino.rs](https://github.com/NEOpisa/neovanguard-os-dev/blob/093d7eb/rust/nvg-nostr/src/pacote_destino.rs):

- Abertura componente a componente com `openat`, `O_DIRECTORY` e `O_NOFOLLOW`,
  incluindo os ancestrais do home; caminhos relativos do manifesto não podem
  conter raiz nem `..` e continuam sujeitos à lista branca.
- Área temporária aleatória, criada exclusivamente com `mkdirat`, privada do
  aplicador (`0700`, dono conferido pelo descritor). O arquivo interno é aberto
  com `O_CREAT | O_EXCL | O_NOFOLLOW`. O temporário previsível não é mais usado.
- Conteúdo, permissões e dono são preparados por descritor, antes de publicar
  com `renameat2`. Diretórios faltantes também são preparados em privado e
  publicados sem substituir um concorrente (`RENAME_NOREPLACE`).
- Diretórios existentes não recebem chmod/chown. Um hardlink no destino é
  substituído, não escrito. Symlinks finais observados são recusados; se um
  aparecer depois da checagem, o rename substitui o link sem seguir seu alvo.

Validação executada em diretórios descartáveis:

```sh
cd rust
cargo test --offline -p nvg-nostr --lib pacote::
cargo test --offline -p nvg-nostr --test cofre_ponta_a_ponta
cargo test --offline -p nvg-nostr --lib -- --skip manifest::testes::aceleracao_so_com_a_gpu_certa
```

Os 16 testes de pacote passaram, incluindo oito regressões novas: componentes
simbólicos, hardlink, temporário preexistente, caminhos de fuga, modos/dono,
limpeza após erro, descritor cujo nome foi trocado e 500 tentativas durante
trocas concorrentes de diretório/symlink. As oito regressões também passaram
com UID 0 em namespace de usuário (`unshare --user --map-root-user`), exercitando
`fchown` sem conceder root no host. O teste ponta a ponta passou com as duas
reproduções originais usando a API real de aplicação.

A suíte de biblioteca passou com 63 testes e essa única exclusão.
O teste de GPU excluído já falhava na auditoria anterior: espera `nenhuma`, mas
recebe `cuda` ao consultar o hardware local. O teste de relay requer execução
fora da restrição de rede do sandbox; não foi alterado por esta correção.

Limites: não há transação de todos os arquivos, nem garantia de disponibilidade
contra um usuário que renomeie seus diretórios durante a aplicação. Descritores
permanecem ligados ao diretório original, mesmo renomeado; uma área temporária
renomeada pode sobrar vazia. Testes no sistema instalado, com sudo e usuários
distintos, continuam pendentes. Não se ampliou esta mudança para outros fluxos
de restauração nem para a validação da origem protegida pelo cofre.

Semântica das chamadas: [openat e descritores de diretório](https://man7.org/linux/man-pages/man2/open.2.html)
e [renameat2](https://www.man7.org/linux/man-pages/man2/rename.2.html).

Implementação: [`093d7eb`](https://github.com/NEOpisa/neovanguard-os-dev/commit/093d7eb) · [PR #8 - integrado](https://github.com/NEOpisa/neovanguard-os-dev/pull/8). Consulte o [registro da rodada](correcoes-2026-09-18.md) para os commits de merge e as pendências.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
