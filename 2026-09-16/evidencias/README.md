# Evidências e reprodução

Base dos testes: `619d7697bf9ff0067a0d314c6456a5183f7a733b`. Os registros foram coletados em 15–16/09/2026. Ferramentas relevantes: Rust/Cargo 1.98.1, Python 3.14 e Qt 6.11.1 no host de auditoria. Essas versões não descrevem necessariamente o conteúdo de uma futura ISO.

Rust, Cargo, jq e bibliotecas necessárias que faltavam foram extraídos para uma área temporária, sem instalar pacotes no sistema. Cache Cargo e saídas de compilação também ficaram em `/tmp/nvg-audit-2026-09-15/`. Os testes originais foram executados contra os fontes do repositório; os testes Rust novos foram acrescentados somente a uma **cópia temporária**.

## Suítes existentes

| Comando / conjunto | Resultado | Registro |
|---|---|---|
| `cargo fmt --all --check` | Passou; saída vazia é normal | [fmt.log](fmt.log) |
| `cargo clippy --locked --offline --all-targets --workspace -- -D warnings` | Passou | [clippy.log](clippy.log) |
| `cargo test --locked --offline --workspace` | Instalador: 68 passaram; biblioteca Nostr: 55 passaram, 1 falhou | [cargo-test-unsandboxed.log](cargo-test-unsandboxed.log) |
| Continuação: `cargo test --locked --offline -p nvg-nostr-agent -p nvg-palette -p nvg-theme -p nvg-update` | 58 passaram, incluindo doctest | [cargo-test-restante.log](cargo-test-restante.log) |
| `cargo test --locked --offline -p nvg-nostr --test cofre_ponta_a_ponta` | 1 passou | [cofre-e2e.log](cofre-e2e.log) |
| `python3 scripts/test-build-deps.py` | 7 passaram | [log](test-build-deps.log) |
| `python3 scripts/test-network-state.py` | 17 passaram | [log](test-network-state.log) |
| `python3 scripts/test-network-modes.py` | 18 passaram, com jq disponível | [log](test-network-modes-with-jq.log) |
| `python3 scripts/test-neo-mac.py` | 8 passaram | [log](test-neo-mac.log) |
| `python3 scripts/test-neo-shamir.py` | 21 passaram | [log](test-neo-shamir.log) |
| `python3 scripts/test-indexed-packages.py` | 5 passaram com fixtures | [log](test-indexed-packages.log) |
| `python3 scripts/test-frost.py` | 12 passaram após gerar o wallpaper esperado | [log](test-frost-with-assets.log) |
| `python3 scripts/test-desktop-controls.py` | 5 passaram com serviços simulados | [log](test-desktop-controls.log) |
| `python3 scripts/test-nft-network.py` | 10 passaram, tráfego em namespaces | [log](test-nft-network-unsandboxed.log) |
| `python3 scripts/check-network-policies.py` | 4 políticas e sondas de kernel/cache aprovadas | [log](check-network-policies-unsandboxed.log) |
| Qt Quick Test, login e seek | 14 resultados aprovados: 10 casos + 4 setup/cleanup | [qml-tests-qt6.log](qml-tests-qt6.log) |
| Política systemd do agente + NIP-46 | Passou; teste existente com localização do binário adaptada | [test-agent-service.log](test-agent-service.log) |
| `check-neo-cli.py`, `check-installer-calls.py`, `check-shortcuts.py` | 55 comandos, 4 chamadas e atalhos aprovados | [CLI](check-neo-cli.log), [instalador](check-installer-calls.log), [atalhos](check-shortcuts.log) |
| `check-ordem-aur.py` | Ordem aprovada; sem pacotes construídos para inspecionar | [log](check-ordem-aur.log) |
| Sintaxe dos arquivos próprios versionados | 84 Bash/PKGBUILD, 37 Python e 10 JSON; zero falhas | [sintaxe.json](sintaxe.json) |
| `./build-iso --check` | **Código 1; não aprovado integralmente** | [build-iso-check.log](build-iso-check.log) |

Os comandos Cargo da tabela usam `rust/` como diretório de trabalho ou `--manifest-path rust/Cargo.toml`. O total Rust original é **182 aprovados + 1 reprovado = 183**; não se contam novamente os testes repetidos nas sondas posteriores. A falha é o teste dependente de GPU do NVG-28. O total Python das nove suítes com contagem é **103 aprovados**.

Para Qt foi usado:

```sh
QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software \
  /usr/lib/qt6/bin/qmltestrunner -input scripts/qml -o -,txt
```

Para verificar sintaxe, foram percorridos arquivos de `git ls-files`, excluindo vendor, saídas geradas e powerlevel10k; Bash foi analisado com `bash -n`, Python com `compile()` sem executar e JSON com `json.loads()`. Isso não é análise semântica nem abrange dependências externas.

### Como interpretar as tentativas que não passaram

