# Segunda rodada de correções

Data: 09/09/2026. Escopo: NVG-04, o primeiro boot de instalações Btrfs pelo systemd-boot.

## Alteração

Em instalações Btrfs novas ou com a raiz reformatada, a entrada do systemd-boot agora inclui `rootflags=subvol=@`. Assim, o kernel monta a mesma raiz `@` usada durante a instalação. Partições Btrfs mantidas não recebem essa opção, pois o instalador não cria nem pode presumir a estrutura de subvolumes existente.

## Evidência

- Formatação Rust aprovada.
- Teste focado aprovado: Btrfs em instalação nova e em raiz reformatada seleciona `@`; Btrfs mantido não recebe uma opção presumida.

Não foi gerada ISO nem realizado boot em VM nesta rodada.

## Pendências

NVG-05 a NVG-09 e a divergência do índice do repositório de pacotes locais continuam pendentes.
