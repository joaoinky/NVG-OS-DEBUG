# NVG-31 — CLI de assinatura ignora --tag e envia um evento sem referências

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **média** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[agente_assinar](../../../rust/nvg-nostr/src/main.rs#L1536) e [chamador neo-clean-dms](../../../neo/bin/neo-clean-dms#L39).

A CLI lê apenas `--kind` e `--conteudo`; a requisição IPC sempre usa `"tags": []`. Argumentos `--tag e=<id>` são silenciosamente ignorados. O chamador existente de limpeza precisa dessa referência para indicar qual evento excluir. Mesmo após corrigir a publicação do NVG-20, o pedido de exclusão continuará sem alvo.

## Evidência

O binário real `nvg-nostr` foi conectado a um socket Unix temporário que apenas registra o pedido e responde sucesso fictício. Executou-se `agente assinar --kind 5 --conteudo teste --tag e=<id>`. A CLI retornou sucesso e o servidor recebeu `tags=[]`. [Prova](evidencias/reproduzir-tags-cli.py) e [log](evidencias/probe-tags-cli.log).

## Limites da conclusão

Nenhum agente real foi destravado e nenhum evento foi assinado com chave pessoal. A perda do argumento foi observada no IPC, antes de qualquer assinatura. O achado não significa que todas as outras APIs de assinatura percam tags.

## Direção da correção

Implementar o formato de tags que os chamadores usam, validar/rejeitar argumentos desconhecidos e testar a requisição IPC resultante. Depois testar a integração de exclusão separadamente.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
