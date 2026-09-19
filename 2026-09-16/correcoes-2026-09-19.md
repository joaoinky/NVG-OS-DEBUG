# Correções de 19/09/2026 - NVG-31 e NVG-20

As duas correções foram implementadas juntas porque pertencem ao mesmo fluxo:
a CLI precisa preservar as referências do pedido de exclusão e o comando de
limpeza precisa publicar o evento assinado. O trabalho está no
[PR #31](https://github.com/NEOpisa/neovanguard-os-dev/pull/31), ainda aberto.

## Publicação

| Problemas | Branch | Commit | PR | Estado |
|---|---|---|---|---|
| NVG-31 e NVG-20 | `fix/NVG-31-NVG-20-exclusao-dms` | [`1c2d7b4`](https://github.com/NEOpisa/neovanguard-os-dev/commit/1c2d7b4) | [#31](https://github.com/NEOpisa/neovanguard-os-dev/pull/31) | Aberto |

## NVG-31 - tags preservadas na assinatura

`nvg-nostr agente assinar` passou a aceitar `--tag NOME=VALOR` mais de uma
vez, mantendo ordem e conteúdo. A CLI rejeita opções desconhecidas, valores
ausentes, nomes de tag inválidos e opções únicas repetidas antes de abrir o
socket do agente. Os padrões anteriores de kind e conteúdo foram preservados.

Além dos casos de parsing, o agente assina um evento kind 5 com referências
`e` e `k`, e a regressão verifica tanto as tags quanto a assinatura final.

[Relatório atualizado](✅-31-assinatura-descarta-tags.md).

## NVG-20 - publicação e confirmação da limpeza

`neo-clean-dms` consulta a chave pública do agente e seleciona somente eventos
que essa identidade pode solicitar que sejam excluídos: kind 4 de sua autoria
e envelopes kind 1059 que a identificam na tag `p`. O usuário confirma a lista
antes das assinaturas.

Cada resposta do agente é validada antes da publicação. O RPC só considera
sucesso quando recebe `OK` positivo com o ID exato do evento enviado. Consulta
incompleta, recusa, ausência de resposta e falha parcial produzem código de
saída diferente de zero. A mesma lista deduplicada sustenta contagem,
confirmação e processamento.

[Relatório atualizado](✅-20-limpeza-dms-nao-publica.md).

## Validação

- Formatação e Clippy passaram.
- A integração de limpeza aprovou 16 cenários.
- A integração do RPC aprovou 12 cenários.
- As suítes `nvg-nostr` e `nvg-nostr-agent` passaram ao excluir somente o teste
  de GPU já documentado no NVG-28.
- `./check quick` executou as demais etapas e permaneceu vermelho apenas pela
  falha preexistente do NVG-28 no host NVIDIA.

Os testes cobrem tags repetidas, Unicode, valores vazios, seleção por autoria e
destinatário, duplicatas, cancelamento, recusa do agente, assinatura inválida,
troca de identidade, EOSE ausente, relay indisponível e respostas `OK`
negativas, ausentes ou vinculadas a outro ID. Foram usadas chaves descartáveis;
nenhuma identidade ou DM pessoal participou da execução.

## Limites e pendências

- O PR continua aberto e ainda não está integrado à `main`.
- Não foi construída nem inicializada uma ISO nesta rodada.
- Os prompts do agente e os binários empacotados precisam de teste em ISO/VM.
- O relay empacotado precisa ser testado com kind 4 e kind 1059, inclusive a
  regra de exclusão pelo destinatário definida na NIP-59.
- Uma resposta `OK` confirma aceitação do pedido, não apagamento físico nem
  remoção de cópias externas.

[Índice da auditoria](README.md) · [Matriz de validação](pendencias-iso-vm-hardware.md)
