# NVG-21 - Flash e transportes mesh perdem a ação ao executar sudo

**Estado: corrigido no código em 20/09/2026; PR #33 aberto; validação no sistema instalado pendente.** Gravidade original: **média** no cenário descrito. Base da auditoria: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[need_root](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/_neo-comum.sh#L56), [cmd_seedsigner](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/neo-flash#L179) e [dispatch do mesh](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/neo-mesh#L162).

`need_root` relança `sudo -E "$0" "$@"`. Em `neo-flash seedsigner`, o dispatcher já consumiu o subcomando e o parser consome destino/modelo antes dessa chamada: a elevação recebe zero argumentos e relança a listagem padrão. Em `neo-mesh --bluetooth` e `--wifi-direct`, o dispatcher também remove o seletor; o processo elevado segue para a ação padrão de anúncio/procura. A ação originalmente pedida não é preservada.

## Evidência

Foram extraídas as funções reais e substituída somente a elevação por um registrador. Flash com destino/modelo recebeu `argumentos_na_elevacao=0`; Bluetooth PAN e Wi-Fi Direct também perderam seu seletor. [Log](evidencias/probes-shell.log).

## Limites da conclusão

Nenhum dispositivo foi gravado e nenhum rádio foi ligado. O problema se manifesta quando é necessário elevar privilégios; uma execução já iniciada com sudo evita esse caminho. Krux não foi incluído no diagnóstico sem uma prova equivalente.

## Direção da correção

Elevar antes de consumir argumentos ou guardar a linha original completa. Cobrir a execução normal e a relançada com cada subcomando e parâmetros.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)

## Correção implementada em 20/09

[PR #33](https://github.com/NEOpisa/neovanguard-os-dev/pull/33), branch `fix/neo-comum-shared-lib`.
Commits de implementação: [`57ef2d2`](https://github.com/NEOpisa/neovanguard-os-dev/commit/57ef2d2), [`a2cb329`](https://github.com/NEOpisa/neovanguard-os-dev/commit/a2cb329).

A elevação com sudo perdia subcomandos já consumidos pelo parser, e o perfil gravado pelo assistente era lido de outro arquivo. A biblioteca preserva os argumentos originais e lê `profile.conf/profile=`, com compatibilidade para `perfil.conf/perfil=`. O formato atual tem precedência; configuração inválida usa `cold` com aviso.

## Validação e limites

57 testes aprovados: biblioteca compartilhada (7), modos de rede (18), estado de rede (17), MAC (8) e dependências de build (7). Sintaxe shell, referências de ajuda dos 56 comandos e `git diff --check` aprovados. Os testes exercitam relançamento de Flash/mesh, limites dos argumentos, persistência do assistente e SOCKS no `neo_curl`.

Não foi executado o assistente completo com sudo, nem gravação de firmware ou transportes mesh reais. NVG-25, sobre o menu capturado na resposta, permanece pendente. `./check quick` completo não foi repetido nesta branch.

As provas originais acima registram o comportamento anterior à correção. O PR ainda não foi integrado à `main`.

[Registro dos cinco grupos](correcoes-2026-09-20.md) · [PR #33](https://github.com/NEOpisa/neovanguard-os-dev/pull/33)
