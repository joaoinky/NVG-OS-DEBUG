# Auditoria de 16/09/2026 - NVG-13 a NVG-32

Revisão da versão **1.2.1 em preparação**, na base
`619d7697bf9ff0067a0d314c6456a5183f7a733b`. O trabalho começou em 15/09
e confirmou 20 problemas novos, além de conferir as correções da auditoria
anterior.

[Visão geral](../README.md) ·
[Correções de 20/09](correcoes-2026-09-20.md) ·
[Correções de 19/09](correcoes-2026-09-19.md) ·
[Correções de 18/09](correcoes-2026-09-18.md) ·
[Evidências](evidencias/README.md) ·
[Validação em ISO/VM](pendencias-iso-vm-hardware.md)

## Situação em 20/09

**13 achados corrigidos no código e sete pendentes.** NVG-17, NVG-29 e
NVG-30 estão integrados à `main`. NVG-20 e NVG-31 continuam no PR #31,
e os oito achados da nova rodada estão nos PRs #32 a #36, todos abertos.

O [registro dos cinco grupos](correcoes-2026-09-20.md) reúne branches,
commits, PRs, validações e limites. As correções anteriores estão nos
registros de [18/09](correcoes-2026-09-18.md) e [19/09](correcoes-2026-09-19.md).

Os 12 problemas anteriores, NVG-01 a NVG-12, permanecem corrigidos no
escopo reavaliado. A [conferência individual](correcoes-verificadas.md)
distingue as correções verificadas das funcionalidades que ainda precisam
de teste no sistema instalado.

Não foi construída uma ISO. A validação conjunta das correções e os cenários
da matriz de ISO/VM continuam pendentes.

## Relatórios

Os títulos descrevem o defeito encontrado na base original, inclusive nos
casos já corrigidos. “Alto”, “médio” e “baixo” indicam o impacto no cenário
do relatório, não uma pontuação CVSS.

Os nomes usam ✅ para correções implementadas e testadas no código e ❌ para
problemas que continuam pendentes. A última coluna distingue PR aberto de
correção já integrada.

