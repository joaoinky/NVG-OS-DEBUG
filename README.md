# NVG-OS Debug

Auditorias, correções e testes do **Neovanguard OS**.

Este repositório acompanha os problemas encontrados no desenvolvimento do
NVG-OS, da reprodução inicial à correção. Os relatórios mostram onde a falha
acontece, como reproduzi-la e quais testes sustentam a solução.

[Auditoria mais recente](2026-09-16/README.md) ·
[Últimas correções](2026-09-16/correcoes-2026-09-18.md) ·
[Código-fonte](https://github.com/NEOpisa/neovanguard-os-dev)

## O Neovanguard OS

O NVG-OS é uma distribuição Linux x86_64 baseada em Arch Linux, com KDE
Plasma e Wayland. Reúne um ambiente de uso diário e ferramentas voltadas a
privacidade, identidade Nostr e custódia de chaves, além de integrações com
Bitcoin, Lightning e Liquid.

O projeto inclui um instalador próprio em Rust, instalação offline,
criptografia de disco, suporte a Btrfs e modos de rede com Tor, VPN e
isolamento. O desktop usa o tema Birfree e os componentes NeovShell.
Há dois perfis de imagem: MBN Live, para uso temporário, e MBN Install,
para instalação.

A versão acompanhada nestes registros é a **1.2.1, em preparação**.
O trabalho de auditoria faz parte desse desenvolvimento: verificar o que
funciona, corrigir o que falha e deixar claro o que ainda não foi testado.

## O que há aqui

O código do sistema fica no
[neovanguard-os-dev](https://github.com/NEOpisa/neovanguard-os-dev).
Aqui ficam os diagnósticos, as provas de reprodução, os logs e o histórico
das correções. Os links para código e PRs podem exigir acesso ao repositório
de desenvolvimento.

| Registro | Conteúdo | Último estado documentado |
|---|---|---|
| [Auditoria inicial](2026-08-09/README.md) | NVG-01 a NVG-12: instalação, boot, rede e recuperação de sementes | 12 corrigidos no escopo verificado |
| [Auditoria de 16/09](2026-09-16/README.md) | NVG-13 a NVG-32: instalador, cofre, Nostr, pagamentos e validação | 3 corrigidos e integrados; 17 pendentes |
| [Correções de 18/09](2026-09-16/correcoes-2026-09-18.md) | Implementação, testes e merges de NVG-29, NVG-30 e NVG-17 | Integradas à main; ISO/VM pendente |

Os nomes históricos das pastas foram mantidos para preservar os links.
As datas de cada revisão estão nos próprios documentos.

## Última atualização

Em 18/09/2026, três correções chegaram à main do código-fonte:

- **NVG-29:** validação dos eventos Nostr antes de aceitar perfis —
  [PR #9](https://github.com/NEOpisa/neovanguard-os-dev/pull/9).
- **NVG-30:** conferência do valor, dos metadados e da validade da fatura
  LNURL antes do pagamento —
  [PR #10](https://github.com/NEOpisa/neovanguard-os-dev/pull/10).
- **NVG-17:** proteção da aplicação do cofre contra links maliciosos no
  destino — [PR #8](https://github.com/NEOpisa/neovanguard-os-dev/pull/8).

Os testes incluem regressões automatizadas, pagamentos CLN em regtest e
trocas concorrentes de diretórios. O [registro da rodada](2026-09-16/correcoes-2026-09-18.md)
detalha os resultados e as pendências, inclusive a validação conjunta após
os merges.

## Consultar e reproduzir

Para acompanhar um problema, comece pelo índice da auditoria e abra o
relatório pelo seu identificador `NVG-xx`. Para repetir uma prova, consulte
as [instruções de execução](2026-09-16/evidencias/README.md): elas indicam
o checkout, as ferramentas e o isolamento necessários.

Use ambientes descartáveis, identidades fictícias e fundos de regtest.
Não publique senhas, seeds, tokens ou dados pessoais junto de logs.
Ao relatar um resultado diferente, informe o commit, o ambiente, os passos
e o comportamento observado.

Uma correção testada no código não confirma, por si só, que uma ISO ou
instalação já a recebeu. As verificações que ainda dependem do sistema
instalado estão na [matriz de ISO, VM e hardware](2026-09-16/pendencias-iso-vm-hardware.md).
