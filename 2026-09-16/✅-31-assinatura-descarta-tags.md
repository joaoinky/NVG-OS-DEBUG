# NVG-31 - CLI de assinatura ignora --tag e envia um evento sem referências

**Estado: corrigido no código em 19/09/2026; PR #31 aberto; validação em ISO pendente.** Gravidade original: **média**. Base da auditoria: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação). A evidência abaixo descreve o comportamento anterior à correção.

## Onde e como acontece

[agente_assinar](../../../rust/nvg-nostr/src/main.rs#L1536) e [chamador neo-clean-dms](../../../neo/bin/neo-clean-dms#L39).

A CLI lê apenas `--kind` e `--conteudo`; a requisição IPC sempre usa `"tags": []`. Argumentos `--tag e=<id>` são silenciosamente ignorados. O chamador existente de limpeza precisa dessa referência para indicar qual evento excluir. Mesmo após corrigir a publicação do NVG-20, o pedido de exclusão continuará sem alvo.

## Evidência

O binário real `nvg-nostr` foi conectado a um socket Unix temporário que apenas registra o pedido e responde sucesso fictício. Executou-se `agente assinar --kind 5 --conteudo teste --tag e=<id>`. A CLI retornou sucesso e o servidor recebeu `tags=[]`. [Prova](evidencias/reproduzir-tags-cli.py) e [log](evidencias/probe-tags-cli.log).

## Limites da conclusão

Nenhum agente real foi destravado e nenhum evento foi assinado com chave pessoal. A perda do argumento foi observada no IPC, antes de qualquer assinatura. O achado não significa que todas as outras APIs de assinatura percam tags.

## Direção da correção

Implementar o formato de tags que os chamadores usam, validar/rejeitar argumentos desconhecidos e testar a requisição IPC resultante. Depois testar a integração de exclusão separadamente.

## Correção implementada

O [PR #31](https://github.com/NEOpisa/neovanguard-os-dev/pull/31), commit
[`1c2d7b4`](https://github.com/NEOpisa/neovanguard-os-dev/commit/1c2d7b4),
adiciona `--tag NOME=VALOR` repetível a `nvg-nostr agente assinar`. A ordem é
preservada e somente o primeiro `=` separa nome e valor. Nomes vazios ou com
espaços e controles, opções desconhecidas, valores ausentes e repetição de
`--kind` ou `--conteudo` são recusados antes do IPC.

O agente ganhou uma regressão que assina um kind 5 com duas referências `e` e
uma tag `k`, preserva todas elas e valida a assinatura final. A integração da
limpeza exercita a CLI real contra um socket Unix temporário, incluindo tags
repetidas, Unicode, valor vazio e argumentos inválidos.

Os testes específicos e as suítes `nvg-nostr` e `nvg-nostr-agent` passaram,
excluindo apenas a falha preexistente de GPU registrada no NVG-28. Ainda falta
validar o binário empacotado e os prompts do agente em uma ISO.

[Registro da correção conjunta](correcoes-2026-09-19.md) · [PR #31](https://github.com/NEOpisa/neovanguard-os-dev/pull/31)

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
