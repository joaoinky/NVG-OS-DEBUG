# Sexta rodada de correções

Data: 11/09/2026. Escopo: NVG-10, NVG-11 e NVG-12, cadeias 09 e 10.
**Estado final:** publicada junto da quinta rodada no
[PR #5](https://github.com/NEOpisa/neovanguard-os-dev/pull/5), integrado à
`main` no merge `034f0d7` depois do CI completo. A quinta rodada foi preservada.

## Alterações

- **NVG-10:** saída DNS UDP/TCP 53 descartada depois do túnel e antes das
  exceções físicas. LAN sem DNS e DHCP IPv4 permanecem liberados. A ajuda
  explica que VPN sem DNS roteado pelo túnel fica sem resolução.
- **NVG-11:** `neo-vpn.py` descobre todos os endpoints de `wg show IFACE endpoints`
  ou lê `--endpoint IP:porta` repetível, com `[IPv6]:porta`. Valida IP literal,
  faixa de porta, ausência de zona IPv6, endereço não especificado e multicast
  antes de gerar nft. Falhas de descoberta, `(none)`, lista vazia ou valores
  inválidos recusam sem carregar regras. Não há fallback irrestrito.
- A exceção de handshake usa endereço e porta UDP exatos. A inspeção extrai
  somente regras nesse formato e compara o resto do ruleset integralmente.
  A aplicação confere também os endpoints pedidos antes de criar o cache.
- `check-network-policies.py --emit` normaliza o bloco `@ENDPOINTS@` e a
  interface. A saída foi revisada, e o JSON atualizado manualmente. A guarda
  de namespace da quinta rodada continua intacta.
- **NVG-12:** guarda compartilhada em Layout, no plano antes de instalar e
  na entrada de `partition`. Com criptografia, recusa senha vazia, LF, CR e
  NUL antes dos comandos. Um caractere é aceito. Senha de conta não mudou.
- O pacote de soberania instala o helper novo. `build-iso --check` exige sua
  presença no pacote e usa o gerador validado para conferir o template VPN.
- Cadeias renomeadas com `mv` comum para ✅, diagnóstico original preservado,
  status e solução acrescentados. Índice, reconciliação e documentação de
  rede atualizados.

## Evidências

- Instalador: **68 testes aprovados**. Senhas inválidas retornam somente
  `Progress::Done(Err(_))` pelo `spawn`, sem comandos. Layout recusa as mesmas
  entradas e aceita `x`; o plano também aceita `x`.
- Estado de rede: **17 testes aprovados**. Cobrem endpoints obrigatórios,
  IPv4/IPv6, exceção sem destino, prefixo, porta inválida, veredito, ordem de
  DNS e comparação entre endpoints solicitados e observados.
- Comandos de rede: **16 testes aprovados**, incluindo descoberta WireGuard,
  endpoints explícitos, entradas inválidas e falhas antes de aplicar nft.
- Tráfego em namespaces: **10 testes aprovados**. `nvgvpn0` é dummy;
  peer em `192.168.1.1`, `198.18.0.2` e `2001:db8::2`. DNS LAN UDP/TCP,
  UDP para host/porta não autorizados e tráfego público bloqueados; endpoints
  IPv4/IPv6, LAN sem DNS e DHCP permitidos. Conexões novas e anteriores cobertas.
- **Controle negativo:** cópia de `HEAD:neo/etc/nftables/killswitch-vpn.nft.in`
  fornecida por `NVG_TEST_VPN_TEMPLATE`, sem alterar o modelo da árvore.
  Cinco subcasos falharam: DNS LAN UDP/TCP, UDP 51820 e 1194 para host fora
  da lista e porta 1194 não autorizada no endpoint IPv4.
- Referências e sondas de kernel: `check-network-policies.py` aprovado,
  reconhecendo os quatro modos e detectando regras divergentes.
- `neovanguard-sovereignty` e `neovanguard-installer` reconstruídos com
  `./neo/packaging/build-aur.sh --forcar`, antes do verificador de ISO.
  O índice local foi atualizado; o aviso de ausência de símbolos de debug
  do instalador não impediu a construção dos pacotes.
- **`./check` aprovado:** fmt, Clippy sem avisos, **183 testes Rust**,
  dependências de empacotamento, 17 testes de estado, 16 de comandos,
  21 de Shamir e `build-iso --check`. A tentativa restrita pelo sandbox
  parou nos testes de sockets e foi interrompida; a execução completa como
  usuário comum fora do sandbox terminou com código zero.
- Rodada final de `python3 scripts/test-nft-network.py` e
  `python3 scripts/check-network-policies.py`: ambos aprovados.
- `git diff --check`: sem erros. Antes da publicação, `main` estava quatro
  commits à frente de `osdev/main` e esta rodada ainda não estava commitada.
- **CI remoto aprovado:** workflow `check`, execução `34655304586`, em 4m33s.
  Cobriu formatação, Clippy/testes, tráfego de firewall, referências e sondas
  de rede, geração do tema e perfil da ISO.

## Arquivos desta rodada

- `neo/bin/neo-killswitch`
- `neo/etc/nftables/killswitch-vpn.nft.in`
- `neo/lib/neo-vpn.py` (novo), `neo-network-state.py`, `neo-rede.sh`, `network-policies.json`
- `neo/packaging/pkgbuilds/neovanguard-sovereignty/PKGBUILD`
- `rust/nvg-installer/src/app.rs`, `install.rs`
- `scripts/check-network-policies.py`, `test-network-state.py`, `test-network-modes.py`, `test-nft-network.py`
- `build-iso`
- `documentation/verificacao-estado-rede.md`, `testes-firewall-tor.md`
- Nesta pasta: `README.md`, `reconciliacao-2026-09-11.md`, as duas cadeias
  renomeadas para ✅ e este `correcoes-06.md`.
- Artefatos ignorados: pacotes/índice em `vendor/repo`, cópias de empacotamento
  em `vendor/aur`, binários Cargo e perfis compostos pelo verificador.

## Limites e o que ficou de fora

- Sem root no host; regras e interfaces de teste apenas em namespaces
  descartáveis `unshare -rn`. O sandbox bloqueou Netlink e sockets locais;
  as verificações de integração foram executadas fora dele como usuário comum.
  Nenhum firewall, interface ou disco real foi alterado.
- Sem instalação, boot em VM, ISO nova, VPN real, teste de roaming ou
  autenticação do servidor. O dummy prova decisões do firewall; não prova
  conectividade do túnel. Vizinhos IPv6 são resolvidos antes de aplicar regras.
- Somente endpoints UDP; OpenVPN TCP não é suportado. Endpoint na porta 53
  também é bloqueado para manter DNS fora do túnel proibido. Mudanças de IP
  ou porta exigem reaplicar o comando. DNS cifrado/em outra porta não é
  identificado por estas regras. LAN sem DNS permanece exceção deliberada.
- A inspeção comum reconhece a estrutura e relata os endpoints carregados;
  não autentica o servidor. Na aplicação, compara-os com os endpoints pedidos.
- Pacotes continuam `1.2.0-1`. Não houve alteração de versão nem publicação
  de ISO. As ISOs antigas continuam antigas.
- O trabalho Shamir da quinta rodada, a senha de conta vazia e as demais
  pendências da reconciliação não foram alterados.
