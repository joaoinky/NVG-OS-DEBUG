# Correções de 20/09/2026 - cinco grupos

Oito achados receberam correções em cinco branches independentes, criadas a partir da `main` no commit `a57513f`. Os PRs abaixo estão abertos; ainda não houve integração conjunta nem construção de ISO.

## Publicação

| Grupo | Achados | Branch | Commits de implementação | PR |
|---|---|---|---|---|
| 1 | NVG-19, NVG-28 | `fix/nvg-nostr-robustness` | [`6e379b3`](https://github.com/NEOpisa/neovanguard-os-dev/commit/6e379b3), [`eca3a45`](https://github.com/NEOpisa/neovanguard-os-dev/commit/eca3a45) | [#32](https://github.com/NEOpisa/neovanguard-os-dev/pull/32) aberto |
| 2 | NVG-21, NVG-26 | `fix/neo-comum-shared-lib` | [`57ef2d2`](https://github.com/NEOpisa/neovanguard-os-dev/commit/57ef2d2), [`a2cb329`](https://github.com/NEOpisa/neovanguard-os-dev/commit/a2cb329) | [#33](https://github.com/NEOpisa/neovanguard-os-dev/pull/33) aberto |
| 3 | NVG-22 | `fix/nvg-22-sync-cursor` | [`a0a1974`](https://github.com/NEOpisa/neovanguard-os-dev/commit/a0a1974) | [#34](https://github.com/NEOpisa/neovanguard-os-dev/pull/34) aberto |
| 4 | NVG-27 | `fix/nvg-27-killswitch-ndp` | [`7dfe455`](https://github.com/NEOpisa/neovanguard-os-dev/commit/7dfe455) | [#35](https://github.com/NEOpisa/neovanguard-os-dev/pull/35) aberto |
| 5 | NVG-24, NVG-32 | `fix/quick-fixes-paper-pkgcheck` | [`058ebdb`](https://github.com/NEOpisa/neovanguard-os-dev/commit/058ebdb), [`c44f913`](https://github.com/NEOpisa/neovanguard-os-dev/commit/c44f913) | [#36](https://github.com/NEOpisa/neovanguard-os-dev/pull/36) aberto |

## Grupo 1: NVG-19 e NVG-28

Envelopes com tamanho inválido podiam abortar o processo, e o teste de aceleração dependia da GPU do host. A decifragem agora valida versão, tamanhos e quantidade de blocos, limita o pacote a 8 MiB e usa reserva falível. Os testes de aceleração cobrem Intel, NVIDIA, AMD e ausência de GPU sem consultar o hardware do executor.

**Validação:** `./check quick` aprovado: 198 testes Rust, formatação, Clippy e verificações de empacotamento. Regressões cobrem envelopes malformados, limites de blocos e pacote de 8 MiB. A entrada com `bruto=u64::MAX` também retornou erro em executável com `panic=abort`.

**Pendente:** Não foi construída ISO. Falta conferir os binários empacotados e a restauração no sistema instalado.

## Grupo 2: NVG-21 e NVG-26

A elevação com sudo perdia subcomandos já consumidos pelo parser, e o perfil gravado pelo assistente era lido de outro arquivo. A biblioteca preserva os argumentos originais e lê `profile.conf/profile=`, com compatibilidade para `perfil.conf/perfil=`. O formato atual tem precedência; configuração inválida usa `cold` com aviso.

**Validação:** 57 testes aprovados: biblioteca compartilhada (7), modos de rede (18), estado de rede (17), MAC (8) e dependências de build (7). Sintaxe shell, referências de ajuda dos 56 comandos e `git diff --check` aprovados. Os testes exercitam relançamento de Flash/mesh, limites dos argumentos, persistência do assistente e SOCKS no `neo_curl`.

**Pendente:** Não foi executado o assistente completo com sudo, nem gravação de firmware ou transportes mesh reais. NVG-25, sobre o menu capturado na resposta, permanece pendente. `./check quick` completo não foi repetido nesta branch.

## Grupo 3: NVG-22

O timestamp agregado incluía o relay local e omitia notas offline antigas. A sincronização compara IDs por destino externo, consulta as notas locais sem o corte de 500 eventos e exige EOSE e confirmação positiva do ID publicado. Falhas parciais retornam erro e são reconciliadas na próxima execução, sem cursor persistido. A atualização das 200 notas recentes por destino e o fluxo Bitcoin são preservados.

**Validação:** 22 cenários aprovados na integração `cargo test --locked -p nvg-nostr --test rpc_eventos`: 12 de RPC e 10 de sincronização, com eventos assinados e verificador Rust real. Cobertura inclui 501 notas no mesmo timestamp, relays divergentes, ACK incorreto, falha parcial e retomada. Formatação, Clippy, sintaxe shell e verificação dos comandos aprovados.

**Pendente:** Transporte simulado; falta validar com o relay empacotado e dois relays reais. A retomada depende de os eventos ainda existirem no relay local, cujo armazenamento é volátil. `./check quick` completo não foi repetido. Compartilha mudanças de EOSE/ACK em `neo-nostr-rpc` e testes com o PR #31; revisar essa sobreposição ao integrar.

## Grupo 4: NVG-27

O endpoint IPv6 deixava de responder quando o cache de vizinhos esvaziava. O kill-switch permite Neighbor Solicitation e Advertisement nas cadeias de entrada e saída, restritos a Hop Limit 255 e código zero. A referência usada para verificar o firewall acompanha as novas regras.

**Validação:** 12 testes de tráfego real em namespaces descartáveis e 18 testes de estado aprovados. Conferência das quatro políticas contra regras carregadas pelo kernel aprovada. Casos incluem esvaziamento repetido de vizinhos, endpoint via gateway e manutenção do bloqueio de DNS, ping e tráfego não autorizado.

**Pendente:** O firewall do host não foi alterado. A interface de túnel dos testes é dummy; falta reconexão com WireGuard/OpenVPN real, ISO/VM e roaming. `./check quick` completo não foi repetido.

## Grupo 5: NVG-24 e NVG-32

A matriz de 24 palavras ultrapassava a folha, e conflitos de pacotes instalados eram reportados como pacote inexistente. O formulário distribui a matriz em quatro colunas, mantém células de 7 x 6 mm e define A4 explicitamente. O verificador lê o índice com `pacman -Slq`, sem resolver transação, e diferencia ausência de pacote de erro de leitura do índice.

**Validação:** Teste de geometria e geração de PDF aprovado para 12 e 24 palavras; ambos renderizados e inspecionados visualmente, com uma página A4. Três testes do verificador de pacotes aprovados, incluindo conflito do host, erro de índice e timeout. Referências e ajuda dos 56 comandos, sintaxe shell e `git diff --check` aprovados.

**Pendente:** Não houve impressão física nem construção de ISO/pacotes. `./check quick` completo não foi repetido nesta branch.

## Integração e acompanhamento

A auditoria de 16/09 passa a ter **13 achados corrigidos no código e sete pendentes**. NVG-17, NVG-29 e NVG-30 estão integrados à main. NVG-20 e NVG-31 continuam no PR #31, aberto, e os oito achados desta rodada estão nos PRs #32 a #36.

Permanecem pendentes NVG-13, NVG-14, NVG-15, NVG-16, NVG-18, NVG-23 e NVG-25. A correção de leitura do perfil (NVG-26) não resolve a captura incorreta do menu no assistente (NVG-25).

O grupo 3 compartilha alterações de EOSE/ACK com o PR #31. Os grupos 2 e 5 também acrescentam verificações ao arquivo `check`. Ao integrar, preservar ambos os conjuntos de testes e executar a validação conjunta, começando pelo grupo 1 para eliminar a dependência de GPU do NVG-28. Nenhum resultado isolado desta rodada comprova a aprovação de todas as branches combinadas.

Os commits adicionais `3e66c27`, `75eb2a6`, `0134fba`, `3a6a8fa` e `59c8568` atualizam os relatórios no repositório de código, respectivamente para os grupos 1 a 5. Não alteram a implementação testada.

As contagens acima pertencem a suítes e branches específicas; não devem ser somadas como testes únicos do projeto. A falha inicial dos testes de modos de rede no grupo 2 foi causada pela ausência de `jq` no PATH; a execução com a ferramenta disponível aprovou os 18 testes. Os logs da auditoria original foram preservados como evidência histórica, sem atribuir a eles as correções posteriores.

[Índice da auditoria](README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
