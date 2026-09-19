# Primeira rodada de correções

Data: 09/09/2026. Escopo: os três erros do instalador nas cadeias 01 e 02 e a retirada do tamanho mínimo de senha solicitada pelo usuário.

## Alterações, em ordem de prioridade

1. **NVG-03 - preservação da raiz:** a combinação particionamento manual + raiz mantida + criação de LUKS é recusada na tela e no motor. Um plano inválido termina antes da preparação do ambiente, sem comandos de instalação ou limpeza. A função de particionamento também verifica essa combinação.
2. **NVG-02 - interpretação de comandos:** o nome completo chega como um argumento literal ao useradd, preservando apóstrofos e aspas. Hostnames aceitam somente os caracteres próprios dos rótulos definidos pela validação. Dados incompatíveis com os registros de conta são recusados antes da execução. Campos vindos de perfis passam pela mesma verificação no motor.
3. **NVG-01 - senha com apóstrofo:** as senhas são enviadas pela entrada padrão de chpasswd. Não são interpoladas em Bash nem gravadas em nvg-secret.sh. A saída do processo fica oculta e os erros não incluem a senha.

As senhas de conta e disco não têm mais tamanho mínimo imposto pelo instalador. A cifra NIP-49 também aceita senhas sem mínimo; a repetição para confirmação permanece. Quebras de linha e NUL continuam incompatíveis com o protocolo de registros enviado ao chpasswd. Os testes de interface incluem entradas vazias; isso não constitui validação de aceitação de senha vazia por LUKS ou PAM no sistema instalado.

## Evidências

- 66 testes do instalador aprovados, incluindo recusa de planos inválidos sem executar comandos, nome literal no Bash, senhas com caracteres especiais e ausência de mínimo.
- 8 testes de chaves Nostr aprovados, incluindo cifra e decifra com senha de um caractere e senha vazia.
- Clippy dos dois pacotes, com todos os alvos e avisos tratados como erros, aprovado.
- Formatação Rust e conferência de whitespace aprovadas.
- A validação de perfis detectou divergência entre índice e tamanho dos pacotes locais neovanguard-base e neovanguard-base-debug. O resultado completo não foi aprovado.

Não foi gerada uma ISO nem realizada instalação em VM nesta rodada. Os testes não executaram formatação de discos ou criação de contas reais. As mudanças estão no código-fonte; os pacotes binários locais ainda não incorporam essas correções.

## Pendências

NVG-04 a NVG-09 permanecem sem correção nesta rodada, conforme o limite de escopo solicitado. O problema do índice do repositório encontrado na validação também permanece pendente.
