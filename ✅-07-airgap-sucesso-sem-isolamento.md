# Cadeia 07 — Operações de isolamento falham, air-gap é anunciado

> **Status: RESOLVIDO** — corrigido na branch `fix/04-07-marcadores` (`NVG-08`).

Erro: **NVG-08**. Impacto: alto, falsa indicação de isolamento. Verificação: reproduzido com todos os comandos de alteração de rede substituídos por funções que falham.

## Solução aplicada

`neo-airgap` agora acompanha falhas de serviços, interfaces, rádios e módulos, reenumera as interfaces após parar os gerenciadores e só grava o marcador após verificar `ip` e `rfkill` no estado final. O `neo-status` consulta o kernel diretamente. `neo-airgap-off` invalida o marcador antes da restauração e preserva os inventários quando a recuperação é parcial.

Validação: falhas operacionais, interfaces virtuais ativas, rádios desbloqueados, restauração parcial e reativação externa não produzem sucesso falso.

## Walkthrough

1. `neo-airgap` tenta baixar interfaces físicas com `ip`: [neo/bin/neo-airgap:19](../neovanguard-os-dev/neo/bin/neo-airgap:19).
2. Tenta bloquear rádios e parar os gerenciadores de rede. Os retornos de falha não interrompem o fluxo nem formam uma condição de sucesso: [neo/bin/neo-airgap:23](../neovanguard-os-dev/neo/bin/neo-airgap:23).
3. Independentemente dessas falhas, chama `mark airgap` e imprime que a máquina está fora da rede: [neo/bin/neo-airgap:55](../neovanguard-os-dev/neo/bin/neo-airgap:55).
4. `neo-status` usa a existência desse arquivo como evidência para a indicação de AIR-GAP: [neo/bin/neo-status:40](../neovanguard-os-dev/neo/bin/neo-status:40).

## Evidência observada

Em uma execução isolada, `ip`, `rfkill` e `systemctl` foram substituídos por funções com retorno 1. Foi oferecida uma interface fictícia, para que o laço de desligamento fosse exercitado.

Resultado: **código de saída 0**, **marcador airgap criado** e **mensagem de sucesso presente**. Nenhuma interface real foi alterada.

## O erro

O resultado comunica uma condição física que o programa não conseguiu estabelecer. Não é necessário provar que o desligamento falha em todo hardware: basta que uma operação necessária falhe para o sucesso incondicional deixar de representar o isolamento.

## Pontos de toque

- `neo-airgap → _neo-comum.sh/mark → neo-status`: uma tentativa é convertida em estado afirmativo.
- [Cadeia 04](✅-04-firewall-e-painel.md): mesma infraestrutura de marcadores, com causa diferente.
- A documentação já reconhece que estado solicitado não comprova air gap em [documentation/security-review-scope.md:17](../neovanguard-os-dev/documentation/security-review-scope.md:17); a reprodução identifica onde essa limitação aparece no comando.
- [Índice](README.md).
