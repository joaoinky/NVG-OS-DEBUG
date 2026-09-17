# Sétima rodada de correções

Data: 12/09/2026. Escopo: pendências posteriores às seis rodadas da auditoria.
**Estado:** publicada na branch `fix/pendencias-pos-auditoria`, no
[PR #7](https://github.com/NEOpisa/neovanguard-os-dev/pull/7), ainda sem merge. Criada
da `main` limpa e idêntica a `osdev/main`, `318c283`. As rodadas anteriores
foram publicadas pelos PRs #5 (`034f0d7`) e #6 (`318c283`); o workflow `check`
da base passou na execução `34656044285`.

## Diagnóstico da build automática

A única execução de `build-iso.yml`, [34023993913](https://github.com/NEOpisa/neovanguard-os-dev/actions/runs/34023993913),
foi agendada em 06/09/2026 sobre `97a4975` e falhou após 41m02s. Evidências
obtidas com `gh run list -R NEOpisa/neovanguard-os-dev --workflow build-iso.yml`
e `gh run view 34023993913 -R NEOpisa/neovanguard-os-dev --log-failed`:

1. Às 09:35:25 UTC, `python-flask-restx` falha com
   `Cannot import 'setuptools.build_meta'` e
   `ERROR Backend 'setuptools.build_meta:__legacy__' is not available.`
2. Às 09:36:34 UTC, o Core Lightning tenta instalar dependências. O
   `target not found: python-flask-restx` aborta a transação inteira do pacman;
   por isso as dependências oficiais também aparecem como ausentes. A ausência
   de paru/yay é consequência do fallback, não a causa da falha inicial.
3. A ordem já era flask-restx **antes** de Core Lightning no commit executado.
   Os comentários que atribuíam essa execução à ordem foram corrigidos.
4. O `yes s | ... || yes y | ...` repete a tentativa, com o mesmo erro às
   09:53:09 UTC. Não resolve dependências nem distingue falha de compilação.

O PKGBUILD local de flask-restx já foi publicado no commit `bc19c8e` e declara
`python-setuptools` em `makedepends`. Foi preservado. A rodada 07 garante sua
seleção na posição do `aur.lista`, sem reconstruí-lo outra vez ao enumerar a
pasta de PKGBUILDs locais, e testa a instalação do backend declarado.

## Alterações

- `build-aur.sh`: instala as dependências oficiais consultando `pacman -Si`
  separadamente dos pacotes AUR; mantém restrições de versão. Depois instala
  os arquivos locais já construídos por `pacman -U`, antes do makepkg do
  consumidor. Para PKGBUILDs locais continuam entrando apenas dependências
  de build, sem instalar serviços de execução no host.
- `--noconfirm` aceita explicitamente PKGBUILDs de terceiros e a importação
  da chave Sparrow. O workflow faz uma única chamada e passa `--forcar` quando
  `rebuild_aur=true`, inclusive com arquivos restaurados do cache. O cache
  considera `VERSION`, o script, a lista AUR e os PKGBUILDs.
- O contêiner da ISO passa a habilitar multilib antes de `pacman -Syu`, como
  o workflow `check` já fazia. Sem isso, depois do AUR a chamada de
  `build-iso --check` no fluxo completo rejeitaria `steam`/`lib32-*` da tela
  de programas. Esse bloqueio foi identificado no código; não foi a falha
  registrada na execução de 06/09, que parou antes.
- **Nenhum pacote opcional.** Todos os selecionados são obrigatórios. Falhas
  de ajuste, compilação ou cópia de artefato terminam com erro. O resumo em
  `vendor/aur/resumo-build.md` informa selecionados, construídos, falhas e
  código de saída; o job o acrescenta a `GITHUB_STEP_SUMMARY` mesmo com falha.
  Não há repetição de build por falta de dependências quando a lista está vazia.
- Removidos o destino antigo de releases, input `publicar`, uso do token
  entre repositórios e comentários obsoletos de imagens e divisão de arquivos.
  **`NEOpisa/neovos` e derivados, inclusive `neovosdev`, estão aposentados.**
  Nada foi recriado, publicado ou configurado neles. O remoto ativo permanece
  `osdev`, repositório privado `NEOpisa/neovanguard-os-dev`.
- **Destino escolhido pelo usuário:** somente checksums SHA-256/BLAKE2 como
  artefato por 14 dias. O CI constrói e valida as ISOs, mas não as guarda ou
  distribui. As duas somas são verificadas contra as imagens antes do upload.
  Também não há artefato separado de log; os logs são os da execução.
  O [GitHub Free inclui 500 MB de armazenamento de artefatos](https://docs.github.com/en/billing/concepts/product-billing/github-actions),
  insuficientes para cerca de 9 GB de ISOs. A cota é compartilhada: checksums
  também podem falhar se o armazenamento da conta já estiver esgotado.
- Actions atualizadas nos dois workflows após conferir releases e
  `runs.using: node24` nos manifests: [checkout v7.0.1](https://github.com/actions/checkout/blob/v7.0.1/action.yml),
  [cache v6.1.0](https://github.com/actions/cache/blob/v6.1.0/action.yml) e
  [upload-artifact v7.0.1](https://github.com/actions/upload-artifact/blob/v7.0.1/action.yml).
  Os workflows referenciam os majors v7, v6 e v7, respectivamente.
- **Versão 1.2.1 autorizada explicitamente pelo usuário.** Atualizados
  `VERSION`, `os-release`, metadados dos dois perfis, README, CHANGELOG e notas
  de versão. Os três pacotes próprios leem `VERSION` e passam a `1.2.1-1`.
  Os números internos dos crates não são a versão da distro.
- `wireguard-tools` é optdepend de soberania e entra em seu perfil padrão:
  quem tem o kill-switch na ISO passa a ter o `wg` para descoberta. O pacote
  não configura nem ativa VPNs. A biblioteca distingue executável ausente
  (instrução de instalação ou `--endpoint`) e peer com `(none)` (identifica o
  peer e pede endpoint). Ambas as falhas impedem carregar regras.
- `neo-mac`: cinco bytes de `/dev/urandom` depois do octeto `02`, com recusa
  de falha ou leitura curta. Troca e restauração acumulam falhas por interface,
  relatam sucessos e retornam erro em inventário vazio, interface inexistente,
  falha ao abaixar/trocar/reativar ou ausência de endereço permanente válido.
  Falha da troca ainda tenta restaurar a interface que estava ativa.
- Reconciliação atualizada para publicação pelos PRs #5/#6; retirada a
  orientação desatualizada de push direto na main. Menção histórica ao remoto
  `neovosdev` marcada como aposentada. Índice e pendências atualizados.

## Evidências

- Reprodução em `archlinux:base-devel`, digest
  `sha256:61f7de2dd88cc4ba1fe36c24cfe1a503c3936984492d6405eeab013ce6ac68c5`,
  usando `docker run --rm --user 1000:1000 --cap-drop ALL --security-opt
  no-new-privileges`. Sem bind de diretórios do host, sem modo privilegiado.
  Bancos `core.db`/`extra.db` baixados para `/tmp/db/sync`; `pacman --dbpath
  /tmp/db -Si` confirmou `libsodium`, `lowdown`, `net-tools`, `postgresql-libs`
  e `python-setuptools`. Não houve instalação pelo pacman.
- Outra sonda no contêiner confirmou `steam` e `lib32-nvidia-utils` ausentes
  com a configuração padrão e presentes depois de habilitar multilib numa
  cópia de `pacman.conf` em `/tmp`. Foram apenas consultas `pacman -Si`.
- No mesmo tipo de contêiner, um venv em `/tmp` com `build`, `installer` e
  `wheel`, mas sem setuptools, reproduziu exatamente o erro do backend.
  Fonte flask-restx 1.3.2 de `files.pythonhosted.org`, SHA-256 conferido contra
  o PKGBUILD (`0ae13d77e7d7e4dce513970cfa9db45364aef210e99022de26d2b73eb4dbced5`).
  Adicionar somente setuptools 84.0.0 permitiu `python -m build --wheel
  --no-isolation`, gerando `flask_restx-1.3.2-py2.py3-none-any.whl`.
  Isso valida a causa e o backend, não toda a build de Core Lightning/ISO.
- `scripts/test-build-deps.py`: **7 testes aprovados**. Cobrem seleção de
  oficiais sem AUR, preservação das restrições de versão, backend do PKGBUILD
  real, ordem sem duplicação, isolamento de dependências de execução, modo
  não interativo/cache/forçar, falha de compilação e ausência de artefato.
- `scripts/test-network-modes.py`: **18 testes aprovados**. `wg` falso no PATH;
  PATH fechado no teste sem executável; peer sem endpoint identificado, peer
  válido, IPv4/IPv6 e recusa antes de alterar o firewall simulado.
- `scripts/test-neo-mac.py`: **8 testes aprovados**, incluídos no `./check`.
  `ip`, `ethtool` e sysfs simulados; leitura determinística e leitura real de
  `/dev/urandom`; falhas parciais, totais, restauração, endereço inválido e
  inventário vazio. Nenhuma interface real foi alterada.
- `check-neo-cli.py` e `check-neo-refs.py`: aprovados, 55 comandos.
- `test-nft-network.py`: **10 testes aprovados** em namespaces descartáveis.
- `check-network-policies.py`: aprovado, quatro referências e sondas do kernel.
- YAML dos dois workflows e sintaxe Bash de seus passos: aprovados.
- Passo de checksums executado com arquivos temporários: aceita conteúdo
  íntegro e recusa conteúdo alterado antes do upload.
- `grep` nos arquivos versionados fora da auditoria, incluindo inspeção dos
  destinos de symlinks: nenhuma ocorrência de `neovos`. Diretórios gerados,
  ISOs antigas e histórico `.git` não foram reescritos.
- Os três pacotes foram reconstruídos como **1.2.1-1**; `.PKGINFO` conferido.
  A primeira chamada gerou base, instalador e soberania, mas terminou com
  código 2 antes do índice porque um comentário do script foi editado durante
  sua execução. A sintaxe final passou em `bash -n`; nova execução de
  `./neo/packaging/build-aur.sh --forcar neovanguard-sovereignty` terminou com
  zero e atualizou o índice. Base/instalador foram reconhecidos na chamada
  seguinte, com zero. O empacotamento base rodou **183 testes release**.
- Os arquivos `neo-mac`, `neo-mac-reset` e `neo-vpn.py` do pacote soberania
  foram comparados byte a byte com a árvore; optdepend WireGuard conferido.
- **`./check` aprovado**, código zero: fmt, Clippy sem avisos, **183 testes
  Rust**, 7 testes de empacotamento, 17 de estado de rede, 18 de modos, 8 de
  MAC, 21 de Shamir e `build-iso --check`. O verificador aprovou o índice dos
  pacotes e o item **“the version agrees everywhere”** com a versão 1.2.1.
- Rodada final de `python3 scripts/test-nft-network.py` e
  `python3 scripts/check-network-policies.py`: ambas aprovadas, códigos zero.
- `git diff --check`: aprovado, sem erros de whitespace.

## Arquivos desta rodada

- `.github/workflows/build-iso.yml`, `.github/workflows/check.yml`, `check`.
- `VERSION`, `CHANGELOG.md`, `README.md`, `documentation/notas-de-versao/1.2.1.md`.
- `neo/packaging/build-aur.sh`, `aur.lista`, `publish-repo.sh` e
  `pkgbuilds/neovanguard-sovereignty/PKGBUILD`.
- `neo/lib/neo-vpn.py`, `neo/bin/neo-mac`, `neo/bin/neo-mac-reset`.
- `profile-src/packages/soberania.txt`, `profile-src/airootfs/base/etc/os-release`
  e `profile-src/perfis/{mbn-live,mbn-install}/profiledef.sh`.
- `scripts/test-build-deps.py`, `scripts/check-ordem-aur.py`,
  `scripts/test-network-modes.py`, `scripts/test-neo-mac.py` (novo).
- `documentation/COMO-CONSTRUIR.md`, `documentation/verificacao-estado-rede.md`.
- Nesta pasta: `README.md`, `reconciliacao-2026-09-11.md` e este arquivo novo.
- Artefatos ignorados: pacotes e índice em `vendor/repo`, cópias em `vendor/aur`,
  binários Cargo e perfis gerados pelo verificador. As ISOs antigas são preservadas.

## Limites e o que depende do usuário

- O usuário autorizou push, PR e limpeza remota, mas excluiu expressamente
  a construção da ISO. **Nenhum disparo de `build-iso.yml` foi feito.**
  A build completa segue sem validação nesta rodada; AUR e Arch continuam variáveis.
- A primeira tentativa de push foi recusada pelo GitHub: a credencial OAuth
  HTTPS não tinha escopo `workflow` para modificar `.github/workflows/build-iso.yml`.
  `gh auth status` confirmou a ausência desse escopo. A alternativa SSH existente
  também falhou com `Permission denied (publickey)`. Após o usuário renovar
  a autorização, `gh auth status` passou a mostrar `workflow`; a nova tentativa
  publicou a branch e abriu o **PR #7**. O CI executa somente `check`, acionado
  pelo PR; [resultados por commit na aba Checks](https://github.com/NEOpisa/neovanguard-os-dev/pull/7/checks).
  Nenhum workflow de ISO foi disparado e nenhum segredo foi configurado.
- **Limpeza remota concluída em 12/09/2026**, após autorização: excluídas
  `fix/regras-nft-excecoes`, `feat/verificacao-estado-rede` e
  `fix/04-07-marcadores`. O push de exclusão foi atômico, com leases dos SHAs
  conferidos antes da operação. `git fetch --prune osdev` terminou com sucesso
  e também removeu referências locais a `docs/auditoria-publicada` e
  `fix/auditoria-05-06`, que já não existiam no remoto. A consulta posterior
  confirmou a ausência das três branches solicitadas.
  Duas pontas eram ancestrais da main. A ponta `7e3c78a` de
  `fix/regras-nft-excecoes` é somente o merge do PR #2: seus dois pais estão
  integrados, e `git show --cc` não mostra resolução exclusiva. Isso explica
  por que `git branch --merged` não a listava literalmente.
- A versão nova permite atualização, mas ainda falta distribuir os pacotes
  pelo repositório de atualizações configurado no alvo. Fonte no GitHub e
  checksum no Actions não fazem uma instalação receber pacotes por `pacman -Syu`.
- Sem root, montagem de ISO local, firewall/interface/disco real, boot de VM,
  teste físico ou VPN real. O teste no contêiner não construiu Core Lightning.
- O PR #1 do NVG-OS-DEBUG não foi alterado. Revisão criptográfica independente
  do `nvgs2` e senha de conta vazia com root igual permanecem fora do escopo.
