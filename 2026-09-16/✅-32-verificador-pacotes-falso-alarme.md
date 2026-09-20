# NVG-32 - Verificador anuncia pacote inexistente por conflito do host

**Estado: corrigido no código em 20/09/2026; PR #36 aberto; validação no sistema instalado pendente.** Gravidade original: **baixa** no cenário descrito. Base da auditoria: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[resolves em check-neo-refs.py](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/scripts/check-neo-refs.py#L113).

O verificador usa `pacman -Sp <pacote>` para decidir se um nome existe no repositório. Esse comando também resolve a transação contra os pacotes instalados no host. Um conflito de versões/dependências faz a consulta falhar, e o código traduz qualquer falha em “package does not exist in the repositories”. Assim uma árvore correta pode falhar na validação por estado particular do computador.

## Evidência

Neste host, `pacman -Si systemd` retornou 0. `pacman -Sp systemd` retornou 1 porque systemd 261.3-1 da base sincronizada conflita com systemd-sysvcompat que exige 261.2. `check-neo-refs.py` então acusou `need bootctl systemd` como pacote inexistente. [Prova e saídas](evidencias/probe-referencia-pacman.log). Não se instalou/atualizou nada.

## Limites da conclusão

Essa reprodução depende do estado de pacotes do host, registrado no log. Não afirma que a ISO possui dependências quebradas ou que o pacote systemd sumiu. É uma falha de diagnóstico e de isolamento do verificador; em container sincronizado pode não ocorrer.

## Direção da correção

Consultar existência pelo índice de pacotes, separando isso da verificação de resolubilidade de uma transação. Quando houver erro de dependência, preservar a causa e apontar que ela pertence ao ambiente de validação.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)

## Correção implementada em 20/09

[PR #36](https://github.com/NEOpisa/neovanguard-os-dev/pull/36), branch `fix/quick-fixes-paper-pkgcheck`.
Commits de implementação: [`058ebdb`](https://github.com/NEOpisa/neovanguard-os-dev/commit/058ebdb), [`c44f913`](https://github.com/NEOpisa/neovanguard-os-dev/commit/c44f913).

A matriz de 24 palavras ultrapassava a folha, e conflitos de pacotes instalados eram reportados como pacote inexistente. O formulário distribui a matriz em quatro colunas, mantém células de 7 x 6 mm e define A4 explicitamente. O verificador lê o índice com `pacman -Slq`, sem resolver transação, e diferencia ausência de pacote de erro de leitura do índice.

## Validação e limites

Teste de geometria e geração de PDF aprovado para 12 e 24 palavras; ambos renderizados e inspecionados visualmente, com uma página A4. Três testes do verificador de pacotes aprovados, incluindo conflito do host, erro de índice e timeout. Referências e ajuda dos 56 comandos, sintaxe shell e `git diff --check` aprovados.

Não houve impressão física nem construção de ISO/pacotes. `./check quick` completo não foi repetido nesta branch.

As provas originais acima registram o comportamento anterior à correção. O PR ainda não foi integrado à `main`.

[Registro dos cinco grupos](correcoes-2026-09-20.md) · [PR #36](https://github.com/NEOpisa/neovanguard-os-dev/pull/36)
