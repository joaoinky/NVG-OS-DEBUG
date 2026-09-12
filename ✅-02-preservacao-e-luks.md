# Cadeia 02 — Raiz marcada como mantida recebe luksFormat

> **Status: RESOLVIDO**: corrigido no commit `3e0b344` (primeira rodada, `NVG-03`), presente na `main` do `neovanguard-os-dev`. [Comportamento atual e testes](correcoes-01.md).

Erro: **NVG-03**. Impacto: crítico pelo potencial de perda de dados. Verificação: fluxo confirmado por leitura; nenhuma formatação executada.

## Solução aplicada

A combinação particionamento manual + raiz mantida + LUKS é recusada na tela e no motor. Um plano inválido termina antes de preparar o ambiente, sem nenhum comando de instalação ou limpeza, e o próprio `partition()` confere a combinação de novo.

Validação: os testes do instalador cobrem a recusa de planos inválidos sem executar comandos (67 aprovados em 11/09/2026).

O texto abaixo registra o problema original; as linhas citadas são as do commit auditado.

## Walkthrough

1. No particionamento manual, o usuário desmarca a formatação da raiz. A revisão apresenta a partição como **“mantida”**: [rust/nvg-installer/src/ui.rs:1761](../../../rust/nvg-installer/src/ui.rs:1761).
2. Em outra tela, a criptografia pode continuar habilitada. Os controles de formatação e criptografia são independentes: [rust/nvg-installer/src/main.rs:424](../../../rust/nvg-installer/src/main.rs:424). A validação de Layout verifica apenas as senhas do disco: [rust/nvg-installer/src/app.rs:991](../../../rust/nvg-installer/src/app.rs:991).
3. `partition()` recebe a raiz manual e, quando `encrypt=true`, executa `cryptsetup luksFormat --batch-mode` nela. Essa chamada não depende de `format_root`: [rust/nvg-installer/src/install.rs:731](../../../rust/nvg-installer/src/install.rs:731).
4. Só depois `format_fs()` consulta a opção de preservar a raiz. Nesse momento, o cabeçalho LUKS já foi escrito: [rust/nvg-installer/src/install.rs:769](../../../rust/nvg-installer/src/install.rs:769).
5. A etapa seguinte tenta montar o mapeador recém-criado sem ter criado um sistema de arquivos dentro dele. Para uma partição comum preexistente, isso tende a falhar após a alteração destrutiva.

## O erro

A informação “mantida” não descreve a operação realizada. A combinação manual + preservar raiz + criptografia causa escrita destrutiva antes de a opção de preservação ser considerada. O impacto não é apenas uma mensagem incorreta: os dados anteriores deixam de estar acessíveis da maneira original. A extensão da recuperação não foi testada.

## Pontos de toque

- `main.rs/app.rs → ui.rs → partition → format_fs → mount`: controles independentes produzem uma promessa que a execução contradiz.
- [Cadeia 01](✅-01-conta-interpretada-pelo-shell.md): falhas tardias depois da preparação do disco.
- [Cadeia 03](✅-03-btrfs-e-primeiro-boot.md): outra divergência entre layout preparado e etapa que o consome; são defeitos independentes.
- [Índice](README.md).
