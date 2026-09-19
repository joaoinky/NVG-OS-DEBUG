# NVG-32 - Verificador anuncia pacote inexistente por conflito do host

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **baixa** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[resolves em check-neo-refs.py](../../../scripts/check-neo-refs.py#L113).

O verificador usa `pacman -Sp <pacote>` para decidir se um nome existe no repositório. Esse comando também resolve a transação contra os pacotes instalados no host. Um conflito de versões/dependências faz a consulta falhar, e o código traduz qualquer falha em “package does not exist in the repositories”. Assim uma árvore correta pode falhar na validação por estado particular do computador.

## Evidência

Neste host, `pacman -Si systemd` retornou 0. `pacman -Sp systemd` retornou 1 porque systemd 261.3-1 da base sincronizada conflita com systemd-sysvcompat que exige 261.2. `check-neo-refs.py` então acusou `need bootctl systemd` como pacote inexistente. [Prova e saídas](evidencias/probe-referencia-pacman.log). Não se instalou/atualizou nada.

## Limites da conclusão

Essa reprodução depende do estado de pacotes do host, registrado no log. Não afirma que a ISO possui dependências quebradas ou que o pacote systemd sumiu. É uma falha de diagnóstico e de isolamento do verificador; em container sincronizado pode não ocorrer.

## Direção da correção

Consultar existência pelo índice de pacotes, separando isso da verificação de resolubilidade de uma transação. Quando houver erro de dependência, preservar a causa e apontar que ela pertence ao ambiente de validação.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
