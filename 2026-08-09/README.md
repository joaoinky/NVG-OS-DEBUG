# Auditoria inicial - NVG-01 a NVG-12

Revisão iniciada em **09/09/2026**, sobre a versão 1.2.0 em preparação,
commit `9bb3e666e938aa8c7ac746eed7a5ea69f11b46d4`. A pasta conserva seu
nome histórico; a data da auditoria é a registrada neste documento.

Foram encontrados nove problemas na primeira análise e mais três na revisão
de 11/09. Os dez relatórios abaixo acompanham a causa de cada falha e seu
efeito na instalação, na rede ou na recuperação de sementes.

[Visão geral do repositório](../README.md) ·
[Auditoria seguinte](../2026-09-16/README.md)

## Situação das correções

Os 12 problemas foram corrigidos no escopo registrado. A
[conferência de 16/09](../2026-09-16/correcoes-verificadas.md) reavaliou
essas correções e manteve o resultado, com as ressalvas de boot, hardware
e sistema instalado.

NVG-01 a NVG-04 foram tratados em `3e0b344`; NVG-05 a NVG-08, nos
PRs #1–#3, integrados pelo [PR #4](https://github.com/NEOpisa/neovanguard-os-dev/pull/4).
NVG-09 foi resolvido na quinta rodada; NVG-10 a NVG-12, na sexta.
Essas duas rodadas chegaram à main pelo
[PR #5](https://github.com/NEOpisa/neovanguard-os-dev/pull/5).

A sétima rodada tratou pendências de build, empacotamento e entrega da
versão 1.2.1. Foi integrada pelo
[PR #7](https://github.com/NEOpisa/neovanguard-os-dev/pull/7);
a indicação “ainda sem merge” no documento daquela rodada registra o
momento em que ele foi escrito.

## Relatórios

| Cadeia | Erros | O que dá errado | Impacto | Estado |
|---|---|---|---|---|
| [01 - Conta e shell](✅-01-conta-interpretada-pelo-shell.md) | NVG-01, NVG-02 | Apóstrofo na senha quebra o script; dados da conta podem ser interpretados como comandos | Alto | **Resolvido** (`3e0b344`) |
| [02 - Preservação e LUKS](✅-02-preservacao-e-luks.md) | NVG-03 | Raiz anunciada como mantida recebe criação destrutiva de contêiner | Crítico | **Resolvido** (`3e0b344`) |
| [03 - Btrfs e boot](✅-03-btrfs-e-primeiro-boot.md) | NVG-04 | Entrada systemd-boot não seleciona o subvolume que contém o sistema | Alto | **Resolvido** (`3e0b344`) |
| [04 - Firewall e painel](✅-04-firewall-e-painel.md) | NVG-05 | Painel pode anunciar Tor após retorno ao firewall de saída direta | Alto | **Resolvido** (PR #3) |
| [05 - Conexões anteriores](✅-05-conexoes-anteriores-ao-bloqueio.md) | NVG-06 | Sessões diretas estabelecidas continuam aceitas | Alto | **Resolvido** (PR #1) |
| [06 - DNS e LAN](✅-06-dns-fora-do-tor.md) | NVG-07 | Consulta ao resolvedor privado evita o redirecionamento Tor | Alto | **Resolvido** (PR #1) |
| [07 - Air-gap](✅-07-airgap-sucesso-sem-isolamento.md) | NVG-08 | Falhas de isolamento terminam com marcador e mensagem de sucesso | Alto | **Resolvido** (PR #3) |
| [08 - Recuperação Shamir](✅-08-shamir-recuperacao-de-outra-semente.md) | NVG-09 | Mistura de conjuntos gera outra semente com checksum válido | Alto | **Resolvido** (5ª rodada) |
| [09 - Kill-switch de VPN](✅-09-killswitch-vpn-saidas-fora-do-tunel.md) | NVG-10, NVG-11 | DNS para o resolvedor da LAN sai fora do túnel; UDP 51820/1194 sai para qualquer host | Alto / Médio | **Resolvido** (6ª rodada) |
| [10 - Senha de disco vazia](✅-10-senha-de-disco-vazia.md) | NVG-12 | Criptografia com senha vazia passa na validação, e o `luksFormat` falha depois de o disco ser apagado | Alto | **Resolvido** (6ª rodada) |


A gravidade se refere à consequência no cenário descrito. Os relatórios
preservam o diagnóstico original; procure a seção “Solução aplicada” e
as rodadas de correção para acompanhar o desfecho.

## Histórico das rodadas

[01 - primeira](correcoes-01.md) ·
[02 - segunda](correcoes-02.md) ·
[03 - substituída](correcoes-03.md) ·
[04 - quarta](correcoes-04.md) ·
[05 - quinta](correcoes-05.md) ·
[06 - sexta](correcoes-06.md) ·
[07 - build e entrega](correcoes-07.md)

A [reconciliação de 11/09](reconciliacao-2026-09-11.md) compara os registros
locais com os repositórios e explica quais correções prevaleceram.
O código ativo está em
[NEOpisa/neovanguard-os-dev](https://github.com/NEOpisa/neovanguard-os-dev);
os destinos antigos `neovos` e `neovosdev` foram aposentados.

## Como os problemas foram verificados

A primeira análise usou comandos simulados, diretórios temporários e
funções reais com dados sintéticos. NVG-03 foi confirmado pela análise
do fluxo destrutivo; não houve formatação de disco. NVG-04, NVG-06 e
NVG-07 tiveram análise de código e da semântica documentada, sem boot
em VM ou captura de tráfego naquela etapa.

A revisão de 11/09 acrescentou tráfego real em namespaces descartáveis
para NVG-10/11 e uma imagem de arquivo de 32 MB para testar o
`cryptsetup` no NVG-12. Não foram usados discos, chaves pessoais ou
regras de firewall do host.

Na primeira tentativa, a suíte Rust foi interrompida enquanto aguardava
o relay local; não houve aprovação completa. Na revisão posterior,
`./check` concluiu os 183 testes do workspace e `build-iso --check`
passou. São resultados daquela revisão, não da árvore atual.

Esta auditoria não incluiu boot real nem revisão integral dos aplicativos
e dependências. As verificações ainda necessárias estão na
[matriz de ISO, VM e hardware](../2026-09-16/pendencias-iso-vm-hardware.md).
