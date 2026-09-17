# NVG-21 — Flash e transportes mesh perdem a ação ao executar sudo

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **média** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[need_root](../../../neo/bin/_neo-comum.sh#L56), [cmd_seedsigner](../../../neo/bin/neo-flash#L179) e [dispatch do mesh](../../../neo/bin/neo-mesh#L162).

`need_root` relança `sudo -E "$0" "$@"`. Em `neo-flash seedsigner`, o dispatcher já consumiu o subcomando e o parser consome destino/modelo antes dessa chamada: a elevação recebe zero argumentos e relança a listagem padrão. Em `neo-mesh --bluetooth` e `--wifi-direct`, o dispatcher também remove o seletor; o processo elevado segue para a ação padrão de anúncio/procura. A ação originalmente pedida não é preservada.

## Evidência

Foram extraídas as funções reais e substituída somente a elevação por um registrador. Flash com destino/modelo recebeu `argumentos_na_elevacao=0`; Bluetooth PAN e Wi-Fi Direct também perderam seu seletor. [Log](evidencias/probes-shell.log).

## Limites da conclusão

Nenhum dispositivo foi gravado e nenhum rádio foi ligado. O problema se manifesta quando é necessário elevar privilégios; uma execução já iniciada com sudo evita esse caminho. Krux não foi incluído no diagnóstico sem uma prova equivalente.

## Direção da correção

Elevar antes de consumir argumentos ou guardar a linha original completa. Cobrir a execução normal e a relançada com cada subcomando e parâmetros.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
