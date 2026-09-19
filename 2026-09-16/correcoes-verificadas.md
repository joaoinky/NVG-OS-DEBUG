# Conferência dos problemas anteriormente marcados como resolvidos

Este documento preserva a conferência de 16/09. As correções posteriores de
NVG-29, NVG-30 e NVG-17 estão no [registro de 18/09](correcoes-2026-09-18.md).

Base auditada: `619d7697bf9ff0067a0d314c6456a5183f7a733b`. Trabalho iniciado em 15/09 e concluído em 16/09/2026. “Sim” abaixo significa que a correção do **defeito originalmente descrito** está presente e foi sustentada pela leitura e pelas verificações indicadas. Não significa que todos os caminhos daquela funcionalidade estejam corretos, nem que a ISO tenha sido testada.

## Lista simples - os 12 erros numerados

| Problema anterior | Foi resolvido? | O que foi conferido agora |
|---|---|---|
| NVG-01 - apóstrofo na senha quebra a criação da conta | **Sim, no código e nos testes.** | Senha enviada como dados para chpasswd; regressão do instalador passou. |
| NVG-02 - campos da conta interpretados como comandos | **Sim, no código e nos testes.** | Validação e escape de argumentos; nome chega literalmente ao useradd. |
| NVG-03 - preservar raiz junto de criar LUKS apaga a raiz | **Sim, no código e nos testes.** | Combinação recusada na interface, no plano e antes da etapa de particionamento. |
| NVG-04 - boot normal Btrfs sem selecionar `@` | **Sim, na geração da entrada.** | `rootflags=subvol=@` presente no caminho correto; regressão passou. Boot real pendente. |
| NVG-05 - painel confia em marcador Tor obsoleto | **Sim, no código e nos testes.** | Estado observado, comparação das regras e invalidação do cache; sondas reais em namespace passaram. |
| NVG-06 - conexões diretas anteriores atravessam bloqueio | **Sim, nas políticas e no tráfego testado.** | Regressões com sessões anteriores, regras carregadas no kernel de namespace descartável. |
| NVG-07 - DNS da LAN contorna Tor | **Sim, nas políticas e no tráfego testado.** | Ordem de redirecionamento/bloqueio e consultas cobertas pela suíte de rede. |
| NVG-08 - air-gap anuncia sucesso apesar de falha | **Sim, no tratamento de falhas testado.** | Falhas simuladas de isolamento/observação impedem sucesso e marcador confiável. Isolamento físico pendente. |
| NVG-09 - misturar partes Shamir recupera outra seed válida | **Sim, na regressão descrita.** | 21 testes: conjuntos diferentes, formato novo e compatibilidade legada. Revisão criptográfica independente continua pendente. |
| NVG-10 - DNS da LAN sai fora da VPN | **Sim, no tráfego testado.** | DNS TCP/UDP fora do túnel bloqueado antes das exceções de LAN. |
| NVG-11 - portas UDP da VPN liberadas para qualquer destino | **Sim, no tráfego testado.** | Exceção exige endpoint/porta validados; destinos e portas não autorizados recusados. |
| NVG-12 - senha LUKS vazia falha depois de apagar disco | **Sim, no código e nos testes.** | Vazio/LF/CR/NUL recusados antes de comandos; senha de um caractere continua permitida. |

Fontes das alegações: [índice anterior](../2026-09-09/README.md) e seus dez diagnósticos, [rodadas 01–07](../2026-09-09/correcoes-07.md), [CHANGELOG](../../../CHANGELOG.md). Evidências atuais: [68 testes do instalador](evidencias/cargo-test-unsandboxed.log), [estado de rede](evidencias/test-network-state.log), [modos de rede](evidencias/test-network-modes-with-jq.log), [tráfego nft](evidencias/test-nft-network-unsandboxed.log), [políticas observadas](evidencias/check-network-policies-unsandboxed.log) e [Shamir](evidencias/test-neo-shamir.log).

Os novos [NVG-16](❌-16-boot-vault-perde-parametros.md) e [NVG-27](❌-27-vpn-ipv6-sem-ndp.md) afetam, respectivamente, **outro gerador de entrada de boot** e **a conectividade IPv6 com cache vazio**. Não são a reaparição do NVG-04 nem dos vazamentos NVG-10/11.

## Outras correções anunciadas em changelog, notas e documentação

Este inventário inclui as alegações de [1.2.0](../../notas-de-versao/1.2.0.md), [1.2.1](../../notas-de-versao/1.2.1.md), [Frost](../../frost.md) e [escopo de segurança](../../security-review-scope.md). “Parcial” distingue alteração presente de efeito final ainda não verificado; não acusa uma falha sem evidência.

