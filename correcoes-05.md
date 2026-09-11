# Quinta rodada de correções

Data: 11/09/2026. Escopo: o NVG-09 (cadeia 08) e a guarda do `scripts/check-network-policies.py`, as duas pendências de código que sobraram da [reconciliação](reconciliacao-2026-09-11.md).

**Estado no momento da validação:** árvore local, antes da publicação. O estado final fica registrado no PR da quinta e sexta rodadas.

## Alterações

1. **NVG-09, partes de divisões diferentes** (`neo/bin/neo-shamir`):
   - Formato novo `nvgs2-K-N-i-ID-hex-crc`. O `ID` são 4 bytes de `os.urandom`, iguais em todas as partes de uma divisão. É aleatório de propósito: não sai da seed e não conta nada sobre ela.
   - A etiqueta são os 4 primeiros bytes de `sha256("neo-shamir/nvgs2\0" + seed)`, anexados à seed **antes** de dividir. Por estar dentro dos bytes divididos, a propriedade "K-1 partes não revelam nada" continua valendo para ela.
   - `juntar` recusa ao colar uma parte de outra divisão (`ID`, mínimo, total, tamanho ou formato diferentes). Depois de juntar, recusa se a etiqueta não fecha, sem mostrar seed.
   - `nvgs1` continua aceito. Como não há etiqueta, o comando pede uma parte a mais (opcional) e exige que toda combinação de K dê os mesmos bytes; sem ela, a seed sai marcada "NÃO CONFERIDA".
   - `decodificar` passou a recusar mínimo, total ou número de parte fora do intervalo.
   - A lógica saiu dos comandos para `dividir_seed()` e `juntar_codigos()`, que dá para testar sem terminal. A conferência de antes de mostrar as partes (reconstruir 20 combinações e checar que K-1 não reconstroem) foi mantida.
   - `--palavras` mostra as palavras dos bytes do tamanho da seed e avisa que o `juntar` lê o código, não as palavras. As palavras nunca bastaram: faltavam índice, mínimo e total.
   - Mensagens que a tradução automática da API tinha estragado (`die de cópia`, `die interno`, `need de`) voltaram a `erro de cópia`, `erro interno` e `precisa de`.
2. **Guarda do `check-network-policies.py`:** a causa não era "precisa de root". O script se relança dentro de `unshare -rn`, e ali dentro **nenhum** processo, nem root, pode ler `/proc/1/ns/net`: o namespace de usuário novo não tem direito de ptrace sobre o PID 1. A guarda recusava toda execução, local e no CI. A nova `disposable_namespace()` exige um namespace diferente do de quem chamou e com `lo` como única interface, que é o que todo namespace recém-criado tem e o do host nunca tem. A comparação com o PID 1 continua quando dá para ler.
3. **`./check`** ganhou `neo-shamir refuses mixed splits` na etapa de empacotamento. Com isso o teste roda no CI, que chama `./check quick`.
4. **`documentation/soberania.md`** descreve o formato `nvgs2` e o comportamento com `nvgs1`.

## Evidências

Rodadas como usuário comum:

- `scripts/test-neo-shamir.py`: 21 testes aprovados. Cobrem a reprodução exata da cadeia 08, `ID` forjado com CRC refeito, duas divisões da mesma seed, parte alterada com CRC refeito, 300 misturas seguidas sem nenhuma aceita, `nvgs1` com e sem parte a mais, formatos misturados e o `juntar` de ponta a ponta por subprocesso.
- `neo-shamir dividir --palavras` dirigido por pty, com lista de 2048 palavras e frase sintéticas: três partes `nvgs2`, conferência "3 combinações de 2 reconstroem; 1 não", e o `juntar` devolveu a frase original.
- `scripts/check-network-policies.py`, sem root: aprovado ("All four network policy references match the loaded nft rules"). Chamado com `--isolated` fora de um namespace descartável, recusa. O `--emit` é idêntico a `neo/lib/network-policies.json`.
- `scripts/check-neo-cli.py` e `scripts/check-neo-refs.py`: 55 comandos conferidos.

Nenhuma seed real foi usada, mostrada ou gravada.

## CI

A `main` do `neovanguard-os-dev` está vermelha desde o PR #1, sempre no passo "Network state references and kernel probes", mas por duas causas:

- **Run `34644214982` (`4ebd017`, só o PR #1):** `can't open file 'scripts/check-network-policies.py'`. O workflow do PR #1 já chamava um script que só chegou no PR #2, mais um efeito da cadeia de PRs mesclada fora de ordem.
- **Run `34645171212` (`2e8320c`, depois do PR #4):** `PermissionError` em `/proc/1/ns/net`, **rodando como root** no container. Isso confirma que a causa era o `unshare -rn`, não a falta de privilégio.

Com esta rodada esse passo deve passar, mas só dá para confirmar depois do push. Os passos seguintes ("Generate the theme resources" e "The ISO profile") não rodam desde o PR #1.

## Limites

- O formato `nvgs2` não passou por revisão criptográfica independente, e a observação de `documentation/soberania.md` continua valendo.
- Uma divisão `nvgs1` misturada, com exatamente K partes, ainda devolve uma frase: não existe informação nas partes que permita recusar. O que mudou é que ela sai marcada como não conferida.
- O pacote `neovanguard-sovereignty` de `vendor/repo` foi reconstruído depois desta rodada, mas continua `1.2.0-1` (ver a pendência de versão na [reconciliação](reconciliacao-2026-09-11.md)).
