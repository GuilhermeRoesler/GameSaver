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
| `spread` | ⚠️ Stub | Restore — ainda não implementado |
| GUI (PyQt6) | ✅ Padrão | `isGUI = True` em `main.py` |
| CLI (colorama) | ✅ Alternativo | `isGUI = False` |

## Estrutura do projeto

```
main.py              # Entry point (GUI ou CLI)
constants.py         # Paths, defaults, textos ASCII
settings.py          # Classe Settings (load/validate/prompt CLI)
game_manager.py      # Detecção de jogos, collect/spread
file_handler.py      # I/O JSON, cópia, validação de paths
utils.py             # Helpers de terminal colorido
games_database.json  # Banco embarcado (75 jogos, versionado)
gui/
  main_window.py     # QMainWindow principal
  game_list_widget.py
  settings_widget.py
  styles.qss         # Tema escuro (#1E1E1E, accent #007AFF)
tests/
  test_file_handler.py
  test_utils.py
```

Arquivos gerados em runtime (gitignored): `games.json`, `settings.json`, `SAVES/`, `Backup/`.

## Arquitetura

```
main.py          → bootstrap (GUI ou CLI)
constants.py     → configuração global e paths (incl. PyInstaller frozen)
settings.py      → objeto Settings com load/validate
game_manager.py  → orquestração: detectar jogos, collect/spread
file_handler.py  → operações de I/O e segurança de paths
utils.py         → utilitários de terminal
gui/*            → camada de apresentação PyQt6
```

### Responsabilidades

- **GameManager**: carrega `games_database.json` + `games.json`, detecta jogos instalados, executa backup.
- **file_handler**: JSON I/O, `shutil.copytree`, validação de segurança de paths.
- **Settings**: carrega/valida `settings.json`; prompts interativos no CLI.
- **GUI**: widgets PyQt6 com sinais (`SettingsWidget.locations_changed` atualiza lista de jogos).

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
python main.py

# Qualidade
ruff check .
pytest -v

# Build local (Windows)
pip install pyinstaller
pyinstaller --onefile --add-data "games_database.json;." --add-data "gui/styles.qss;gui" main.py
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
| CLI quebrado | `main.py` passa args a `GameManager(...)`, mas `__init__` não aceita |
| Settings GUI | Alterações não persistem em `settings.json` |
| Size na tabela | Hardcoded `'0 Kb'` |
| `images/icon.png` | Referenciado em `main.py`, ausente no repo |
| `get_save_destination()` | Lógica inconsistente com `copy_selected_games()` |

Consulte [reference.md](reference.md) para detalhes de CI/CD, testes e checklist de PR.

## Checklist antes de entregar

- [ ] Lógica separada de UI
- [ ] Paths validados com funções de segurança
- [ ] Compatível com modo frozen (`constants.py`)
- [ ] `ruff check .` passa
- [ ] `pytest -v` passa
- [ ] Sem dependências desnecessárias
