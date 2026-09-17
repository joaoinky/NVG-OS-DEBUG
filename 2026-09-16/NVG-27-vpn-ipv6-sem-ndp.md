# NVG-27 — Kill-switch impede endpoint IPv6 quando o cache de vizinhos esvazia

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **média** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[killswitch-vpn.nft.in](../../../neo/etc/nftables/killswitch-vpn.nft.in#L19) e [fixture de tráfego](../../../scripts/test-nft-network.py).

O template permite o endpoint UDP IPv6, mas bloqueia Neighbor Solicitation/Advertisement nas interfaces físicas. Sem resolução de vizinhos não se chega ao endpoint, ou ao gateway que o alcança. Os testes anteriores resolvem os vizinhos antes de aplicar o firewall, escondendo esse caso. O túnel pode deixar de reconectar quando o cache expira.

## Evidência

Tráfego UDP real em dois namespaces descartáveis: (1) endpoint IPv6 respondeu com cache aquecido; (2) apenas esvaziar vizinhos fez a mesma troca expirar; (3) permitir somente NDP nas duas cadeias restaurou a mesma troca com cache vazio. [Prova](evidencias/reproduzir-rede.py) e [log](evidencias/probes-network.log). [RFC 4861](https://datatracker.ietf.org/doc/html/rfc4861) define esse mecanismo.

## Limites da conclusão

Não se alterou o firewall do host. A interface de túnel da fixture é dummy; não houve handshake WireGuard/OpenVPN real. Trata-se de indisponibilidade confirmada do transporte IPv6, não de vazamento nem reabertura dos NVG-10/11.

## Direção da correção

Permitir o conjunto mínimo e adequadamente restrito de ICMPv6 necessário ao enlace. Acrescentar testes sem pré-aquecer vizinhos, com expiração de cache e reconexão do túnel real.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
