# Auditoria do Neovanguard OS — 16/09/2026

**Os 12 erros NVG-01 a NVG-12 permanecem corrigidos no escopo original verificável. Foram confirmados 20 novos problemas, documentados individualmente abaixo.** Outras correções anunciadas têm resultados parciais ou dependem de integração; isso está discriminado na conferência, sem presumir que alteração de fonte seja validação de uma ISO.

Base: `619d7697bf9ff0067a0d314c6456a5183f7a733b`, merge do PR #7, versão 1.2.1 em preparação. Auditoria iniciada em 15/09 e concluída em 16/09/2026. A árvore estava limpa no início. Nenhum fonte de produção foi alterado; os arquivos acrescentados são relatórios, provas e registros desta pasta. O wallpaper foi materializado e os perfis foram compostos em diretórios ignorados pelo Git para executar as verificações.

## Os três entregáveis

1. **[Lista e conferência das correções anteriores](correcoes-verificadas.md):** resposta para cada NVG antigo e para as demais correções anunciadas no changelog, notas de versão e documentação Frost/segurança.
2. **Um MD por problema novo:** os 20 documentos na tabela abaixo, com causa, cenário, evidência reproduzível, impacto, limites e direção de correção.
3. **[O que ainda exige build, VM, instalação ou hardware](pendencias-iso-vm-hardware.md):** matriz de cenários e critérios de aprovação, além dos limites que VM não resolve.

## Novos problemas confirmados

| ID / relatório | Problema | Gravidade |
|---|---|---|
| [NVG-13](NVG-13-particao-da-midia-live.md) | Partições da mídia Live são aceitas como destino manual | Alta |
| [NVG-14](NVG-14-raiz-esp-home-sobrepostas.md) | A mesma partição pode ser raiz, ESP e home | Alta |
| [NVG-15](NVG-15-usuario-reservado.md) | O instalador aceita root como nova conta e falha depois da formatação | Alta |
| [NVG-16](NVG-16-boot-vault-perde-parametros.md) | A entrada Cold Vault perde parâmetros necessários para Btrfs e LUKS | Alta |
| [NVG-17](NVG-17-cofre-links-no-destino.md) | Aplicação privilegiada do cofre segue links no home e no temporário | Alta |
| [NVG-18](NVG-18-restauracao-instalador-sem-filtros.md) | Restauração do instalador ignora a lista de arquivos permitidos | Alta |
| [NVG-19](NVG-19-envelope-causa-panic.md) | Tamanho não autenticado do envelope pode abortar o processo | Média |
| [NVG-20](NVG-20-limpeza-dms-nao-publica.md) | Limpeza de DMs anuncia envio sem publicar pedidos de exclusão | Média |
| [NVG-21](NVG-21-elevacao-perde-argumentos.md) | Flash e transportes mesh perdem a ação ao executar sudo | Média |
| [NVG-22](NVG-22-sync-ignora-eventos-offline.md) | Sincronização deixa eventos offline antigos sem publicar | Média |
| [NVG-23](NVG-23-secureboot-sucesso-falso.md) | Setup de Secure Boot anuncia cadeia assinada após falha | Alta |
| [NVG-24](NVG-24-matriz-24-palavras-cortada.md) | Matriz de aço para 24 palavras ultrapassa a página | Média |
| [NVG-25](NVG-25-wizard-captura-menu.md) | Primeiro boot captura o menu junto com a resposta | Alta |
| [NVG-26](NVG-26-perfil-gravado-nao-lido.md) | Perfil é gravado em arquivo e chave diferentes dos que são lidos | Média |
| [NVG-27](NVG-27-vpn-ipv6-sem-ndp.md) | Kill-switch impede endpoint IPv6 quando o cache de vizinhos esvazia | Média |
| [NVG-28](NVG-28-teste-depende-da-gpu.md) | Teste do manifesto falha em hosts NVIDIA e bloqueia o check | Média |
| [NVG-29](NVG-29-rpc-aceita-evento-forjado.md) | Cliente Nostr aceita perfil com hash e assinatura inválidos | Alta |
| [NVG-30](NVG-30-zap-nao-confere-valor.md) | Zap não compara o valor da fatura com os sats solicitados | Alta |
| [NVG-31](NVG-31-assinatura-descarta-tags.md) | CLI de assinatura ignora --tag e envia um evento sem referências | Média |
| [NVG-32](NVG-32-verificador-pacotes-falso-alarme.md) | Verificador anuncia pacote inexistente por conflito do host | Baixa |

