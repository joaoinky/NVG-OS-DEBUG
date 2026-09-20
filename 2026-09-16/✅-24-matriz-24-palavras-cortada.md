# NVG-24 - Matriz de aço para 24 palavras ultrapassa a página

**Estado: corrigido no código em 20/09/2026; PR #36 aberto; validação no sistema instalado pendente.** Gravidade original: **média** no cenário descrito. Base da auditoria: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-paper:72](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/neo-paper#L72).

A matriz começa em y=75 mm, dispõe duas palavras por linha e reduz y em 9 mm a cada par. Para 24 palavras há 12 linhas; as linhas das palavras 19 a 24 ficam abaixo de y=0. As 24 células correspondentes saem inteiramente da página A4, embora o gerador termine com sucesso.

## Evidência

O script foi executado com `--palavras 24`; somente `ps2pdf` foi substituído por uma cópia do PostScript para inspeção. Das 96 células geradas, 24 satisfazem `y + altura < 0`. [Log](evidencias/probes-shell.log).

## Limites da conclusão

O formulário não recebeu seed. A lista principal das 24 palavras não foi demonstrada como ausente: o defeito confirmado é na matriz para transferência ao aço. Não houve impressão física.

## Direção da correção

Recalcular dimensões por quantidade de palavras ou paginar. Conferir limites de todos os retângulos e renderizar PDFs de 12 e 24 palavras antes de validar impressão.

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
