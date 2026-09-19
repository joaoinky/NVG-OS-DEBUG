# Cadeia 08 - Partes de divisões diferentes produzem “seed reconstruída”

> **Status: RESOLVIDO**: corrigido na quinta rodada (`NVG-09`), em 11/09/2026. [Registro da rodada](correcoes-05.md).

Erro: **NVG-09**. Impacto: alto, recuperação silenciosa de uma identidade diferente. Verificação: funções reais exercitadas em memória com dados sintéticos.

## Solução aplicada

As partes passaram ao formato `nvgs2-K-N-i-ID-hex-crc`. O `ID` são 4 bytes aleatórios, iguais em todas as partes de uma divisão, e o `juntar` recusa na hora de colar uma parte com outro `ID`, outro mínimo, outro total ou outro tamanho. Junto com a seed são divididos 4 bytes de SHA-256 dela (a etiqueta). Depois da interpolação, a etiqueta tem de fechar com os bytes reconstruídos; se não fechar, o comando termina **sem mostrar seed nenhuma**. Como a etiqueta está dentro dos bytes divididos, K-1 partes continuam sem informação sobre a seed.

Partes `nvgs1` já impressas continuam abrindo. Sem etiqueta, o comando pede uma parte a mais e exige que todas as combinações de K devolvam os mesmos bytes; sem essa parte, a seed sai marcada **"NÃO CONFERIDA"**, com a instrução de refazer a divisão. O texto final deixou de sugerir que o `neo-seed-check` confirma a origem: ele confere que a frase é bem formada, não que é a original.

Validação: 21 testes em `scripts/test-neo-shamir.py`, incluindo a reprodução exata desta cadeia (dois segredos de 16 bytes, mínimo 2 de 3, uma parte de cada), `ID` forjado com CRC refeito, duas divisões da mesma seed, parte alterada, 300 misturas seguidas sem nenhuma aceita, e o comando `juntar` de ponta a ponta. O `dividir` foi exercitado por pty com lista e frase sintéticas.

O texto abaixo registra o problema original; as linhas citadas são as do commit auditado.

## Walkthrough

1. Duas sementes distintas são divididas com o mesmo mínimo e a mesma quantidade de partes.
2. O formato de cada parte contém versão, mínimo, total, índice, bytes e checksum local. Não contém uma identificação da divisão: [neo/bin/neo-shamir:196](../../../neo/bin/neo-shamir:196).
3. Durante a recuperação, `cmd_juntar()` compara o mínimo e rejeita índices duplicados. Uma parte de cada divisão, com índices distintos e mínimo igual, passa: [neo/bin/neo-shamir:269](../../../neo/bin/neo-shamir:269).
4. A interpolação devolve bytes que, em geral, não correspondem a nenhuma das sementes originais.
5. `entropia_para_frase()` calcula um checksum novo para esses bytes: [neo/bin/neo-shamir:178](../../../neo/bin/neo-shamir:178).
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
- [Cadeia 07](✅-07-airgap-sucesso-sem-isolamento.md): relação de diagnóstico, não dependência de execução - ambos apresentam sucesso sem comprovar a propriedade que o usuário espera.
- [Índice](README.md).
