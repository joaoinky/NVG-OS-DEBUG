# NVG-26 - Perfil é gravado em arquivo e chave diferentes dos que são lidos

**Estado: corrigido no código em 20/09/2026; PR #33 aberto; validação no sistema instalado pendente.** Gravidade original: **média** no cenário descrito. Base da auditoria: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[neo-first-boot:19 e 122](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/wizard/neo-first-boot#L19), [profile](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/_neo-comum.sh#L85) e [neo_curl](https://github.com/NEOpisa/neovanguard-os-dev/blob/619d7697bf9ff0067a0d314c6456a5183f7a733b/neo/bin/_neo-bitcoin.sh#L99).

O assistente grava `/etc/neovanguard/profile.conf` com `profile=cold`. A biblioteca lê `/etc/neovanguard/perfil.conf`, procura `perfil=` e usa `hot` como fallback. Mesmo um arquivo corretamente gravado, sem a corrupção do NVG-25, não informa o perfil aos consumidores. O painel e decisões condicionadas a `profile`, como o fallback SOCKS de `neo_curl`, recebem Hot.

## Evidência

Em NEO_ETC temporário gravou-se `profile.conf` válido com `profile=cold`. A função real `profile()` retornou `hot`. [Log](evidencias/probes-shell.log).

## Limites da conclusão

É independente do menu capturado: persiste mesmo depois de corrigir NVG-25. Não significa que um firewall já ativo será burlado; a falha está na leitura do perfil e em comportamentos que dependem dela.

## Direção da correção

Adotar um único caminho/esquema compartilhado, prever migração da configuração existente e testar escrita pelo assistente seguida de leitura pelos comandos consumidores.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)

## Correção implementada em 20/09

[PR #33](https://github.com/NEOpisa/neovanguard-os-dev/pull/33), branch `fix/neo-comum-shared-lib`.
Commits de implementação: [`57ef2d2`](https://github.com/NEOpisa/neovanguard-os-dev/commit/57ef2d2), [`a2cb329`](https://github.com/NEOpisa/neovanguard-os-dev/commit/a2cb329).

A elevação com sudo perdia subcomandos já consumidos pelo parser, e o perfil gravado pelo assistente era lido de outro arquivo. A biblioteca preserva os argumentos originais e lê `profile.conf/profile=`, com compatibilidade para `perfil.conf/perfil=`. O formato atual tem precedência; configuração inválida usa `cold` com aviso.

## Validação e limites

57 testes aprovados: biblioteca compartilhada (7), modos de rede (18), estado de rede (17), MAC (8) e dependências de build (7). Sintaxe shell, referências de ajuda dos 56 comandos e `git diff --check` aprovados. Os testes exercitam relançamento de Flash/mesh, limites dos argumentos, persistência do assistente e SOCKS no `neo_curl`.

Não foi executado o assistente completo com sudo, nem gravação de firmware ou transportes mesh reais. NVG-25, sobre o menu capturado na resposta, permanece pendente. `./check quick` completo não foi repetido nesta branch.

As provas originais acima registram o comportamento anterior à correção. O PR ainda não foi integrado à `main`.

[Registro dos cinco grupos](correcoes-2026-09-20.md) · [PR #33](https://github.com/NEOpisa/neovanguard-os-dev/pull/33)
