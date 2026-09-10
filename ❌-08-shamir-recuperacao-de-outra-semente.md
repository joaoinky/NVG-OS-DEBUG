# Cadeia 08 — Partes de divisões diferentes produzem “seed reconstruída”

Erro: **NVG-09**. Impacto: alto, recuperação silenciosa de uma identidade diferente. Verificação: funções reais exercitadas em memória com dados sintéticos.

## Walkthrough

1. Duas sementes distintas são divididas com o mesmo mínimo e a mesma quantidade de partes.
2. O formato de cada parte contém versão, mínimo, total, índice, bytes e checksum local. Não contém uma identificação da divisão: [neo/bin/neo-shamir:196](../neovanguard-os-dev/neo/bin/neo-shamir:196).
3. Durante a recuperação, `cmd_juntar()` compara o mínimo e rejeita índices duplicados. Uma parte de cada divisão, com índices distintos e mínimo igual, passa: [neo/bin/neo-shamir:269](../neovanguard-os-dev/neo/bin/neo-shamir:269).
4. A interpolação devolve bytes que, em geral, não correspondem a nenhuma das sementes originais.
5. `entropia_para_frase()` calcula um checksum novo para esses bytes: [neo/bin/neo-shamir:178](../neovanguard-os-dev/neo/bin/neo-shamir:178).
6. O comando apresenta “seed reconstruída” e sugere conferência com `neo-seed-check`. A integridade sintática da frase não demonstra que ela seja a semente original.

## Evidência observada

Foram divididos dois valores sintéticos de 16 bytes com mínimo 2 e total 3. A mistura da primeira parte de um conjunto com a segunda do outro foi aceita pela interpolação e devolveu um terceiro valor, diferente de ambos.

A conversão desse resultado em palavras, usando uma lista sintética de 2.048 entradas, passou pela própria verificação de checksum do programa. Nenhuma semente real foi usada, exibida ou gravada.

## O erro

Partes individualmente íntegras não comprovam que pertençam ao mesmo conjunto. O programa transforma essa mistura em uma frase válida e anuncia recuperação. A consequência possível é abrir uma carteira ou identidade diferente, mesmo depois de uma conferência de checksum.

O teste não indica defeito na aritmética GF(256); demonstra falta de detecção de mistura no formato e no fluxo de recuperação.

## Pontos de toque

- `codificar/decodificar → cmd_juntar → juntar_bytes → entropia_para_frase`.
- `neo-seed-check` é citado pelo próprio comando, mas a validade do checksum não confirma a origem dos bytes reconstruídos.
- [Cadeia 07](✅-07-airgap-sucesso-sem-isolamento.md): relação de diagnóstico, não dependência de execução — ambos apresentam sucesso sem comprovar a propriedade que o usuário espera.
- [Índice](README.md).
