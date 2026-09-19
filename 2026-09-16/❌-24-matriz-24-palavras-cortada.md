# NVG-24 - Matriz de aço para 24 palavras ultrapassa a página

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **média** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-paper:72](../../../neo/bin/neo-paper#L72).

A matriz começa em y=75 mm, dispõe duas palavras por linha e reduz y em 9 mm a cada par. Para 24 palavras há 12 linhas; as linhas das palavras 19 a 24 ficam abaixo de y=0. As 24 células correspondentes saem inteiramente da página A4, embora o gerador termine com sucesso.

## Evidência

O script foi executado com `--palavras 24`; somente `ps2pdf` foi substituído por uma cópia do PostScript para inspeção. Das 96 células geradas, 24 satisfazem `y + altura < 0`. [Log](evidencias/probes-shell.log).

## Limites da conclusão

O formulário não recebeu seed. A lista principal das 24 palavras não foi demonstrada como ausente: o defeito confirmado é na matriz para transferência ao aço. Não houve impressão física.

## Direção da correção

Recalcular dimensões por quantidade de palavras ou paginar. Conferir limites de todos os retângulos e renderizar PDFs de 12 e 24 palavras antes de validar impressão.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
