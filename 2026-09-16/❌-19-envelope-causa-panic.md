# NVG-19 - Tamanho não autenticado do envelope pode abortar o processo

**Estado: confirmado; correção não implementada nesta auditoria.** Gravidade: **média** no cenário descrito. Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b` (1.2.1 em preparação).

## Onde e como acontece

[configs::decifrar:307](../../../rust/nvg-nostr/src/configs.rs#L307).

O campo JSON `bruto` controla `Vec::with_capacity(env.bruto as usize)` antes da decifragem/autenticação dos blocos. Um envelope pequeno com `bruto=18446744073709551615` provoca `capacity overflow`, em vez de retornar um erro de entrada inválida. A função é usada pela CLI e pelo instalador; o perfil release usa `panic=abort`.

## Evidência

A prova `auditoria_envelope_nao_autenticado_causa_panic` passa um JSON com versão/algoritmo reconhecidos, esse tamanho e nenhum bloco. `catch_unwind` captura o panic antes de qualquer bloco ser autenticado. Não há alocação massiva na prova. [Resultado](evidencias/rust-probes.log). O comportamento é definido pela documentação de [Vec::with_capacity](https://doc.rust-lang.org/std/vec/struct.Vec.html#method.with_capacity).

## Limites da conclusão

Foi demonstrado abortamento lógico, não execução de código nem quebra da criptografia. Um caminho que rejeite um hash fixado antes de chamar a função pode impedir o ataque específico; a API e seus chamadores não possuem todos essa barreira.

## Direção da correção

Validar e limitar tamanho e número de blocos antes da reserva; usar conversão e reserva falíveis e limite acumulado ao decifrar. Transformar entradas inválidas em `Err`, inclusive no build release.

[Índice da auditoria](README.md) · [Como executar as provas](evidencias/README.md) · [Validação em ISO/VM/hardware](pendencias-iso-vm-hardware.md)