| Alegação | Resultado desta auditoria |
|---|---|
| Proteção das mídias atuais/antigas no instalador | **Parcial.** Detecção por rótulos e bloqueio no modo apagar existem; seleção manual contorna a proteção: **NVG-13**. |
| fstab sem destinos duplicados, incluindo `/var/log` | **Sim, na função e na regressão automatizada.** Montagens finais ainda exigem instalação. |
| Hook `encrypt` no drop-in efetivo; presets sem `ALL_config` que o desabilite | **Presente no código.** Initramfs gerado e desbloqueio no boot ainda não certificados. |
| Versão dos três pacotes lida corretamente também em cópia de build | **Presente nos PKGBUILDs.** Leitura de `VERSION` e busca da raiz verificadas; `.PKGINFO` de novos pacotes não foi produzido nesta sessão. |
| Dependências de execução dos pacotes próprios não instaladas no host pelo build | **Sim no fluxo e nas regressões de build.** 7 testes passaram. |
| setuptools no PKGBUILD local de flask-restx | **Sim na declaração e nos testes.** Não se reconstruiu flask-restx/Core Lightning nesta sessão. |
| Separar dependências oficiais/AUR, preservar restrições e ordem sem duplicação | **Sim no fluxo e nos testes de build.** Resolução completa atual do AUR depende de novo build. |
| Modo não interativo, cache/forçar, falhas obrigatórias e resumo do build | **Sim na lógica testada.** Não se reproduziu um workflow remoto completo. |
| WireGuard presente no perfil e ferramenta ausente distinta de peer sem endpoint | **Sim nos fontes e nos 18 testes de modos.** Conteúdo binário da ISO e VPN real pendentes. |
| MAC usa `/dev/urandom`, recusa leitura curta e propaga falhas parciais | **Sim nos 8 testes.** Troca/restauração de interface física não executada. |
| Serviço do agente pode criar IPC e abrir sockets IP mantendo home somente leitura | **Sim.** Política systemd real aplicada a teste sintético; IPC, IPv4/IPv6 e NIP-46 passaram. |
| Agente expira sem tráfego e limita leitura de IPC/prompt | **Sim nos caminhos e testes existentes.** Não equivale a uma prova de resistência a todas as formas de exaustão de recursos. |
| Cancelamento remoto NIP-46 e formato NIP-04 | **Sim nas implementações e testes existentes.** Compatibilidade com clientes externos reais permanece pendente. |
| Relay usa banco em `/run` com diretório gerenciado pelo systemd | **Presente e consistente entre configuração/unidade.** Persistência efetiva, reinício e isolamento de clientes aguardam sistema instalado. |
| Formatação obrigatória e resolução Cargo com lockfile | **Sim na configuração.** fmt e Clippy passaram. A suíte atual não ficou toda verde: **NVG-28**. |
| CI gera recursos antes da validação e inicializa chaveiro Arch | **Presente na ordem dos workflows.** Não se executou CI/build de ISO. |
| Actions atualizadas para versões destinadas ao Node 24 | **Referências locais conferidas** (`checkout@v7`, `cache@v6`, `upload-artifact@v7`). Manifests remotos e execução dessas versões não foram revalidados. |
| CI guarda somente checksums por 14 dias e remove destino antigo | **Presente no workflow.** Upload, quotas, artefatos e publicação remota não foram consultados. |
| Reaplicação de cores/accent e materialização Birfree no KConfig | **Lógica coberta pelos testes Rust passou.** Aplicação na sessão Plasma real pendente. |
| Layout por tela, acessibilidade Orca e metadados dos plasmoides | **Alterações presentes; efeito final não certificado.** Exigem sessão gráfica, múltiplos monitores e tecnologia assistiva. |

### Correções enumeradas na documentação Frost

| Item do documento original | Resultado |
|---|---|
| 1 - um único wallpaper oficial | **Sim nos fontes e no teste.** Recurso instalado pelo gerador foi conferido. |
| 2 - instalador transfere os novos componentes visuais | **Sim na lista e na regressão estática.** Presença no disco instalado pendente. |
| 3 - ciclo de persistência dos favoritos | **Inicialização/gravação separadas no código.** Carregamento completo do launcher em KWin não foi repetido; não certificar funcionamento visual só por inspeção. |
| 4 - brilho não chega a zero nem seleciona LED de teclado | **Sim no helper e no teste:** mínimo 5%, classe backlight. Hardware pendente. |
| 5 - estado não depende do idioma e distingue Wi-Fi habilitado de adaptador presente | **Sim no helper e nas regressões sintéticas.** Integração real pendente. |
| 6 - controles comunicam falhas dos comandos | **Sim nos testes de falha e no código de tratamento.** Apresentação visual completa pendente. |
| 7 - primeiro login só grava marcador após sucesso | **Guarda de sucesso presente em `nvg-first-session`.** Primeiro login real não executado. É outro programa que o assistente `neo-first-boot` afetado pelo NVG-25. |
| 8 - metadados de tamanho do índice local corrigidos | **Não revalidável sem aqueles artefatos.** Testes do indexador passaram; o repositório binário desta cópia está ausente. |
| 9 - largura/cartões do painel de controles | **Alteração de layout presente.** Não foram repetidas capturas e comparação visual nas resoluções alvo. |
| 10 - riscos/emendas a cada 12 px no FrameSvg | **Correção estrutural confirmada:** hint de esticar bordas e ausência do stroke problemático; teste passou. Aparência sob compositor real pendente. |
| 11 - Meta abre o menu pelo atalho atual do plasmashell | **Configuração e verificador de atalhos passaram.** Tecla e compositor reais não exercitados. |

Além disso, os testes Qt de login e seek passaram: 10 casos funcionais e 4 entradas de inicialização/limpeza. Isso não autentica um login PAM nem testa hardware de áudio/vídeo.

## Alegações históricas que não viraram certificação atual

- Registros de “183 testes passaram”, pacotes reconstruídos, CI verde e publicação descrevem execuções antigas. A execução desta auditoria observou **182 testes Rust aprovados e 1 reprovado**, antes das provas adicionais. O resultado atual está documentado no NVG-28.
- `correcoes-07.md` ainda diz “sem merge”, mas o HEAD local é o merge do PR #7 e contém a rodada. É desatualização do registro histórico, não ausência local da correção.
- Não se consultaram todos os repositórios remotos, branches, PRs, binários publicados ou instalações existentes. Não se presume que código corrigido já esteja distribuído aos usuários.
- A revisão de segurança do pacote não cobre automaticamente toda restauração: os **NVG-17/18/19** comprovam limites concretos. A validação de eventos do cliente Rust também não se estende ao helper Python, afetado pelo **NVG-29**.

[Índice e novos problemas](README.md) · [Testes ainda necessários](pendencias-iso-vm-hardware.md)
