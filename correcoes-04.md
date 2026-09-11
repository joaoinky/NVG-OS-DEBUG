# Quarta rodada de correções

Data: 10/09/2026, com a mescla na `main` em 11/09/2026. Escopo: as cadeias 04, 05, 06 e 07 (NVG-05 a NVG-08), ligadas ao firewall, Tor, DNS, air-gap e ao painel `neo-status`.

Esta rodada foi feita no `neovanguard-os-dev` e registrada no repositório NVG-OS-DEBUG, onde aparece como `correcoes-02.md`. Aqui ela é a **quarta**, porque a segunda e a terceira locais (NVG-04 e a primeira versão do NVG-05) já tinham esses números. Ver [reconciliação](reconciliacao-2026-09-11.md).

## Alterações, na ordem de integração

1. **NVG-06, conexões anteriores ao bloqueio:** `tor.nft` e `killswitch-tor.nft` passaram a exigir o UID do Tor também em `ct state established,related`. Conexões diretas preexistentes deixam de ser aceitas só por estarem no conntrack.
2. **NVG-07, DNS fora do Tor:** o tratamento de UDP/53 e TCP/53 foi movido para antes da exceção de LAN. UDP vai ao DNSPort 9053 e TCP ao TransPort 9040; DNS residual é bloqueado no filtro.
3. **Infraestrutura de verificação:** consulta do estado real de nftables, interfaces (`ip`) e rádios (`rfkill`), com resultados `verified`, `mismatch` e `unknown`, códigos de saída distintos, referências de políticas e caches gravados só depois da verificação. Arquivos: `neo/lib/neo-network-state.py`, `neo/lib/neo-rede.sh`, `neo/lib/network-policies.json`.
4. **NVG-05, marcador Tor órfão:** Tor, kill-switch e reset invalidam os caches antes da troca, usam um lock compartilhado e só gravam evidência depois de confirmar as regras carregadas. O `neo-status` consulta o kernel em vez de confiar na existência do marcador. Isto **substitui** a correção da [terceira rodada](correcoes-03.md).
5. **NVG-08, falso sucesso do air-gap:** `neo-airgap` acompanha falhas, reenumera interfaces depois de parar os gerenciadores, verifica interfaces e rádios no estado final e não anuncia sucesso sem evidência. A restauração invalida o cache primeiro e preserva os inventários em falhas parciais.
6. **Leitores e documentação:** `mark`/`is_marked` passaram a verificar o estado real; `neo_curl` não cai para conexão direta quando uma proteção não pode ser confirmada; `neo-status --json` diferencia `false` de `null`.

## Branches, commits e PRs

| PR | Branch | Commits | Base | Chegou à `main`? |
|---|---|---|---|---|
| [#1](https://github.com/NEOpisa/neovanguard-os-dev/pull/1) | `fix/regras-nft-excecoes` | `6c3cbd4`, `8536e72`, `77d448d` | `main` | Sim, `4ebd017` |
| [#2](https://github.com/NEOpisa/neovanguard-os-dev/pull/2) | `feat/verificacao-estado-rede` | `dd78ebd`, `fbde731` | `fix/regras-nft-excecoes` | Só pelo #4 |
| [#3](https://github.com/NEOpisa/neovanguard-os-dev/pull/3) | `fix/04-07-marcadores` | `8834a9d`, `092d703` | `feat/verificacao-estado-rede` | Só pelo #4 |
| [#4](https://github.com/NEOpisa/neovanguard-os-dev/pull/4) | `feat/verificacao-estado-rede` | ponta `633ca01` | `main` | Sim, `2e8320c` |

Os PRs #2 e #3 foram mesclados nas bases encadeadas **depois** que o #1 já tinha entrado na `main`: às 20:26:19 (UTC) de 11/09 entrou o #1 na `main`, e às 20:26:38 e 20:27:03 os outros dois foram mesclados nas branches-base. O GitHub mostrava os três como "merged", mas a `main` só tinha o conteúdo do #1. O PR #4 levou a ponta da cadeia para a `main`. A mescla foi limpa, e a árvore da `main` ficou idêntica à de `633ca01`.

## Evidências

Reexecutadas em 11/09/2026, como usuário comum, na árvore local reconciliada (`trabalho-local-2026-09-11`):

- `scripts/test-network-state.py`: 16 testes aprovados.
- `scripts/test-network-modes.py`: 14 testes aprovados.
- `scripts/test-nft-network.py`: 7 testes de tráfego em namespace descartável aprovados.
- `scripts/check-neo-refs.py`: 55 comandos, funções, pacotes e chamadas conferidos.
- Nenhum rádio ou interface real da máquina de desenvolvimento foi alterado; o air-gap foi testado com comandos de kernel simulados.

## CI e limites

- **`scripts/check-network-policies.py` não roda como usuário comum.** A guarda da linha 92 compara o namespace de rede com o de `/proc/1/ns/net`, e o kernel nega essa leitura a quem não é root (`PermissionError: [Errno 13]`). É a mesma falha dos rechecks do CI (`/proc/1/ns/net`). Os commits `77d448d`, `fbde731` e `092d703` deram privilégios de container ao workflow, mas não resolveram essa leitura. Pendência do verificador, não das regras. **Resolvida na [quinta rodada](correcoes-05.md):** a leitura falha dentro de qualquer `unshare -rn`, mesmo como root.
- Não foi construída ISO nem validado hardware real. Continuam necessárias as validações de UID do serviço Tor, rádios, hotplug, gerenciadores de rede e isolamento físico no equipamento-alvo. As correções não certificam anonimato Tor nem isolamento permanente.

## Pendências

NVG-09 (Shamir) e a pendência do `check-network-policies.py` acima; as duas foram resolvidas na [quinta rodada](correcoes-05.md).
