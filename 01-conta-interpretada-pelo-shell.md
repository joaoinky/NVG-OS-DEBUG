# Cadeia 01 — Dados da conta viram instruções de shell

**Estado: corrigido no código-fonte na primeira rodada.** O texto abaixo registra o problema original. [Comportamento atual e testes](correcoes-01.md).

Erros: **NVG-01 e NVG-02**. Impacto: alto. Verificação: leitura do fluxo e reprodução isolada da interpretação pelo Bash.

## Walkthrough

1. Na tela de conta, o usuário informa nome completo, hostname e senha. A validação exige hostname não vazio e senha com tamanho mínimo e confirmação; não restringe os caracteres relevantes para o shell. O nome completo não recebe essa validação. Entrada: [rust/nvg-installer/src/app.rs:1002](../neovanguard-os-dev/rust/nvg-installer/src/app.rs:1002).
2. O plano copia os campos e `accounts()` monta um script. O nome completo entra entre aspas duplas, removendo apenas o próprio caractere de aspas duplas. A senha entra entre aspas simples. Transformação: [rust/nvg-installer/src/install.rs:1057](../neovanguard-os-dev/rust/nvg-installer/src/install.rs:1057).
3. `chroot()` e `chroot_quiet()` gravam esses textos e executam Bash no destino. O conteúdo passa a ter significado de código, com os privilégios da instalação: [rust/nvg-installer/src/install.rs:253](../neovanguard-os-dev/rust/nvg-installer/src/install.rs:253).

## NVG-01 — Senha válida na interface quebra a criação da conta

Uma senha fictícia como `minha'senha` passa pelos critérios da tela, mas encerra prematuramente as aspas em `echo 'usuario:senha' | chpasswd`. A instalação chega à etapa de contas e falha ao interpretar o script, depois de já ter preparado e preenchido o disco.

Evidência: a linha gerada com essa senha foi submetida somente a `bash -n`; retornou código **2**, erro de sintaxe. Não foi executado `chpasswd`. Senhas com combinações específicas de aspas também podem modificar o significado das instruções.

## NVG-02 — Nome completo e hostname permitem interpretação de comandos

No nome completo, uma substituição como `$(printf NVG_MARCADOR)` é executada dentro das aspas duplas. A remoção de `"` não neutraliza essa sintaxe. No hostname, a interpolação em comandos entre aspas simples também permite encerrar o literal. O hostname chega ao script de configuração em [rust/nvg-installer/src/install.rs:983](../neovanguard-os-dev/rust/nvg-installer/src/install.rs:983).

Reprodução inofensiva da construção usada no nome: `Pessoa $(printf NVG_MARCADOR)` resultou em **Pessoa NVG_MARCADOR**, demonstrando que o texto foi interpretado. Não foi executado nenhum comando privilegiado. O alcance demonstrado é uma entrada local no instalador; não foi demonstrada exploração remota.

## Pontos de toque

- `app.rs → Plan → configure/accounts → chroot`: entrada aceita, interpolação e execução.
- [rust/nvg-installer/src/perfil.rs:104](../neovanguard-os-dev/rust/nvg-installer/src/perfil.rs:104) também preenche hostname e nome completo a partir de um perfil; esse é outro caminho de entrada, sujeito aos controles de confiança do perfil.
- [Cadeia 02](02-preservacao-e-luks.md): ambos os problemas podem surgir depois de operações no disco, quando a falha já não equivale a simplesmente cancelar o formulário.
- [Índice](README.md).
