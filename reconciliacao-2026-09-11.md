# Reconciliação: local, NVG-OS-DEBUG e neovanguard-os-dev

Data: 11/09/2026. Objetivo: juntar as três versões desta auditoria e do código num estado só, sem perder o trabalho feito localmente.

## As três fontes

| Fonte | Onde | Estado em 11/09/2026 |
|---|---|---|
| **Local** | `~/Projetos/Neovanguard/distro` | `main` em `08f0bbe`, mais 58 arquivos alterados e **nunca commitados** |
| **NVG-OS-DEBUG** | [github.com/joaoinky/NVG-OS-DEBUG](https://github.com/joaoinky/NVG-OS-DEBUG), ponta `000e412` | Cópia desta pasta, à frente na rede (NVG-05 a NVG-08) e com os arquivos renomeados para ✅/❌ |
| **neovanguard-os-dev** | [github.com/NEOpisa/neovanguard-os-dev](https://github.com/NEOpisa/neovanguard-os-dev), `main` | Antes: `4ebd017`, só com o PR #1. Depois do PR #4: `2e8320c`, com os PRs #1, #2 e #3 |

O NVG-OS-DEBUG nasceu da branch local `audit-public-2026-09-09` (commit órfão `27fd0e8`, só com os 12 arquivos desta pasta). O NVG-OS-DEBUG serviu de **modelo** para o formato: nomes com ✅/❌, bloco de status e seção "Solução aplicada" em cada cadeia.

## Regra aplicada

Onde o mesmo erro tinha correção nos dois lados, **prevalece o código do `neovanguard-os-dev`**. Os PRs #1, #2 e #3 contam como correções mescladas. Onde só o local tinha o trabalho, ele foi preservado e documentado.

## Decisão por erro

| Erro | Local | NVG-OS-DEBUG | neovanguard-os-dev | Decisão |
|---|---|---|---|---|
| NVG-01, NVG-02 | Corrigido (`3e0b344`) | ✅ | Mesmo commit, ancestral da `main` | ✅ Resolvido |
| NVG-03 | Corrigido (`3e0b344`) | ✅ | Mesmo commit | ✅ Resolvido |
| NVG-04 | Corrigido (`3e0b344`, rodada 2) | **❌ pendente** | **Mesmo commit**: `rootflags=subvol=@` está na `main` | ✅ Resolvido. O ❌ do NVG-OS-DEBUG está errado |
| NVG-05 | Corrigido v1 (`3e0b344`, rodada 3: `unmark` cruzado) | ✅ v2 | v2: PR #3, verificação no kernel | ✅ Vale a **v2 do upstream**; a v1 fica no histórico |
| NVG-06, NVG-07 | Pendente | ✅ | PR #1, na `main` | ✅ Resolvido |
| NVG-08 | Pendente | ✅ | PR #3 | ✅ Resolvido |
| NVG-09 | Pendente | ❌ | Não tocado | ✅ Resolvido depois, na [quinta rodada](correcoes-05.md) |

## Divergências encontradas

1. **Os PRs #2 e #3 não tinham chegado à `main`.** Eram PRs encadeados (base do #2 = branch do #1; base do #3 = branch do #2). O #1 entrou na `main` às 20:26:19 UTC de 11/09, e só depois o #2 e o #3 foram mesclados nas **branches-base**. O GitHub mostrava os três como "merged", mas `dd78ebd` e `8834a9d` não estavam na `main`. **Correção:** [PR #4](https://github.com/NEOpisa/neovanguard-os-dev/pull/4) (`feat/verificacao-estado-rede` → `main`), mesclado em `2e8320c`. A mescla foi limpa, e a árvore resultante é idêntica a `633ca01`.
2. **NVG-04 marcado como pendente no NVG-OS-DEBUG.** A correção está em `3e0b344`, ancestral da `main` do `neovanguard-os-dev` (função `root_mount_option` e teste `btrfs_novo_seleciona_o_subvolume_raiz_no_boot`). O NVG-OS-DEBUG perdeu o registro dela porque sobrescreveu o `correcoes-02.md`.
3. **Numeração das rodadas.** No NVG-OS-DEBUG, o `correcoes-02.md` passou a descrever a rodada de rede, e o `correcoes-03.md` não existe. Aqui ficaram as quatro:
   - [correcoes-01](correcoes-01.md): NVG-01 a NVG-03 (local);
   - [correcoes-02](correcoes-02.md): NVG-04 (local);
   - [correcoes-03](correcoes-03.md): NVG-05 v1 (local, marcada como substituída);
   - [correcoes-04](correcoes-04.md): NVG-05 a NVG-08 (upstream, o `correcoes-02.md` do NVG-OS-DEBUG).
4. **Data invertida.** O `correcoes-02.md` do NVG-OS-DEBUG diz "09/10/2026"; os commits são de **10/09/2026**. Aqui está corrigido.
5. **Links.** O NVG-OS-DEBUG aponta para `../neovanguard-os-dev/...` (clone ao lado), e a pasta local apontava para `/home/neo/...`. Agora os links são relativos ao repositório (`../../../`) e funcionam tanto no clone quanto no GitHub.
6. **As duas versões do NVG-05 não conflitam no código.** O PR #3 foi escrito em cima de `3e0b344`, então parte da v1 e a substitui. Nada da v1 se perde: ela continua no histórico.

## Trabalho local que não estava em repositório nenhum

O que estava só na árvore de trabalho foi salvo no commit **`384b797`**, na branch local **`trabalho-local-2026-09-11`** (criada a partir de `08f0bbe`). Nenhum desses arquivos existia no `neovanguard-os-dev` nem no NVG-OS-DEBUG. Inventário:

### Tiling automático removido

- Apagados: `vendor/krohnkite/` (LICENSE, README, `.kwinscript`), `usr/local/bin/nvg-tiling`, `nvg-tiling.desktop`, `nvg-tiling-mode.desktop`.
- Limpos: os 25 atalhos `Krohnkite*` e os `_launch` de `Meta+Shift+T`/`Meta+Alt+T` nos dois `kglobalshortcutsrc` (skel e liveuser); `krohnkiteEnabled`, `[Script-krohnkite]` e `[Neovanguard] NeovTilingMode` nos dois `kwinrc` e no `defaults` do look-and-feel; a entrada em `profiledef.sh` da mbn-live; os quatro caminhos na lista de branding do `rust/nvg-installer/src/install.rs`; `.gitignore` e `LICENSES.md`.
- `branding/gen-assets.sh` troca o desempacotamento por `rm -rf` das cópias antigas, que ficaram no perfil fora do git.
- `ElectricBorderMaximize` volta a `true` (só existia desligado por causa do modo automático). O `motd` troca "Tiling: Meta+Shift+T" por "Menu: tecla Meta".

### Tecla Meta

- `activate application launcher` passou de `none,Meta\tAlt+F1` para `Meta\tAlt+F1,Meta\tAlt+F1` nos dois `kglobalshortcutsrc`. Era a causa do Meta morto na 1.2.0.
- `[ModifierOnlyShortcuts]` saiu dos `kwinrc`: o KWin 6.7 não lê mais essa seção.
- `scripts/check-shortcuts.py`: `check_krohnkite` virou `check_launcher` (acusa a ação sem `Meta`) e passa a recusar `activate widget N`, que são IDs numéricos de outra instalação.
- Comentários de `build-iso`, `nvg-dock` e do plasmoide menu corrigidos.

### Atalhos novos e retirados

- Entraram `Meta+S` (central, associada à instância real no layout), `Meta+I` (Configurações do sistema) e `Meta+Shift+C` como segunda tecla do histórico da área de transferência.
- Saíram `Meta+Shift+N`, `Meta+Alt+B` e `Meta+Shift+B`, que dependiam de IDs de widget.

### Vidro Frost (Birfree 0.6)

- `gen-plasma-style.py` emite `hint-stretch-borders` e desenha o reflexo como preenchimento, não como `stroke`. Isso acaba com as emendas a cada 12 px na barra, na dock e no menu. Os 14 SVGs do desktoptheme foram regenerados.
- `materials.json`: `glass03` 0,90 → 0,80 e `floating` 0,78 → 0,62. Também em `sddm/Frost.js`, nos `Frost.js` dos plasmoides e em `documentation/frost.md` (itens 10 e 11).
- `scripts/test-frost.py` vigia as duas coisas.

### Plasmoides (NeovShell 0.3)

- **control**: central com `Meta+S`; sai o controle de organização das janelas, que chamava o `nvg-tiling`.
- **desktops**: troca de área por `nvg-session desktop N` (posição a partir de 1, vale em X11 e Wayland) e navegação por teclado (setas, Enter, Espaço).
- **media**: `SeekSlider.qml` novo separa o destino do arraste da posição recebida e permite buscar pela barra com o teclado. Teste em `scripts/qml/tst_seek.qml`, rodado pelo `build-iso --check` via `qmltestrunner` quando ele existe.
- **menu**: marca maior na dock (caixa `altura × 1,38`); Home/End vão às pontas; a seleção sobrevive à atualização da lista (acompanha o `favoriteId`); o botão diz "Adicionar"/"Remover favorito" conforme o estado.
- **windowtitle**: reescrito com `updateTitle()`, sem piscar e com largura limitada.
- `scripts/plasmoid-preview/` e `scripts/test-desktop-controls.py` acompanham as mudanças.

### Scripts da sessão

- `nvg-dock`: uma ida só ao plasmashell (localizar, ler, trocar, devolver `antes:depois`), confere o que ficou em vez do que pediu, e mostra a falha por `notify-send`. Eram três idas, uns dois segundos numa VM.
- `nvg-session`: sair, reiniciar e desligar usam `org.kde.LogoutPrompt` (confirmação nativa); ganhou `desktop N`.
- `nvg-quick`: as seis consultas rodam em paralelo; `powerAvailable` só com um perfil conhecido; ações novas `bluetooth-settings` (`kcm_bluetooth`) e `brightness-settings` (`kcm_powerdevilprofilesconfig`).

### zsh

- `compinit` completo quando o cache não existe; `INC_APPEND_HISTORY` desligado, porque o `SHARE_HISTORY` já grava; `typeset -U path` para o PATH não duplicar ao recarregar; `EDITOR`/`VISUAL` do usuário respeitados.

### Documentação

- `documentation/desktop.md`: tabela de atalhos, launcher, player, título e zsh.

### Fora do git (ignorado, sem perda)

- `out/`: ISOs 1.2.0 Live e Install de **10/09 às 15:52–15:59**, com logs e somas. Foram geradas **antes** do trabalho acima e antes dos PRs de rede: não contêm nenhuma das duas coisas.
- `build/perfis/` (gerado), `work/` (do `mkarchiso`, dono root) e `vm/`.

## Estado do git depois da reconciliação

```
main (local, 3 commits à frente de osdev/main, não publicada)
├── 4ce4080  documentação desta reconciliação
├── 9c0eb3d  merge osdev/main (PRs #1–#4) no trabalho local
│   ├── 2e8320c  main do neovanguard-os-dev (PR #4)
│   └── 384b797  trabalho local salvo
└── 08f0bbe  onde a main local estava
```

- A mescla do upstream no trabalho local foi limpa. O único arquivo tocado pelos dois lados, `build-iso`, recebeu alterações em trechos diferentes (lista de arquivos do pacote × teste QML do player).
- **Prova da mescla:** aplicar o patch `08f0bbe..384b797` sobre `osdev/main` dá exatamente a árvore de `9c0eb3d` (`c285ff0…`). Nenhum dos 72 arquivos que diferem do upstream está fora do trabalho local ou da documentação.
- Nenhum remoto tinha commits fora da `main` local em 11/09/2026.
- Para publicar: `git push osdev main`.

### Limpeza feita depois da mescla

A `main` local avançou até a ponta reconciliada (fast-forward), e as cópias e sobras foram apagadas:

| Apagado | Por que não fazia mais falta |
|---|---|
| Branch `trabalho-local-2026-09-11` | Virou a `main` |
| Branch `tres-isos` | Já contida na `main` |
| Branch `audit-public-2026-09-09` | Árvore idêntica a `3e0b344:documentation/auditoria-erros/2026-09-09`; é a semente do NVG-OS-DEBUG |
| Remoto `neovosdev` | O repositório não existe mais (404 na API); o `neovosdev/main` já estava contido na `main` |
| `build/perfis/myo/` | Perfil gerado da ISO MYO, que saiu da distro; ainda carregava a licença do Krohnkite |
| Pacotes `*-1.0.0-1-*` em `pkgbuilds/` e `vendor/repo/` | Cópias idênticas entre si e fora do índice (que só tinha 1.2.0) |
| `vendor/repo/*.tar.gz.old` | Backups do índice; o `build-aur.sh` reconstrói o índice do zero |
| `__pycache__/` (3) | Cache do Python |
| Clones do NVG-OS-DEBUG e do neovanguard-os-dev | Usados só na comparação |

Continuam no lugar, de propósito: `out/` (ISOs de 10/09, desatualizadas mas não são cópia; refazer exige sudo), `work/` (dono root), `build/perfis/mbn-*`, os assets gerados em `profile-src/` e os pacotes `1.2.0` de `vendor/repo`. Os três últimos a próxima build refaz: `build_rust` chama `build-aur.sh --forcar` para os três pacotes Neovanguard, e `build_assets` roda o `gen-assets.sh`.

## Verificação da árvore reconciliada

Tudo rodado como usuário comum em 11/09/2026, na `main` local:

| Verificação | Resultado |
|---|---|
| `./check` (fmt, clippy `-D warnings`, `cargo test --workspace`) | Aprovado: **182 testes**, incluindo `ida_e_volta_num_relay_local`, que na auditoria original travava por mais de 60 s |
| `cargo test -p nvg-installer` | 67 aprovados, incluindo o do NVG-04 |
| `scripts/test-network-state.py` / `test-network-modes.py` / `test-nft-network.py` | 16 / 14 / 7 aprovados |
| `scripts/check-neo-refs.py`, `check-shortcuts.py`, `test-frost.py`, `test-desktop-controls.py` | Aprovados |
| `./build-iso --check` | **Aprovado**, depois de reconstruir os pacotes (abaixo). Inclui "o índice do repositório local bate com os arquivos", a pendência antiga da [primeira rodada](correcoes-01.md) |
| `scripts/check-network-policies.py` | **Não roda sem root** (lê `/proc/1/ns/net`), ver [correcoes-04](correcoes-04.md) |

**Pacotes reconstruídos.** O primeiro `./build-iso --check` reprovou: o `neovanguard-sovereignty-1.2.0` de `vendor/repo` era de 10/09, anterior ao PR #2, e não tinha `neo-rede.sh`, `neo-network-state.py` nem `network-policies.json`. Rodei `./neo/packaging/build-aur.sh --forcar neovanguard-base neovanguard-installer neovanguard-sovereignty`, o mesmo passo da build, e os três saíram às 18:15–18:19 com todas as correções.

Não foi gerada ISO nem feito boot em VM.

## O que falta corrigir

Os dois itens de código desta lista foram resolvidos na [quinta rodada](correcoes-05.md):

- ~~**NVG-09, Shamir.**~~ Formato `nvgs2` com identificador da divisão e etiqueta de conferência; 21 testes.
- ~~**`check-network-policies.py` exige root.**~~ A guarda lia `/proc/1/ns/net` dentro do `unshare -rn`, onde nem root consegue ler; agora exige namespace novo com só `lo`.

A revisão feita depois achou **três erros novos**, resolvidos na [sexta rodada](correcoes-06.md). Os diagnósticos abaixo foram corrigidos com bloqueio de DNS fora do túnel, endpoints UDP validados e guarda da senha de disco antes dos comandos:

- **NVG-10**: no kill-switch de VPN, DNS para o resolvedor da LAN sai fora do túnel ([cadeia 09](✅-09-killswitch-vpn-saidas-fora-do-tunel.md)).
- **NVG-11**: no mesmo arquivo, UDP 51820/1194 sai para qualquer host, não só para o servidor da VPN ([cadeia 09](✅-09-killswitch-vpn-saidas-fora-do-tunel.md)).
- **NVG-12**: senha de disco vazia com criptografia passa na validação, e o `luksFormat` falha depois de o disco ter sido apagado ([cadeia 10](✅-10-senha-de-disco-vazia.md)).

E continua faltando o que não é código ou depende de você:

1. **Versão repetida.** Os pacotes corrigidos continuam `1.2.0-1`, o mesmo número dos pacotes das ISOs de 10/09. Uma máquina que já tenha a 1.2.0 instalada **não recebe** as correções por `pacman -Syu`. Se a 1.2.0 saiu para alguém, é preciso subir o `VERSION` (1.2.1) ou o `pkgrel` antes da próxima ISO. A decisão é sua.
2. **ISO nova.** As ISOs de `out/` não têm nenhuma correção deste documento. Para gerar: `./build-iso` (pede sudo).
3. **Validação no hardware.** UID do Tor, rádios, hotplug, gerenciadores de rede, isolamento físico do air-gap e o primeiro boot Btrfs + systemd-boot (NVG-04) só foram exercitados em teste, nunca numa máquina ou VM.
4. **Revisão criptográfica do `nvgs2`**, já pedida em `documentation/soberania.md` para o `neo-shamir` como um todo.
5. **Confirmar o CI remoto.** A validação local passou; o resultado do workflow após o merge deve ser conferido no GitHub.
