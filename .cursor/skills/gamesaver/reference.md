# GameSaver — Referência Detalhada

> Documentação viva para desenvolvedores. Mantida em sincronia com o código e o [README.md](../../README.md).

## Fluxo collect (backup)

1. Usuário define `user_location` (home) e `destination_location` (padrão `SAVES/`).
2. `BackupService.get_installed_games()` verifica existência de `user_location + game.path`.
3. Para cada jogo selecionado:
   - Valida path com `is_safe_game_path()`.
   - Monta destino: `destination_location / basename(game_location)`.
   - Valida com `validate_copy_paths()`.
   - Copia com `shutil.copytree(..., dirs_exist_ok=True)`.
4. Retorna `BackupReport` com sucessos e falhas.

## Fluxo spread (restore)

Espelho do collect:

1. Origem = pasta já coletada em `destination_location`.
2. Destino = `user_location + game.path`.
3. Valida com `validate_spread_paths()` (origem ⊆ backup, destino ⊆ home).
4. Confirma operação antes de sobrescrever saves existentes (GUI e CLI).

## GUI — componentes

| Widget | Arquivo | Função |
|--------|---------|--------|
| `GameSaverWindow` | `gamesaver/gui/main_window.py` | Janela principal, layout |
| `SettingsWidget` | `gamesaver/gui/settings_widget.py` | Campos user/destination, browse, persistência |
| `GameListWidget` | `gamesaver/gui/game_list_widget.py` | Tabela, busca, collect/spread |
| `OperationWorker` | `gamesaver/gui/workers.py` | QThread para operações longas |

Sinais:
- `SettingsWidget.locations_changed` → recarrega lista de jogos instalados.

Estilo: `gamesaver/gui/styles.qss` — fundo `#1E1E1E`, accent `#007AFF`, fonte Segoe UI/Arial, janela mínima 800×600.

## CLI — fluxo

1. `configure_logging()` + `create_default_files()` (`games.json`, `settings.json`, `SAVES/`).
2. `Settings().load()` carrega/valida `settings.json`.
3. `GameManager` (facade) executa `collect()` ou `spread()` conforme `mode`.
4. Relatório colorido no terminal + logs estruturados.

Entrada: `python -m gamesaver --cli` (opcional `-v` para debug).

## Testes

```
tests/
  test_file_handler.py    # path policy reexportada, JSON I/O
  test_backup_service.py  # collect/spread, repositories, metadata
  test_adapters.py        # argparse, GameManager, Settings save
  test_bootstrap.py       # create_default_files
  test_utils.py           # colored helpers
```

Padrões:
- `@pytest.mark.parametrize` para validação de path.
- `tmp_path` para I/O temporário.
- Cobertura mínima 60% no pacote `gamesaver` (GUI omitida).

## CI/CD

### ci.yml
- Trigger: push/PR em `main`/`master`.
- Python 3.11, 3.12, 3.13.
- Steps: `ruff check .` → `mypy` → `pytest -v --cov=gamesaver`.

### release.yml
- Trigger: tags `v*`.
- Build multi-OS com `GameSaver.spec` (PyInstaller).
- Publica artefatos no GitHub Releases.

## Adicionar jogo — exemplos de paths válidos

```
AppData/Roaming/GameName
Documents/My Games/GameName/saves
AppData/Local/GameName/Saved
Saved Games/GameName
```

## Adicionar jogo — paths inválidos

```
AppData                    # muito amplo
Documents                  # muito amplo
AppData/Roaming            # muito amplo
Saved Games                # muito amplo (sem subpasta)
```

## Checklist de PR

1. Escopo mínimo — não refatorar código não relacionado.
2. Novos paths passam por `path_policy` (segurança).
3. Testes para lógica nova no domínio/infra.
4. `ruff check .`, `mypy` e `pytest -v --cov=gamesaver` passam localmente.
5. Se alterar assets empacotados, verificar `GameSaver.spec` / release workflow.
6. Atualizar README/skill/reference se comportamento ou arquitetura mudar.
7. Código e comentários em inglês.