| Cadeia | Erro | O que dá errado | Impacto | Estado |
|---|---|---|---|---|
| [01 - Mídia Live como destino](❌-13-particao-da-midia-live.md) | NVG-13 | Partições da própria mídia Live são aceitas como destino manual | Alto | **Pendente** |
| [02 - Partições sobrepostas](❌-14-raiz-esp-home-sobrepostas.md) | NVG-14 | A mesma partição pode ser raiz, ESP e home | Alto | **Pendente** |
| [03 - Usuário reservado](❌-15-usuario-reservado.md) | NVG-15 | `root` é aceito como nova conta e a instalação falha depois da formatação | Alto | **Pendente** |
| [04 - Boot do Cold Vault](❌-16-boot-vault-perde-parametros.md) | NVG-16 | A entrada perde parâmetros necessários para Btrfs e LUKS | Alto | **Pendente** |
| [05 - Links no cofre](✅-17-cofre-links-no-destino.md) | NVG-17 | Aplicação privilegiada segue links no home e no temporário | Alto | Corrigido - [PR #8](https://github.com/NEOpisa/neovanguard-os-dev/pull/8) |
| [06 - Restauração sem filtros](❌-18-restauracao-instalador-sem-filtros.md) | NVG-18 | O instalador ignora a lista de arquivos permitidos | Alto | **Pendente** |
| [07 - Envelope não autenticado](✅-19-envelope-causa-panic.md) | NVG-19 | Um tamanho não autenticado pode abortar o processo | Médio | Corrigido no código - [PR #32](https://github.com/NEOpisa/neovanguard-os-dev/pull/32) aberto |
| [08 - Limpeza de DMs](✅-20-limpeza-dms-nao-publica.md) | NVG-20 | A interface anuncia envio sem publicar pedidos de exclusão | Médio | Corrigido no código - [PR #31](https://github.com/NEOpisa/neovanguard-os-dev/pull/31) aberto |
| [09 - Elevação e argumentos](✅-21-elevacao-perde-argumentos.md) | NVG-21 | Flash e transportes mesh perdem a ação ao executar `sudo` | Médio | Corrigido no código - [PR #33](https://github.com/NEOpisa/neovanguard-os-dev/pull/33) aberto |
| [10 - Sincronização offline](✅-22-sync-ignora-eventos-offline.md) | NVG-22 | Eventos offline antigos deixam de ser publicados | Médio | Corrigido no código - [PR #34](https://github.com/NEOpisa/neovanguard-os-dev/pull/34) aberto |
| [11 - Secure Boot](❌-23-secureboot-sucesso-falso.md) | NVG-23 | O setup anuncia uma cadeia assinada após falha | Alto | **Pendente** |
| [12 - Matriz de aço](✅-24-matriz-24-palavras-cortada.md) | NVG-24 | A matriz para 24 palavras ultrapassa a página | Médio | Corrigido no código - [PR #36](https://github.com/NEOpisa/neovanguard-os-dev/pull/36) aberto |
| [13 - Menu do primeiro boot](❌-25-wizard-captura-menu.md) | NVG-25 | O assistente captura o menu junto com a resposta | Alto | **Pendente** |
| [14 - Perfil divergente](✅-26-perfil-gravado-nao-lido.md) | NVG-26 | O perfil é gravado em arquivo e chave diferentes dos lidos | Médio | Corrigido no código - [PR #33](https://github.com/NEOpisa/neovanguard-os-dev/pull/33) aberto |
| [15 - VPN e IPv6](✅-27-vpn-ipv6-sem-ndp.md) | NVG-27 | O kill-switch impede o endpoint quando o cache NDP esvazia | Médio | Corrigido no código - [PR #35](https://github.com/NEOpisa/neovanguard-os-dev/pull/35) aberto |
| [16 - Teste dependente de GPU](✅-28-teste-depende-da-gpu.md) | NVG-28 | O teste do manifesto falha em hosts NVIDIA e bloqueia o check | Médio | Corrigido no código - [PR #32](https://github.com/NEOpisa/neovanguard-os-dev/pull/32) aberto |
| [17 - Evento Nostr forjado](✅-29-rpc-aceita-evento-forjado.md) | NVG-29 | O cliente aceita perfil com hash e assinatura inválidos | Alto | Corrigido - [PR #9](https://github.com/NEOpisa/neovanguard-os-dev/pull/9) |
| [18 - Valor do zap](✅-30-zap-nao-confere-valor.md) | NVG-30 | O valor da fatura não é comparado aos sats solicitados | Alto | Corrigido - [PR #10](https://github.com/NEOpisa/neovanguard-os-dev/pull/10) |
| [19 - Tags descartadas](✅-31-assinatura-descarta-tags.md) | NVG-31 | A CLI ignora `--tag` e envia evento sem referências | Médio | Corrigido no código - [PR #31](https://github.com/NEOpisa/neovanguard-os-dev/pull/31) aberto |
| [20 - Verificador de pacotes](✅-32-verificador-pacotes-falso-alarme.md) | NVG-32 | Um conflito do host produz diagnóstico de pacote inexistente | Baixo | Corrigido no código - [PR #36](https://github.com/NEOpisa/neovanguard-os-dev/pull/36) aberto |


Entre os achados ainda pendentes, os de seleção de disco e restauração
(NVG-13/14/15/18) e os de boot e isolamento (NVG-16/23/25) merecem atenção
prioritária pelas consequências descritas nos relatórios.

## Resultados da auditoria original

Estes números pertencem à execução de 15–16/09, antes das correções posteriores:

| Conjunto | Resultado |
|---|---|
| Rust | 182 testes aprovados e 1 reprovado; falha dependente de GPU, NVG-28 |
| Python | 103 testes aprovados, incluindo 10 de tráfego em namespaces |
| Políticas de rede | Quatro políticas nft e suas sondas aprovadas |
| Qt | 14 resultados aprovados em modo offscreen |
| Agente systemd | Política de IPC, sockets, acesso ao home e NIP-46 aprovada |
| Sintaxe | 84 arquivos Bash/PKGBUILD, 37 Python e 10 JSON sem falhas |
| Build | `./build-iso --check` sem aprovação integral; nenhuma ISO construída |

As provas adicionais reproduziram os novos defeitos. Nelas, um teste
aprovado significa que o problema foi observado, não que foi corrigido.
Os [comandos e logs](evidencias/README.md) detalham as condições de cada
execução. Os testes posteriores estão separados no
[registro de 18/09](correcoes-2026-09-18.md).

## Escopo e limites

A revisão cobriu instalador, armazenamento, boot, cofre, Nostr, agente e
IPC, comandos `neo-*`, políticas de rede, primeiro boot, build,
empacotamento e integração visual.

As reproduções usaram funções e comandos reais, com isolamento ou
simulação nas operações sensíveis. Os testes originais não tocaram em
discos, contas, chaves pessoais, firmware ou firewall do host, nem
realizaram pagamentos. O regtest CLN com fundos fictícios foi executado
depois, na correção da NVG-30.

Dependências externas, kernel e pacotes Arch/AUR não tiveram revisão
integral. Os resultados não certificam uma ISO; os testes necessários
no sistema instalado estão na
[matriz de validação](pendencias-iso-vm-hardware.md).
