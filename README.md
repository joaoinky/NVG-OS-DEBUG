# NVG-OS-DEBUG

Repositório público de auditorias técnicas do **Neovanguard OS (NVG-OS)**. Aqui ficam os diagnósticos de falhas, as cadeias de causa e efeito, as evidências reproduzíveis e os registros de correções encontrados durante a revisão do projeto.

## Sobre o NVG-OS

O Neovanguard OS é um sistema operacional voltado a privacidade, segurança e soberania digital. O projeto reúne instalação com disco criptografado e Btrfs, modos de rede com Tor, VPN e isolamento, recursos de cofre e recuperação, identidade e comunicação por Nostr e integrações com Bitcoin, Lightning e Liquid.

Esses componentes atravessam limites sensíveis — disco, boot, rede, credenciais e pagamentos — e por isso precisam ser avaliados como fluxos completos. Um comando pode funcionar isoladamente e ainda produzir um estado final inseguro ou incoerente. As auditorias deste repositório procuram tornar essas relações visíveis e verificáveis.

## Objetivo do repositório

Este não é o repositório do código-fonte do sistema. É um histórico técnico complementar, criado para:

- registrar cada problema com contexto, causa, propagação, impacto e limites;
- manter evidências e procedimentos de reprodução sem usar dados pessoais ou recursos reais desnecessariamente;
- acompanhar quais correções foram verificadas e quais continuam pendentes;
- separar análise de código, teste automatizado e simulação de validações que exigem ISO, VM, instalação ou hardware;
- facilitar a revisão pública sem afirmar garantias maiores que as evidências permitem.

## Auditorias disponíveis

| Pasta | Conteúdo | Situação registrada |
|---|---|---|
| [2026-08-09](2026-08-09/README.md) | NVG-01 a NVG-12, registros das rodadas de correção e reconciliação com o repositório de desenvolvimento | 12 erros corrigidos no escopo verificado |
| [2026-09-16](2026-09-16/README.md) | Conferência das correções anteriores e 20 novos problemas, NVG-13 a NVG-32, com provas e matriz de validação | 3 corrigidos e integrados; 17 pendentes |

Atualização de 18/09/2026: NVG-29, NVG-30 e NVG-17 foram corrigidos e integrados
à main do código-fonte. Veja os [commits, PRs e testes da rodada](2026-09-16/correcoes-2026-09-18.md).
Validação conjunta após os merges e em ISO/VM permanece pendente.

Comece pelo README da auditoria desejada. Ele contém a ordem de leitura, o estado de cada achado, um mapa das áreas afetadas e os limites da validação. Na auditoria de 16/09, os comandos e logs ficam reunidos em [evidências](2026-09-16/evidencias/README.md).

## Como interpretar os relatórios

“Confirmado” significa que o comportamento descrito foi reproduzido ou sustentado pelas evidências indicadas. “Corrigido” significa que a correção foi conferida dentro do escopo registrado. Nenhum desses termos, sozinho, certifica uma imagem instalável ou prova a ausência de outras falhas.

As reproduções evitam ações destrutivas e dados reais sempre que possível. Antes de executar qualquer prova, leia suas precondições e guardas: alguns cenários lidam com particionamento, regras de rede, contas, firmware ou pagamentos e são deliberadamente simulados ou isolados.

## Escopo e responsabilidade

Este material registra o estado do código nas revisões e commits indicados em cada pasta. Resultados podem mudar depois desses pontos de referência. O conteúdo deve ser usado como apoio à correção e à validação, não como certificação de segurança do NVG-OS ou de uma ISO específica.
