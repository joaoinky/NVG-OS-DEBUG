# O que falta verificar com build, VM, instalação ou hardware

Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b`, versão-fonte 1.2.1 em preparação. Esta auditoria não construiu uma ISO, não instalou o sistema e não iniciou VM. Testes de funções, tráfego em namespaces e QML offscreen não substituem essas etapas.

Os [20 problemas confirmados](README.md) não são hipóteses pendentes: já possuem evidência própria. A matriz abaixo trata do comportamento final ainda não certificado, inclusive da validação necessária depois de corrigi-los. Fazer os testes destrutivos em discos/imagens descartáveis, com snapshots e identidades fictícias.

## Atualização de 20/09

Oito achados foram corrigidos nos cinco grupos, com PRs #32 a #36 abertos.
O [registro consolidado](correcoes-2026-09-20.md) detalha os testes.
NVG-19/28, NVG-21/26, NVG-22, NVG-27 e NVG-24/32 têm correção no código,
mas ainda precisam de integração e das verificações abaixo. Os testes de
cada branch não substituem uma execução com todas as correções reunidas.

## Matriz mínima de validação

Atualização de 18/09: NVG-29, NVG-30 e NVG-17 foram corrigidos e integrados.
O [registro da rodada](correcoes-2026-09-18.md) documenta as regressões,
o pagamento CLN em regtest e a execução do escritor do cofre com UID 0 em
namespace. Esses resultados reduzem as lacunas abaixo, mas não substituem
a validação conjunta da main, a ISO nem testes com usuários distintos.

| Área | Por que o código/teste atual não basta | Procedimento necessário e critério de aprovação |
|---|---|---|
| Build limpo e pacotes | Não foram reconstruídos AUR, pacotes próprios, índice ou payload. NVG-28 e NVG-32 foram corrigidos em branches ainda não integradas. | Em ambiente Arch limpo, construir todos os pacotes obrigatórios e ambas as imagens atuais (MBN Live/Install). Conferir `VERSION`, `.PKGINFO`, dependências, assinaturas, conteúdo, índice e checksums; nenhuma falha obrigatória pode ser ocultada. |
| Conteúdo final da ISO | Presença no fonte/PKGBUILD não prova presença no squashfs. | Inspecionar imagens: binários/helpers/serviços da versão correta, tema e recursos, ausência de colisões de propriedade e programas exclusivos da instalação fora da Live. Guardar hashes e inventário. |
| Boot Live e Install | Não se executaram kernel/initramfs, descoberta da mídia e payload reais. | Inicializar ambas em UEFI/OVMF e BIOS quando suportado; testar Install como CD-ROM e USB, online/offline. Origem/payload corretos, sem depender da máquina de build. |
| Instalação automática | Testes Rust não particionam nem montam sistemas de arquivos. | Discos virtuais vazios com ext4/Btrfs/XFS, UEFI e BIOS suportados, criptografia ligada/desligada. Concluir instalação offline, retirar ISO e reiniciar pelo disco. Conferir fstab, UUIDs, subvolumes e ausência de montagem duplicada. |
| Particionamento manual | NVG-13/14 demonstram pré-validação insuficiente; preservação precisa de teste de dados reais. | Selecionar mídia de origem, partições sobrepostas, ESP inválida/pequena, raiz pequena e aliases: recusar antes de escrita. Instalar em layouts válidos mantendo ESP/home e arquivos sentinela; comparar hashes antes/depois. |
| Conta, senha e login | Passagem literal ao comando não prova configuração PAM, grupos e sudo no alvo. | Testar apóstrofo, espaços e símbolos permitidos; recusar nomes reservados antes de particionar. Login TTY/SDDM, sudo, conta Live removida, autologin Live removido. Testar senha vazia somente conforme a política já escolhida pelo projeto. |
| LUKS/initramfs/boot Btrfs | Fonte do drop-in e string de boot não demonstram o initramfs efetivo. NVG-16 afeta a entrada Vault. | Inspecionar hooks/presets e conteúdo do initramfs construído; testar senha correta/incorreta, prompt Plymouth/TTY, raiz `@`, boot normal e Vault, atualização de kernel e reboot subsequente. |
| Primeiro boot e perfis | NVG-26 foi corrigido; NVG-25 ainda impede capturar corretamente as escolhas. Testes não executaram o assistente completo com sudo. | Após correção, executar Hot/Cold, Tor/híbrido/kill-switch, nó e identidade; conferir estado real de serviços/rede, configuração persistida, conclusão somente após sucesso e comportamento de `--refazer`. |
| Tor, VPN e DNS | Namespaces testaram decisões de firewall, não daemon Tor, handshake, DNS do túnel ou servidores reais. NVG-27 passou com cache vazio e gateway em namespaces; handshake real continua pendente. | Em VM com captura fora e dentro do túnel, testar IPv4/IPv6, UDP/TCP 53, sessões anteriores, reinício/queda de Tor/VPN, endpoint incorreto, mudança de IP/porta, vizinhos vazios/expirados e roaming. Nenhuma saída proibida; conectividade permitida precisa funcionar. Documentar a exceção deliberada de LAN. |
| Air-gap e Cold Vault | Estado de software não prova ausência de rádio nem interfaces não previstas. | Em hardware, verificar Ethernet/Wi-Fi/Bluetooth/USB tethering, módulos, rfkill, interfaces virtuais e hotplug. Falha em qualquer corte/observação deve impedir confirmação de isolamento. Conferir comportamento após reboot/suspensão. |
| Secure Boot | O firmware e as chaves inscritas não foram tocados; NVG-23 mostra falso sucesso. | Primeiro em OVMF descartável: setup, assinatura, verificação, ativação e reboot; falha parcial deve bloquear confirmação. Depois hardware dedicado, com recuperação preparada; testar atualização de kernel/bootloader. |
| Cofre e restauração | NVG-17/18/19 cobrem defeitos concretos; não esgotam corridas, limites e limpeza de segredos. | Depois das correções, testar pacote válido/malformado, expansão excessiva limitada, symlinks e troca concorrente no destino, permissões/ownership sob root, interrupção, espaço cheio e restauração pela instalação. Nada pode sair da área autorizada; falhas devem preservar estado recuperável. |
| Agente e clientes Nostr | Teste local NIP-46 e sandbox passou, mas clientes gráficos/reais não foram exercitados. | Identidade descartável: prompt real, recusa/timeout, lock/idle, suspensão, desconexão, cancelamento e concorrência. Testar NIP-04/NIP-44/NIP-46 com clientes compatíveis e eventos inválidos; não usar identidade pessoal. |
| Relay, sincronização e limpeza | NVG-20/22/29/31 possuem regressões automatizadas com transporte simulado, incluindo 501 notas no mesmo instante e retomada por destino. Falta relay distribuído real. | Dois relays isolados: várias notas offline, falhas parciais, duplicados, perfis forjados e exclusão autorizada. Conferir persistência em `/run`, vida útil após restart/reboot e confirmação de publicação por destino. |
| Lightning/Bitcoin/Liquid | Em 18/09, CLN teve liquidação real em regtest e recusou três faturas inválidas; HTTP LNURL e LND tiveram cobertura simulada. ISO e LND real ainda não foram validados. | Repetir no sistema instalado com fundos fictícios, incluir LND real, erro de nó, callback inválido, indisponibilidade e limites de taxas. Conferir destino autenticado, valor em msat e resultado antes de anunciar pagamento. Não validar com dinheiro real. |
| Mesh, flash e mídia removível | NVG-21 passou nas regressões de relançamento com argumentos preservados; transportes e gravação real não foram executados. | Após correção, validar relançamento normal/sudo e destino efetivo; gravar apenas mídia descartável e verificar conteúdo. Bluetooth PAN/Wi-Fi Direct entre duas máquinas, descoberta e acesso ao relay na interface anunciada. |
| Plasma/Frost/SDDM | QML offscreen testou lógica, não PAM, compositor, blur, renderização e ergonomia completas. | Primeiro login, favoritos/recentes, atalhos Meta/Meta+A, dock, troca sucessiva de cores, bloqueio, mídia, teclado e logout. Testar 800×600 a 4K/ultrawide, escala fracionária, múltiplos monitores e hotplug. Registrar capturas e erros. |
| GPU, energia e acessibilidade | Detectores/helpers tiveram testes sintéticos; efeitos físicos não foram medidos. | Intel/AMD/NVIDIA disponíveis, Wayland, software rendering, suspender/retomar, áudio, Wi-Fi, Bluetooth e brilho. Orca/leitor de tela, foco, teclado virtual e contrastes em sessão real. |
| Atualizações e entrega | Um merge de fonte não distribui pacotes. Artefatos remotos não foram conferidos. | Em instalação descartável 1.2.0, atualizar pelo repositório efetivamente configurado. Conferir assinatura/versão de cada pacote, hooks, boot e regressões após `pacman -Syu`. Verificar checksums contra imagens correspondentes e conteúdo que foi realmente publicado. |
| Formulário em papel | NVG-24 corrigido: geometria e PDFs de 12/24 palavras renderizados e inspecionados em uma página A4; falta impressão física. | Renderizar PDF de 12/24 palavras, conferir todos os elementos dentro da página e impressão em escala correta. Usar somente palavras fictícias. |

## Limites que uma VM, sozinha, não resolve

- **Revisão criptográfica independente:** Shamir/nvgs2, derivação de chaves, parâmetros NIP-49, uso de NIP-04/NIP-44, resistência a adulteração e exposição de segredos em memória. Testes atuais demonstram casos específicos, não uma prova criptográfica.
- **Dependências e cadeia de fornecimento:** não houve auditoria integral de Rust crates, kernel, Arch/AUR, software vendorizado, binários externos ou todas as vulnerabilidades publicadas. O lockfile fixa resolução, não garante ausência de vulnerabilidades.
- **Firmware e isolamento físico:** Secure Boot, rádios, DMA, GPU, recuperação e comportamento de dispositivos exigem equipamentos reais representativos.
- **Distribuição e serviços externos:** CI atual, relays públicos, GitHub, AUR e repositórios de atualização podem mudar. Esta sessão não verificou sua disponibilidade nem o estado de todas as publicações remotas.
- **Cobertura:** revisão ampla dos componentes próprios e testes dirigidos não permite afirmar que não existam outras falhas. Não foi feita prova formal nem campanha longa de fuzzing/concorrência.

## Evidência a guardar em cada execução

Registrar commit, versões dos pacotes, hashes da ISO, firmware/configuração da VM, layout de disco, passos, resultado esperado/obtido, logs de boot/instalação e capturas pertinentes. Para rede, guardar topologia e captura externa ao convidado; para dados, hashes dos arquivos sentinela. Remover segredos dos registros.

Uma aprovação de release só deve ser atribuída ao artefato e cenário efetivamente testados. Os resultados anteriores de outra ISO ou outro commit não são transferíveis automaticamente.
