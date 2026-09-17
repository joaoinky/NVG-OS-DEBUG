# NVG-26 — Perfil é gravado em arquivo e chave diferentes dos que são lidos

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **média** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-first-boot:19 e 122](../../../neo/wizard/neo-first-boot#L19), [profile](../../../neo/bin/_neo-comum.sh#L85) e [neo_curl](../../../neo/bin/_neo-bitcoin.sh#L99).

O assistente grava `/etc/neovanguard/profile.conf` com `profile=cold`. A biblioteca lê `/etc/neovanguard/perfil.conf`, procura `perfil=` e usa `hot` como fallback. Mesmo um arquivo corretamente gravado, sem a corrupção do NVG-25, não informa o perfil aos consumidores. O painel e decisões condicionadas a `profile`, como o fallback SOCKS de `neo_curl`, recebem Hot.

## Evidência

Em NEO_ETC temporário gravou-se `profile.conf` válido com `profile=cold`. A função real `profile()` retornou `hot`. [Log](evidencias/probes-shell.log).

## Limites da conclusão

É independente do menu capturado: persiste mesmo depois de corrigir NVG-25. Não significa que um firewall já ativo será burlado; a falha está na leitura do perfil e em comportamentos que dependem dela.

## Direção da correção

Adotar um único caminho/esquema compartilhado, prever migração da configuração existente e testar escrita pelo assistente seguida de leitura pelos comandos consumidores.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
