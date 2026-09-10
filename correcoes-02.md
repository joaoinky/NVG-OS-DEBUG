# Segunda rodada de correções

Data: 09/10/2026. Escopo: as cadeias 04, 05, 06 e 07 (NVG-05 a NVG-08),
relacionadas ao firewall, Tor, DNS, air-gap e ao painel `neo-status`.

## Alterações, na ordem de integração

1. **NVG-06 — conexões anteriores ao bloqueio:** as regras `tor.nft` e
   `killswitch-tor.nft` passaram a exigir o UID do Tor também em
   `ct state established,related`. Conexões diretas preexistentes não são
   mais aceitas apenas por estarem no conntrack.
2. **NVG-07 — DNS fora do Tor:** o tratamento de UDP/53 e TCP/53 foi movido
   para antes da exceção de LAN. UDP é redirecionado ao DNSPort 9053 e TCP ao
   TransPort 9040; DNS residual é bloqueado no filtro.
3. **Infraestrutura de verificação:** foi criada a consulta de estado real
   para nftables, interfaces (`ip`) e rádios (`rfkill`), com resultados
   `verified`, `mismatch` e `unknown`, códigos de saída distintos, referências
   de políticas e caches gravados somente após verificação.
4. **NVG-05 — marcador Tor órfão:** comandos de Tor, kill-switch e reset
   invalidam caches antes da troca, usam lock compartilhado e só gravam
   evidência depois de confirmar as regras carregadas. O `neo-status` consulta
   o kernel, em vez de confiar na existência do marcador.
5. **NVG-08 — falso sucesso do air-gap:** `neo-airgap` acompanha falhas,
   reenumera interfaces após parar gerenciadores, verifica interfaces e
   rádios no estado final e não anuncia sucesso sem evidência. A restauração
   invalida o cache primeiro e preserva inventários em falhas parciais.
6. **Leitores e documentação:** `mark`/`is_marked` passaram a verificar o
   estado real; `neo_curl` não faz fallback direto quando uma proteção não
   pode ser confirmada; `neo-status --json` diferencia `false` de `null`.

## Branches, commits e revisão

- `fix/regras-nft-excecoes`: `6c3cbd4`, `8536e72` — PR [#1](https://github.com/NEOpisa/neovanguard-os-dev/pull/1).
- `feat/verificacao-estado-rede`: `dd78ebd` — PR [#2](https://github.com/NEOpisa/neovanguard-os-dev/pull/2).
- `fix/04-07-marcadores`: `8834a9d` — PR [#3](https://github.com/NEOpisa/neovanguard-os-dev/pull/3).

As branches foram publicadas em sequência e os PRs foram abertos com bases
encadeadas: regras, verificação e marcadores.

## Evidências

- 14 testes de comandos e modos de rede aprovados.
- 16 testes do verificador de estado aprovados.
- 7 testes de tráfego nftables em namespace descartável aprovados.
- Referências de políticas, caches, CLI e links internos verificados.
- Nenhum rádio ou interface de rede real da máquina de desenvolvimento foi
  alterado; o air-gap foi testado com comandos de kernel simulados.

## CI e limites

Os primeiros checks dos três PRs falharam porque o runner não permitiu o
mapeamento de UID de `unshare`. O workflow foi ajustado nos commits
`77d448d`, `fbde731` e `092d703` para executar os testes de namespace com os
privilégios do container. Nos rechecks, o runner ainda apresentou limitações
de acesso a `/proc/1/ns/net`; a branch 1 também não contém o verificador da
seção 2. Isso é uma pendência do workflow, não uma reprovação dos testes
locais das correções, e deve ser resolvido antes do merge.

Não foi construída uma ISO nem validado hardware real. Permanecem necessárias
as validações de UID do serviço Tor, rádios, hotplug, gerenciadores de rede e
isolamento físico no equipamento alvo. As correções não certificam anonimato
Tor ou isolamento permanente.

## Registro desta documentação

Os arquivos dos problemas passaram a indicar o estado no próprio nome:
`✅` para resolvidos e `❌` para pendentes. O `README.md` e todas as referências
cruzadas foram atualizados para refletir essa nomenclatura.
