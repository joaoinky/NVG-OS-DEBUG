# Cadeia 10 — Senha de disco vazia passa e a instalação morre depois de apagar o disco

> **Status: RESOLVIDO** na sexta rodada de 11/09/2026. Diagnóstico original preservado abaixo.

## Solução aplicada

`validate_disk_password` recusa senha vazia, LF, CR e NUL quando a criptografia
está ligada. Layout, `validate_before_install` e a entrada de `partition`
chamam a mesma guarda antes de qualquer comando de disco. Um caractere
continua válido; a senha de conta vazia continua permitida.

Os 68 testes do instalador passaram. O teste novo envia cada senha inválida
ao `spawn` e exige somente `Progress::Done(Err(_))`, sem comandos ou progresso.
Também testa a tela Layout e o plano com senha `x`. Não houve instalação,
formatação ou acesso a disco real. Evidências: [sexta rodada](correcoes-06.md).

Erro: **NVG-12**. Impacto: alto, falha tardia depois de uma operação destrutiva. Verificação: leitura do fluxo e comportamento do `cryptsetup` medido numa imagem de arquivo descartável; nenhum disco real foi formatado.

As linhas citadas são as da árvore de 11/09/2026 (`main` local `445eb7b`).

## Walkthrough

1. A [primeira rodada](correcoes-01.md) tirou o tamanho mínimo das senhas, inclusive a do disco. O próprio registro dela diz que aceitar senha vazia no LUKS **não** foi validado.
2. Na tela Layout, com criptografia ligada, a validação confere o armazenamento e se as duas senhas do disco são iguais. Vazia com vazia passa: [rust/nvg-installer/src/app.rs:991](../../../rust/nvg-installer/src/app.rs:991).
3. O motor repete só a conferência de armazenamento e a de conta, sem olhar a senha do disco: `validate_before_install`, em [install.rs:149](../../../rust/nvg-installer/src/install.rs:149), que chama `validate_storage` ([install.rs:80](../../../rust/nvg-installer/src/install.rs:80)).
4. No modo "apagar o disco", `partition()` roda `wipefs -af` e `sgdisk --zap-all` e cria as partições novas: [install.rs:789](../../../rust/nvg-installer/src/install.rs:789).
5. Só depois vem o `cryptsetup luksFormat --key-file -`, com a senha pela entrada padrão: [install.rs:834](../../../rust/nvg-installer/src/install.rs:834). Com a entrada vazia, ele recusa, e a instalação termina com o disco já apagado e nada instalado.

## Evidência observada

Numa imagem de 32 MB em arquivo, sem root:

| Entrada em `cryptsetup luksFormat --type luks2 --batch-mode --key-file -` | Resultado |
|---|---|
| vazia (`printf ''`) | `Nothing to read on input.`, **código 1** |
| um byte (`printf 'x'`) | código 0 |

A passagem da senha em si está certa: `run_in` escreve os bytes como vieram, sem `\n` no fim ([install.rs:274](../../../rust/nvg-installer/src/install.rs:274)), então a senha digitada no boot é a mesma do contêiner.

## O erro

É o padrão da [cadeia 01](✅-01-conta-interpretada-pelo-shell.md) (NVG-01): um valor que a tela aceita e que só falha na execução, depois de o disco ter sido apagado. Aqui a causa não é o shell, e sim a retirada do mínimo sem conferir o que o `cryptsetup` aceita. Senha de um caractere continua sendo possível; o que o LUKS não aceita é senha nenhuma.

## Pontos de toque

- `app.rs (Layout) → Plan → validate_before_install → partition (wipefs/sgdisk) → cryptsetup luksFormat`.
- [Cadeia 02](✅-02-preservacao-e-luks.md): a mesma chamada de `luksFormat`, por outra causa (raiz mantida); a correção dela criou `validate_storage`, que é o lugar natural desta conferência.
- Senha de **conta** vazia é outra coisa: o `chpasswd` aceita, e foi uma escolha do usuário na primeira rodada. Com "root com a mesma senha", o root também fica sem senha, e o PAM do Arch (`nullok`) aceita login assim. Fica registrado como decisão, não como erro.
- [Índice](README.md).
