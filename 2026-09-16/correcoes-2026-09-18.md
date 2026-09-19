# Correções de 18/09/2026 — NVG-29, NVG-30 e NVG-17

As três correções foram implementadas em branches independentes de
`NEOpisa/neovanguard-os-dev`, a partir de `4d58b74`, e publicadas em pull
requests separados. Os três PRs estão integrados à `main`.

Este registro reúne o trabalho realizado depois da auditoria de 16/09.
Os relatórios e logs originais foram preservados: eles mostram os defeitos
antes das correções, não o comportamento do código atualizado.

## Publicação

| Problema | Branch | Commit da correção | PR | Merge na main |
|---|---|---|---|---|
| NVG-29 | `fix/NVG-29-validar-eventos-nostr` | [`1917f0d`](https://github.com/NEOpisa/neovanguard-os-dev/commit/1917f0d) | [#9](https://github.com/NEOpisa/neovanguard-os-dev/pull/9) | [`f249e84`](https://github.com/NEOpisa/neovanguard-os-dev/commit/f249e84896f491a770862b8e492f7ecd82550adf) |
| NVG-30 | `fix/NVG-30-validar-fatura-lnurl` | [`f9bffa5`](https://github.com/NEOpisa/neovanguard-os-dev/commit/f9bffa5) | [#10](https://github.com/NEOpisa/neovanguard-os-dev/pull/10) | [`c56d0d7`](https://github.com/NEOpisa/neovanguard-os-dev/commit/c56d0d748900536ff68c1475c174baa743699fcd) |
| NVG-17 | `fix/NVG-17-cofre-links-destino` | [`093d7eb`](https://github.com/NEOpisa/neovanguard-os-dev/commit/093d7eb) | [#8](https://github.com/NEOpisa/neovanguard-os-dev/pull/8) | [`fe92b39`](https://github.com/NEOpisa/neovanguard-os-dev/commit/fe92b39c7e4c2ae1328cad3c1f6ae95cd0a06c4c) |

Os merges foram conferidos no GitHub. Seus horários são de 19/09 em UTC,
correspondentes à noite de 18/09 no fuso America/Bahia (UTC−3).
Os resultados abaixo pertencem às respectivas branches; não representam
uma nova execução conjunta sobre a main após os merges.

## NVG-29 — autenticidade dos eventos Nostr

O helper Python passou a verificar os eventos antes de ordená-los ou remover
duplicatas. O comando `nvg-nostr eventos-verificar` usa o SDK já adotado pelo
projeto para conferir estrutura, hash, assinatura e filtro da consulta.
Mensagens de outra inscrição são ignoradas. Se o verificador faltar ou falhar,
a consulta termina sem devolver conteúdo não verificado.

A integração Rust/Python passou com nove cenários de regressão. A suíte do
pacote teve 55 testes unitários e duas integrações aprovados, com a exclusão
do teste de GPU já afetado pela NVG-28. Formatação, Clippy e verificação da
interface dos comandos também passaram. A checagem de referências reproduziu
o falso alarme de `systemd` documentado na NVG-32.

[Relatório e detalhes da validação](NVG-29-rpc-aceita-evento-forjado.md).

## NVG-30 — valor e vínculo da fatura LNURL

`neo-zap` agora decodifica a fatura no nó antes de pagar. O novo helper
`neo-lnurl-verify` exige valor exato em millisatoshis, hash dos metadados
originais e prazo de validade vigente. Respostas inválidas ou falhas na
verificação impedem o pagamento. A correção também trata limites LNURL e
parâmetros do callback; o fluxo de fatura direta continua separado.

Os 13 testes automatizados passaram com cenários para CLN e LND. Em regtest,
Bitcoin Core 29.0 e dois nós Core Lightning 26.06.7 confirmaram que faturas
com valor maior, diferença de um millisatoshi ou hash incorreto ficaram sem
pagamento. A fatura correta de 1000 sats foi liquidada. Só foram usados
fundos fictícios; a resposta HTTP LNURL permaneceu simulada.

[Relatório, comandos e resultado do regtest](NVG-30-zap-nao-confere-valor.md).

## NVG-17 — aplicação do cofre sem seguir links

A escrita no home passou a usar descritores de diretório, com recusa de
links nos componentes do caminho. Arquivos e diretórios novos são preparados
em uma área privada e publicados por rename. O temporário previsível foi
removido e diretórios existentes conservam dono e permissões.

Passaram 16 testes de pacote e o teste ponta a ponta. As oito regressões
novas também passaram com UID 0 em namespace isolado, exercitando `fchown`
sem privilégios de root sobre o host. O teste de troca concorrente de
diretório por link foi repetido 20 vezes, com 500 tentativas por execução.
A biblioteca teve 63 testes aprovados, excluindo apenas o caso de GPU da
NVG-28. Clippy terminou sem avisos.

[Relatório, comportamento e limites](NVG-17-cofre-links-no-destino.md).

## Reprodução dos testes

Executar no checkout de `neovanguard-os-dev`, no commit correspondente da
tabela. Este repositório de auditoria não contém os fontes nem os novos testes.

```sh
# NVG-29: inclui os nove casos Python
cd rust
cargo test --locked -p nvg-nostr --test rpc_eventos
```

```sh
# NVG-30: a partir da raiz do código-fonte
python3 scripts/test-neo-zap.py
python3 scripts/test-neo-zap-regtest.py \
  --bitcoin-bin /caminho/bitcoin/bin --cln-bin /caminho/cln/bin
```

```sh
# NVG-17: a partir de rust/
cargo test --offline -p nvg-nostr --lib pacote::
cargo test --offline -p nvg-nostr --test cofre_ponta_a_ponta
cargo test --offline -p nvg-nostr --lib -- --skip manifest::testes::aceleracao_so_com_a_gpu_certa
```

`--offline` exige as dependências no cache. O teste de relay local precisou
de sockets liberados fora do sandbox. As contagens se sobrepõem e não devem
ser somadas como se fossem testes distintos. Este documento resume os
resultados da sessão; não substitui os logs brutos da auditoria original.

## O que continua pendente

- Validar as correções no conteúdo de uma ISO e no sistema instalado.
- Testar liquidação com LND real; nesta rodada, LND teve cobertura simulada.
- Exercitar a aplicação do cofre com sudo e usuários distintos em ISO/VM.
- Executar a validação conjunta da main após os três merges.
- Tratar os outros 17 achados da auditoria de 16/09, sem alterar seu estado
  por associação com estas correções.

Não foi construída uma ISO nesta rodada. Merge de código não confirma que
pacotes ou imagens atualizados já tenham sido distribuídos.

[Índice da auditoria](README.md) · [Matriz de validação](pendencias-iso-vm-hardware.md)
