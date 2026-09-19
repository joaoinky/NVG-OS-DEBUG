# NVG-30 — Zap não compara o valor da fatura com os sats solicitados

**Estado: corrigido e integrado à main em 18/09/2026; validação em ISO/VM pendente.** Gravidade original: **alta** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-zap:73](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/neo-zap#L73).

O comando valida os limites anunciados pelo LNURL e solicita `amount`, mas aceita o campo `pr` da resposta sem decodificar seu valor. Em seguida chama `lightning-cli pay <fatura>` ou `lncli payinvoice --force <fatura>`. O nó recebe a fatura, sem receber o limite de sats informado pelo usuário. Um destinatário/servidor LNURL desonesto pode emitir uma fatura maior que a solicitação.

## Evidência

O script completo pediu 1000 sats a um endpoint simulado. A resposta trouxe o vetor público BOLT11 de 2500 microBTC, equivalente a 250000 sats. A chamada registrada foi diretamente `lightning-cli pay <essa fatura>`, sem decodificação ou comparação. [Log](evidencias/probes-nostr-payment.log). O [LUD-06, fluxo LNURL-pay](https://github.com/lnurl/luds/blob/luds/06.md) exige conferir o valor; o vetor está no [BOLT11](https://github.com/lightning/bolts/blob/master/11-payment-encoding.md#examples).

## Limites da conclusão

O pagador foi substituído por um registrador; nenhum satoshi saiu. O vetor de teste está expirado e não demonstra liquidação real. Demonstra que o valor divergente atravessa a fronteira de autorização sem verificação; uma fatura atual válida pode usar o mesmo caminho. Não se trata da opção de pagar uma fatura direta, em que o próprio usuário fornece a fatura.

## Direção da correção

Decodificar/verificar BOLT11 e exigir igualdade exata em millisatoshis, além dos demais vínculos LNURL, antes de chamar o pagador. Rejeitar divergência e resposta inválida. Validar com nó regtest e fundos fictícios.

## Correção — 2026-09-18

`neo-zap` agora decodifica a mesma fatura que será enviada ao pagador com
`lightning-cli decode` ou `lncli decodepayreq`, fixando o backend entre as duas
operações. No CLN exige `valid: true` e `type: "bolt11 invoice"`; no LND exige
sucesso do RPC. A verificação BOLT11 e de assinatura fica a cargo do nó.
As chamadas CLN usam `-N none -J` para não misturar notificações de progresso
ao JSON consumido pelo helper/jq.

O novo helper `neo-lnurl-verify`, instalado pelo empacotamento existente dos
comandos `neo-*`, exige igualdade exata em millisatoshis, `description_hash`
igual ao SHA-256 dos bytes UTF-8 originais de `metadata` e fatura não expirada.
Fatura sem valor, resposta malformada, erro do serviço, erro de decodificação
ou ausência do helper abortam antes do pagador. A comparação usa inteiros
Python; não usa `num_satoshis` do LND, que trunca frações de satoshi, nem
aritmética shell/JSON de ponto flutuante.

Também valida `tag`, metadados e limites LNURL sem truncar msat, preserva
parâmetros existentes no callback com `curl -G --data-urlencode` e recusa
callbacks inseguros ou com parâmetros de pagamento duplicados. O fluxo de
fatura direta fornecida pelo usuário continua separado. A igualdade autoriza
o valor da fatura; taxas de roteamento continuam sob a política do nó.

Referências das interfaces utilizadas:
[CLN decode](https://docs.corelightning.org/reference/decode) e
[LND DecodePayReq](https://api.lightning.community/api/lnd/lightning/decode-pay-req/index.html).

## Regressão automatizada

```sh
python3 scripts/test-neo-zap.py
```

São 13 testes, com subcasos para CLN e LND, executando o shell e helper reais
com HTTP e nó simulados. Verificam que não há chamada ao pagador nos casos
inválidos, incluindo 250000 sats para pedido de 1000, diferença de um msat,
ausência de valor/hash, expiração, JSON inválido, limites fracionários em sats,
overflow, valores acima da precisão de float, falha de transporte/decodificador
e ausência do helper. Os casos válidos verificam a ordem decodificar → pagar.
A suíte integra `./check quick`. Passaram também `check-neo-cli.py`, `bash -n`
dos arquivos shell alterados e `git diff --check`.

Teste adicional com nós reais isolados, fora do check rápido:

```sh
python3 scripts/test-neo-zap-regtest.py \
  --bitcoin-bin /caminho/bitcoin/bin --cln-bin /caminho/cln/bin
```

O script cria uma rede Bitcoin regtest, duas carteiras CLN novas e um canal
financiado com moedas fictícias. Só a resposta HTTP LNURL é simulada. Os
processos são encerrados e os dados temporários removidos ao sair. Não usa
carteiras existentes nem instala dependências.

Executado com Bitcoin Core 29.0 e Core Lightning 26.06.7, em 2026-09-18:

```text
Canal regtest confirmado; apenas fundos fictícios.
maior: unpaid; comportamento esperado confirmado.
um-msat: unpaid; comportamento esperado confirmado.
hash-errado: unpaid; comportamento esperado confirmado.
correta: paid; comportamento esperado confirmado.
```

Cada caso solicitou 1000 sats. O teste conferiu tanto a ausência/presença de
chamada `pay` quanto o estado da fatura no nó recebedor. O caso correto
liquidou 1000000 msat. Os três casos recusados usaram, respectivamente,
250000000 msat, 1000001 msat e hash de metadados divergente. LND foi coberto
pelos testes simulados; liquidação real com LND e validação em ISO continuam
pendentes. Nenhum fundo de mainnet/testnet foi utilizado.

Implementação: [`f9bffa5`](https://github.com/NEOpisa/neovanguard-os-dev/commit/f9bffa5) · [PR #10 — integrado](https://github.com/NEOpisa/neovanguard-os-dev/pull/10). Consulte o [registro da rodada](correcoes-2026-09-18.md) para os commits de merge e as pendências.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
