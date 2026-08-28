---
name: gamesaver
description: Especificações completas do GameSaver — app desktop Python/PyQt6 para backup/restore de saves de jogos. Use ao implementar features, corrigir bugs, adicionar jogos, modificar GUI/CLI, escrever testes ou fazer build com PyInstaller.
---

# GameSaver — Especificações do Projeto

## Documentação viva

| Documento | Público | Escopo |
|-----------|---------|--------|
| `README.md` | Usuários e contribuidores | Instalação, uso, configuração |
| Este arquivo (`SKILL.md`) | Desenvolvedores e agentes | Arquitetura, convenções, workflows |
| `reference.md` | Desenvolvedores | Fluxos detalhados, CI/CD, checklist de PR |

**Regra:** ao alterar comportamento do código, atualizar README (se impacta usuário) e esta skill (se impacta arquitetura/convenções) no mesmo PR.

## Visão geral

GameSaver detecta jogos instalados, copia pastas de save para uma pasta central de backup (`collect`) e (futuro) restaura saves para os diretórios originais (`spread`).

| Modo | Status | Descrição |
|------|--------|-----------|
| `collect` | ✅ Implementado | Backup de saves para pasta de destino |
| `spread` | ✅ Implementado | Restore de saves para diretórios originais |
| GUI (PyQt6) | ✅ Padrão | `python -m gamesaver` ou `python main.py` |
| CLI (colorama) | ✅ Alternativo | `python -m gamesaver --cli` |

## Estrutura do projeto

```
main.py                      # Entry point fino (delega para gamesaver)
gamesaver/
  __main__.py                # argparse (--cli), bootstrap GUI/CLI
  constants.py               # Paths, defaults, PyInstaller
  models.py                  # GameEntry, AppSettings, BackupReport
  path_policy.py             # Validação e resolução de paths
  backup_service.py          # Lógica collect/spread (sem I/O de UI)
  repositories.py            # GameRepository, SettingsRepository
  file_handler.py            # JSON I/O, bootstrap de arquivos
  file_utils.py              # Tamanho, timestamps, formatação
  game_manager.py            # Facade CLI (print/input)
  settings.py                # Facade de settings com prompts CLI
  utils.py                   # Helpers colorama
  gui/
    main_window.py
    game_list_widget.py
    settings_widget.py
    workers.py               # QThread para collect/spread
    styles.qss
games_database.json          # Banco embarcado (75 jogos)
GameSaver.spec               # Build PyInstaller
tests/
  test_file_handler.py
  test_backup_service.py
  test_adapters.py
  test_bootstrap.py
  test_utils.py
```

Arquivos gerados em runtime (gitignored): `games.json`, `settings.json`, `SAVES/`, `Backup/`.

## Arquitetura

```
gamesaver/__main__.py  → argparse + bootstrap (GUI ou CLI)
gamesaver/constants.py → configuração global e paths (incl. PyInstaller frozen)
gamesaver/settings.py  → facade Settings (load/validate/save)
gamesaver/game_manager.py → facade CLI sobre BackupService
gamesaver/backup_service.py → orquestração pura: collect/spread
gamesaver/repositories.py → persistência JSON
gamesaver/path_policy.py → segurança de paths
gamesaver/file_handler.py → operações de I/O
gamesaver/gui/*        → camada de apresentação PyQt6 + workers assíncronos
```

### Responsabilidades

- **BackupService**: collect/spread sem print/input; retorna `BackupReport`.
- **GameManager**: adaptador CLI; imprime resultados e pede confirmação via terminal.
- **GameRepository**: carrega `games_database.json` + `games.json`.
- **SettingsRepository**: load/save de `settings.json`.
- **GUI**: uma instância de `GameManager`; operações via `OperationWorker` (QThread).

## Modelos de dados

### Jogo

```json
{
  "game": "Nome do Jogo",
  "path": "AppData/Roaming/GameFolder",
  "size": 0,
  "last_save": ""
}
```