- A tentativa Rust inicial dentro do sandbox não conseguiu exercitar adequadamente sockets e ficou aguardando o teste de relay. A execução com permissões adequadas concluiu esse teste; o processo bloqueado foi encerrado ao final. O bloqueio ambiental não foi contado como falha da distro.
- A ausência inicial de jq fez falhar a suíte de modos; após disponibilizá-lo, os 18 testes passaram.
- `test-frost.py` inicialmente não encontrou o wallpaper instalado. `python3 branding/install-wallpapers.py` materializou o recurso ignorado pelo Git e os 12 testes passaram. Não foi classificado como bug.
- `test-agent-service.py` primeiro tentou executar um binário em `/tmp`, ocultado por `PrivateTmp=yes`. A prova [reproduzir-politica-agente.py](reproduzir-politica-agente.py) executa o mesmo teste e a mesma política, copiando somente o binário para um diretório temporário dentro do checkout. Esse diretório é removido ao sair. IPC, sockets IP, home somente leitura e integração NIP-46 passaram. A primeira revisão automática de permissão expirou; a repetição permitida foi aprovada.
- `build-iso --check` compôs os dois perfis e verificou, entre outros, sintaxe, rótulos/colisões, linhas de boot, chamadas do instalador, atalhos, QML e versão. Não obteve aprovação integral: encontrou o **falso diagnóstico NVG-32**, restrições de Netlink/systemd no sandbox e recursos do tema ainda não materializados pelo gerador completo. Pacotes/índice local ausentes fizeram verificações de artefatos serem explicitamente omitidas. Tráfego nft e política do agente foram validados separadamente, com permissões apropriadas. Não se chamou esse resultado de build de ISO nem de `./check` verde.

## Provas dos problemas novos

**Nestas provas, uma asserção aprovada significa que o defeito foi reproduzido.** Elas não corrigem o produto e devem falhar ou mudar de expectativa quando a correção correspondente for implementada.

Executar a partir da raiz do repositório, como usuário comum. Pré-requisitos conforme a prova: Python, Bash, jq, tar/zstd, Rust/Cargo, iproute2, nftables, user namespaces e, para a política do agente, uma sessão systemd de usuário. Algumas restrições de sandbox impedem sockets/Netlink/auditoria do useradd; os logs informam o ambiente em que foram executadas.

| Relatórios | Prova | Saída registrada |
|---|---|---|
| NVG-13/14/15/17/18/19 | [preparar-provas-rust.py](preparar-provas-rust.py): copia fontes e acrescenta seis testes | [rust-probes.log](rust-probes.log) |
| NVG-15, recusa real de conta existente | [reproduzir-conta-reservada.py](reproduzir-conta-reservada.py): useradd com `--prefix` descartável | [probe-conta-reservada.log](probe-conta-reservada.log) |
| NVG-16/20/21/22/23/24/25/26 | [reproduzir-shell.py](reproduzir-shell.py): funções/scripts reais com comandos externos simulados | [probes-shell.log](probes-shell.log) |
| NVG-27 | [reproduzir-rede.py](reproduzir-rede.py): tráfego real com cache IPv6 vazio e controle NDP | [probes-network.log](probes-network.log) |
| NVG-28 | [reproduzir-teste-gpu.py](reproduzir-teste-gpu.py): mesmo teste, lspci NVIDIA/Intel controlado | [probe-gpu.log](probe-gpu.log) |
| NVG-29/30 | [reproduzir-nostr-pagamento.py](reproduzir-nostr-pagamento.py): transporte e pagador simulados | [probes-nostr-payment.log](probes-nostr-payment.log) |
| NVG-31 | [reproduzir-tags-cli.py](reproduzir-tags-cli.py): CLI real e socket IPC fictício | [probe-tags-cli.log](probe-tags-cli.log) |
| NVG-32 | [reproduzir-referencia-pacman.py](reproduzir-referencia-pacman.py): consultas somente leitura | [probe-referencia-pacman.log](probe-referencia-pacman.log) |

Exemplos:

```sh
python3 documentation/auditoria-erros/2026-09-16/evidencias/reproduzir-shell.py
python3 documentation/auditoria-erros/2026-09-16/evidencias/reproduzir-nostr-pagamento.py
python3 documentation/auditoria-erros/2026-09-16/evidencias/reproduzir-rede.py
python3 documentation/auditoria-erros/2026-09-16/evidencias/reproduzir-teste-gpu.py
```

As provas Rust não alteram os fontes originais:

```sh
audit_rust_copy=$(python3 documentation/auditoria-erros/2026-09-16/evidencias/preparar-provas-rust.py)
cargo test --locked --manifest-path "$audit_rust_copy/Cargo.toml" \
  -p nvg-installer -p nvg-nostr auditoria -- --nocapture
```

Usar `--offline` se as dependências já estiverem no cache. A filtragem por `auditoria` também executa um teste antigo de log do cofre; ele não integra os seis testes novos. O diretório temporário da cópia é preservado para inspeção e pode ser removido depois.

A prova de tags usa `rust/target/debug/nvg-nostr` por padrão. Para outro diretório de build, fornecer o caminho absoluto por `NVG_AUDIT_BINARY`. O socket é novo, sob um `XDG_RUNTIME_DIR` temporário; o agente real não é consultado.

O useradd da prova só opera com `--prefix` em uma árvore fictícia criada pelo script. O teste de rede recusa executar se o namespace não for diferente do inicial e não começar exclusivamente com loopback; as regras são carregadas somente nesse namespace. Não executar manualmente comandos extraídos desses scripts fora de suas guardas.

## Integridade e limites

Cada relatório aponta para os fontes originais e separa o que foi observado do efeito final ainda inferido. Mocks são usados em ações que poderiam atingir discos, rádios, firmware ou fundos; o comportamento interno relevante do script é preservado. Não foram usadas seeds, credenciais, contas ou faturas pessoais.

O [inventário](inventario.json) lista os vinte relatórios. Os caminhos temporários nos logs documentam a execução; não são dependências fixas dos arquivos de prova. O [índice principal](../README.md) e a [matriz de validação](../pendencias-iso-vm-hardware.md) delimitam as conclusões.
