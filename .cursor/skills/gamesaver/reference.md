# GameSaver — Referência Detalhada

## Fluxo collect (backup)

1. Usuário define `user_location` (home) e `destination_location` (padrão `SAVES/`).
2. `GameManager.get_installed_games()` verifica existência de `user_location + game.path`.
3. Para cada jogo selecionado:
   - Valida path com `is_safe_game_path()`.
   - Monta destino: `destination_location / basename(game_location)`.
   - Valida com `validate_copy_paths()`.
   - Copia com `shutil.copytree(..., dirs_exist_ok=True)`.

## Fluxo spread (restore) — a implementar

Espelho do collect:

1. Ler jogos de `destination_location`.
2. Para cada jogo, copiar de destino para `user_location + game.path`.
3. Validar que destino de restore permanece dentro do home do usuário.
4. Confirmar operação antes de sobrescrever saves existentes.

## GUI — componentes

| Widget | Arquivo | Função |
|--------|---------|--------|
| `GameSaverWindow` | `gui/main_window.py` | Janela principal, layout |
| `SettingsWidget` | `gui/settings_widget.py` | Campos user/destination, browse |
| `GameListWidget` | `gui/game_list_widget.py` | Tabela de jogos, busca, collect |

Sinais:
- `SettingsWidget.locations_changed` → recarrega lista de jogos instalados.

Estilo: `gui/styles.qss` — fundo `#1E1E1E`, accent `#007AFF`, fonte Segoe UI/Arial, janela mínima 800×600.

## CLI — fluxo

1. `create_default_files()` cria JSONs padrão se inexistentes.
2. `Settings().load()` carrega/valida `settings.json`.
3. `GameManager` executa `collect()` ou `spread()` conforme `mode`.

**Bug**: `GameManager(settings.user_location, settings.destination_location)` — construtor não aceita argumentos. Corrigir passando via atributos ou ajustando `__init__`.

## Testes

```
tests/
  test_file_handler.py  # is_safe_game_path, validate_copy_paths, JSON I/O
  test_utils.py         # colored, printc
```

Padrões:
- `@pytest.mark.parametrize` para casos de validação de path.
- `tmp_path` para I/O temporário.
- Sem testes de GUI ou GameManager (gap a preencher).

Config em `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

## CI/CD

### ci.yml
- Trigger: push/PR em `main`/`master`.
- Python 3.11, 3.12, 3.13.
- Steps: `ruff check .` → `pytest -v`.

### release.yml
- Trigger: tags `v*`.
- Build multi-OS com PyInstaller.
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
2. Novos paths passam por validação de segurança.
3. Testes para lógica nova em `file_handler` ou `game_manager`.
4. `ruff check .` e `pytest -v` passam localmente.
5. Se alterar assets empacotados, verificar workflow de release.
6. Código e comentários em inglês.
