# NVG-25 — Primeiro boot captura o menu junto com a resposta

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[pergunta](../../../neo/wizard/neo-first-boot#L21) e [atribuições/aplicação](../../../neo/wizard/neo-first-boot#L84).

`pergunta()` escreve título, opções, prompt e chave escolhida em stdout. Seus chamadores usam `VAR="$(pergunta ...)"`, capturando tudo na variável. O menu deixa de aparecer durante a leitura e valores como PERFIL, NO, IDENT e REDE não correspondem às chaves dos `if`/`case`. Selecionar Cold não satisfaz `PERFIL == cold`; suas decisões de isolamento não são aplicadas. O assistente ainda pode gravar a configuração e marcar a execução como concluída.

## Evidência

A função original recebeu a resposta `2` para Hot/Cold. A variável resultante terminou em `cold`, mas continha todo o menu; a comparação com `cold` retornou falso. O mesmo contrato de saída é usado nas quatro perguntas. [Log](evidencias/probes-shell.log).

## Limites da conclusão

Não se executou o assistente inteiro com sudo. O contrato de entrada/saída e a impossibilidade de corresponder às chaves são reproduzidos. A condição final de rede depende do estado anterior e dos comandos comuns do assistente; não se presume isolamento efetivo.

## Direção da correção

Enviar interface/prompt ao terminal ou stderr e reservar stdout para a resposta. Validar enumerações antes de gravar/aplicar e só registrar conclusão após confirmar os resultados escolhidos.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