- `games_database.json`: banco embarcado (75 entradas). Não editar manualmente em produção.
- `games.json`: jogos customizados do usuário. Mesclados em `GameManager.all_games`.

Paths são **relativos ao home do usuário**, separados por `/`.

### Settings

```json
{
  "user_location": "C:/Users/Gui",
  "destination_location": ".../SAVES",
  "mode": "collect"
}
```

Modos válidos: `collect`, `spread`, `""` (vazio).

## Segurança de paths

Obrigatório para qualquer operação de cópia:

1. `is_safe_game_path(path)` — bloqueia paths genéricos (`AppData`, `Documents`, etc.).
2. `validate_copy_paths(source, dest, user_location, destination_location)` — garante que origem ⊆ user e destino ⊆ pasta de backup.

```python
# file_handler.py — paths bloqueados
BLOCKED_EXACT_PATHS = {
    "AppData", "Documents", "Saved Games",
    "Documents/My Games", "AppData/Roaming", "AppData/Local",
}
```

Nunca contornar essas validações.

## PyInstaller (modo frozen)

`constants.py` trata executável empacotado:

- `BASE_DIR` = diretório do `.exe` quando `sys.frozen`.
- `DATABASE_PATH` e `STYLES_PATH` usam `sys._MEIPASS` quando empacotado.
- `games.json` e `settings.json` ficam ao lado do executável.

Ao adicionar assets empacotados, atualizar o workflow de release em `.github/workflows/release.yml`.

## Convenções de código

| Aspecto | Padrão |
|---------|--------|
| Naming | snake_case (exceção: `isGUI`, `loadGUI`) |
| Widgets GUI | método `init_ui()` para construção |
| Type hints | parciais — adicionar onde fizer sentido |
| Paths | normalizar com `/` via `normalize_path()` |
| Idioma do código | inglês (comentários e strings de UI) |
| Lint | ruff (`E`, `F`, `W`; line-length 120) |
| Testes | pytest com `tmp_path` |

### Dependências

- **Produção**: PyQt6, colorama
- **Dev**: pytest, ruff
- **Build**: pyinstaller

Evitar adicionar novas dependências sem necessidade clara.

## Comandos essenciais

```bash
# Desenvolvimento
pip install -r requirements.txt -r requirements-dev.txt
python -m gamesaver          # GUI
python -m gamesaver --cli    # CLI

# Qualidade
ruff check .
mypy
pytest -v --cov=gamesaver

# Build local (Windows)
pip install pyinstaller
pyinstaller GameSaver.spec --noconfirm --clean
```

Scripts auxiliares: `run.bat` / `run.sh` (mensagens em português).

## Workflows comuns

### Adicionar jogo ao banco embarcado

1. Adicionar entrada em `games_database.json` com path relativo ao home.
2. Verificar que o path passa em `is_safe_game_path()`.
3. Testar detecção com `user_location` apontando para home real.

### Adicionar feature na GUI

1. Implementar lógica em `game_manager.py` ou `file_handler.py`.
2. Conectar widget em `gui/` via sinais PyQt.
3. Manter tema em `gui/styles.qss` (escuro, accent `#007AFF`).
4. Não persistir settings na GUI sem salvar em `settings.json` (gap conhecido).

### Implementar spread (restore)

1. Inverter fluxo de `collect`: copiar de `destination_location` para `user_location + game.path`.
2. Reutilizar `validate_copy_paths` com origem/destino invertidos.
3. Implementar em `GameManager.spread()` e conectar botão na GUI.
4. Adicionar testes em `tests/`.

## Problemas conhecidos

| Issue | Detalhe |
|-------|---------|
| `images/icon.png` | Referenciado quando existente; ausente no repo |

Consulte [reference.md](reference.md) para detalhes de CI/CD, testes e checklist de PR.

## Checklist antes de entregar

- [ ] Lógica separada de UI
- [ ] Paths validados com funções de segurança
- [ ] Compatível com modo frozen (`constants.py`)
- [ ] `ruff check .` passa
- [ ] `pytest -v` passa
- [ ] Sem dependências desnecessárias