A gravidade considera a consequência no cenário indicado, não uma pontuação CVSS nem a probabilidade de ocorrência. Os relatórios não afirmam efeitos que não foram observados: distinguem, por exemplo, aceitar uma seleção destrutiva de efetivamente formatar um disco, despachar uma fatura de liquidar um pagamento e perder parâmetros de boot de executar um boot.

Prioridade de tratamento: aplicação privilegiada do cofre (NVG-17), autenticidade/valor em pagamentos (NVG-29/30), seleção destrutiva e restauração no instalador (NVG-13/14/15/18), boot e isolamento solicitado (NVG-16/23/25). Os demais problemas também possuem cenários confirmados.

## Validação realizada

- **Rust:** 182 testes existentes passaram e 1 falhou, somando 183 execuções distintas da suíte original. A falha depende da GPU do host (NVG-28), reproduzida com controles NVIDIA/Intel. As partes após a interrupção da suíte foram executadas separadamente.
- **Análise Rust:** fmt e Clippy do workspace, com todos os alvos e avisos tratados como erro, passaram.
- **Python/rede:** 103 testes existentes passaram, incluindo 10 de tráfego real em namespaces descartáveis. Quatro referências de políticas nft e suas sondas de estado passaram.
- **Qt:** 14 resultados aprovados (10 testes funcionais de login/mídia e 4 de inicialização/limpeza), offscreen.
- **Agente sob systemd:** teste adicional com a política fornecida pelo projeto passou para IPC, sockets IP, home somente leitura e NIP-46.
- **Sintaxe:** 84 arquivos Bash/PKGBUILD, 37 Python e 10 JSON próprios, sem falhas no conjunto inspecionado.
- **Provas dos achados:** funções reais, CLI real, cópias temporárias de scripts, respostas externas simuladas e tráfego isolado. Seis testes Rust adicionais reproduziram defeitos; “passou” nessas provas significa que o defeito foi observado, não que está corrigido.
- **Perfil de ISO:** a composição e verificações estáticas foram exercitadas, mas não houve aprovação integral nem build da ISO. O [registro de evidências](evidencias/README.md) separa falhas confirmadas, limitações do ambiente e pré-requisitos ausentes.

Logs, comandos e provas estão em **[evidencias/](evidencias/README.md)**. Nenhuma chave pessoal, pagamento real, disco real, conta real, firmware ou firewall do host foi usado para reproduzir falhas.

## Alcance e interpretação

A revisão percorreu os componentes próprios de instalação, disco/contas/boot, cofre/configurações/identidade Nostr, agente e IPC, utilitários neo-*, políticas de rede, assistente inicial, build/empacotamento/workflows e integração visual, com leitura dirigida pelos fluxos e pelas alegações anteriores. Não foi uma auditoria linha a linha de toda dependência vendorizada, Arch/AUR ou kernel, nem uma prova de ausência de outros erros.

As correções antigas foram avaliadas contra o diagnóstico original. Foram mantidos separados: erro novo, limitação já documentada, falha do ambiente de auditoria e comportamento que depende de testes reais. Não foram chamados de defeitos o wallpaper ainda não gerado, restrições de sockets do sandbox ou uma hipótese não confirmada sobre nomes longos de usuário.

Esta auditoria conclui os entregáveis de revisão do código; **não certifica a ISO nem a ausência de outras falhas**. A próxima validação técnica está especificada no documento de pendências.
