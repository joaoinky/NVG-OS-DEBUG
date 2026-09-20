# NVG-27 - Kill-switch impede endpoint IPv6 quando o cache de vizinhos esvazia

**Estado: corrigido no código em 20/09/2026; PR #35 aberto; validação no sistema instalado pendente.** Gravidade original: **média** no cenário descrito. Base da auditoria: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[killswitch-vpn.nft.in](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/etc/nftables/killswitch-vpn.nft.in#L19) e [fixture de tráfego](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/scripts/test-nft-network.py).

O template permite o endpoint UDP IPv6, mas bloqueia Neighbor Solicitation/Advertisement nas interfaces físicas. Sem resolução de vizinhos não se chega ao endpoint, ou ao gateway que o alcança. Os testes anteriores resolvem os vizinhos antes de aplicar o firewall, escondendo esse caso. O túnel pode deixar de reconectar quando o cache expira.

## Evidência

Tráfego UDP real em dois namespaces descartáveis: (1) endpoint IPv6 respondeu com cache aquecido; (2) apenas esvaziar vizinhos fez a mesma troca expirar; (3) permitir somente NDP nas duas cadeias restaurou a mesma troca com cache vazio. [Prova](evidencias/reproduzir-rede.py) e [log](evidencias/probes-network.log). [RFC 4861](https://datatracker.ietf.org/doc/html/rfc4861) define esse mecanismo.

## Limites da conclusão

Não se alterou o firewall do host. A interface de túnel da fixture é dummy; não houve handshake WireGuard/OpenVPN real. Trata-se de indisponibilidade confirmada do transporte IPv6, não de vazamento nem reabertura dos NVG-10/11.

## Direção da correção

Permitir o conjunto mínimo e adequadamente restrito de ICMPv6 necessário ao enlace. Acrescentar testes sem pré-aquecer vizinhos, com expiração de cache e reconexão do túnel real.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)

## Correção implementada em 20/09

[PR #35](https://github.com/NEOpisa/neovanguard-os-dev/pull/35), branch `fix/nvg-27-killswitch-ndp`.
Commits de implementação: [`7dfe455`](https://github.com/NEOpisa/neovanguard-os-dev/commit/7dfe455).

O endpoint IPv6 deixava de responder quando o cache de vizinhos esvaziava. O kill-switch permite Neighbor Solicitation e Advertisement nas cadeias de entrada e saída, restritos a Hop Limit 255 e código zero. A referência usada para verificar o firewall acompanha as novas regras.

## Validação e limites

12 testes de tráfego real em namespaces descartáveis e 18 testes de estado aprovados. Conferência das quatro políticas contra regras carregadas pelo kernel aprovada. Casos incluem esvaziamento repetido de vizinhos, endpoint via gateway e manutenção do bloqueio de DNS, ping e tráfego não autorizado.

O firewall do host não foi alterado. A interface de túnel dos testes é dummy; falta reconexão com WireGuard/OpenVPN real, ISO/VM e roaming. `./check quick` completo não foi repetido.

As provas originais acima registram o comportamento anterior à correção. O PR ainda não foi integrado à `main`.

[Registro dos cinco grupos](correcoes-2026-09-20.md) · [PR #35](https://github.com/NEOpisa/neovanguard-os-dev/pull/35)
