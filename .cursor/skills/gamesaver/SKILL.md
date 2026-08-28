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

GameSaver detecta jogos instalados, copia pastas de save para uma pasta central de backup (`collect`) e restaura saves para os diretórios originais (`spread`).

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
  __main__.py                # argparse (--cli, -v), bootstrap GUI/CLI
  constants.py               # Paths e defaults (PyInstaller)
  cli_messages.py            # Textos ASCII do CLI
  logging_config.py          # logging padrão
  models.py                  # GameEntry, AppSettings, BackupReport
  path_policy.py             # Validação e resolução de paths
  backup_service.py          # Lógica collect/spread (sem I/O de UI)
  repositories.py            # GameRepository, SettingsRepository
  file_handler.py            # JSON I/O, bootstrap de arquivos
  file_utils.py              # Tamanho, timestamps, formatação
  game_manager.py            # Facade CLI (printc + logging)
  settings.py                # Facade de settings com prompts CLI
  utils.py                   # Helpers colorama
  gui/
    main_window.py
    window_icon.py
    game_list_widget.py
    settings_widget.py       # user/destination/mode + persistência
    workers.py               # QThread para collect/spread (cancelável)
    styles.qss
games_database.json
images/icon.png
images/icon.ico
GameSaver.spec
tests/
```

Arquivos gerados em runtime (gitignored): `games.json`, `settings.json`, `SAVES/`.

## Arquitetura

```
gamesaver/__main__.py      → argparse + bootstrap (GUI ou CLI)
gamesaver/constants.py     → paths e defaults (incl. PyInstaller frozen)
gamesaver/cli_messages.py  → banners CLI
gamesaver/logging_config.py → configure_logging / get_logger
gamesaver/settings.py      → facade Settings (load/validate/save)
gamesaver/game_manager.py  → facade CLI sobre BackupService
gamesaver/backup_service.py → orquestração pura: collect/spread
gamesaver/repositories.py  → persistência JSON
gamesaver/path_policy.py   → segurança de paths (pathlib)
gamesaver/file_handler.py  → I/O e bootstrap (games/settings/SAVES)
gamesaver/gui/*            → apresentação PyQt6 + workers assíncronos
```

### Responsabilidades

- **BackupService**: collect/spread sem print/input; retorna `BackupReport`.
- **GameManager**: adaptador CLI; feedback colorido + logging.
- **GameRepository**: carrega `games_database.json` + `games.json`.
- **SettingsRepository**: load/save de `settings.json`.
- **GUI**: uma instância de `GameManager`; operações via `OperationWorker` (QThread). Settings persistem em `settings.json`.

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
- `games.json`: jogos customizados do usuário. Mesclados via `GameRepository`.

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
2. `validate_copy_paths` / `validate_spread_paths` — usam `Path.resolve()` + `Path.relative_to()`.

```python
# path_policy.py — paths bloqueados
BLOCKED_EXACT_PATHS = {
    "AppData", "Documents", "Saved Games",
    "Documents/My Games", "AppData/Roaming", "AppData/Local",
}
```

Nunca contornar essas validações.

## PyInstaller (modo frozen)

`GameSaver.spec` deve usar `main.py` como script de entrada (imports absolutos). **Não** apontar `Analysis` para `gamesaver/__main__.py` — o PyInstaller roda o arquivo como script solto e os imports relativos falham com `ImportError: attempted relative import with no known parent package`.

`constants.py` trata executável empacotado:

- `BASE_DIR` = diretório do `.exe` quando `sys.frozen`.
- `DATABASE_PATH` e `STYLES_PATH` usam `sys._MEIPASS` quando empacotado.
- `games.json` e `settings.json` ficam ao lado do executável.
- Ícones: `images/icon.png` + `images/icon.ico` (ambos nos datas do spec). `EXE(icon=...)` usa o `.ico`.
- No Windows: `configure_windows_app_id()` + `apply_native_window_icon()` (`WM_SETICON` via Win32) para a barra de tarefas; preferir `.ico` em `gui/window_icon.py`.

Ao adicionar assets empacotados, atualizar `GameSaver.spec` e o workflow de release.

## Convenções de código

| Aspecto | Padrão |
|---------|--------|
| Naming | snake_case |
| Widgets GUI | método `init_ui()` para construção |
| Type hints | preferidos; mypy no CI |
| Paths | normalizar com `/` via `normalize_path()` |
| Idioma do código | inglês (comentários e strings de UI) |
| Lint | ruff (`E`, `F`, `W`; line-length 120) |
| Types | mypy |
| Testes | pytest + cobertura ≥ 60% no core |

### Dependências

- **Produção**: PyQt6, colorama
- **Dev**: pytest, pytest-cov, ruff, mypy
- **Build**: pyinstaller

Evitar adicionar novas dependências sem necessidade clara.

## Comandos essenciais

```bash
# Desenvolvimento
pip install -r requirements.txt -r requirements-dev.txt
python -m gamesaver          # GUI
python -m gamesaver --cli    # CLI
python -m gamesaver --cli -v # CLI com debug logs

# Qualidade
ruff check .
mypy
pytest -v --cov=gamesaver

# Build local
pip install -r requirements-build.txt
pyinstaller GameSaver.spec --noconfirm --clean
```

Scripts auxiliares: `run.bat` / `run.sh` (mensagens em português).

## Workflows comuns

### Adicionar jogo ao banco embarcado

1. Adicionar entrada em `games_database.json` com path relativo ao home.
2. Verificar que o path passa em `is_safe_game_path()`.
3. Testar detecção com `user_location` apontando para home real.

### Adicionar feature na GUI

1. Implementar lógica em `backup_service.py` (domínio) — não nos widgets.
2. Conectar widget em `gamesaver/gui/` via sinais PyQt / workers.
3. Manter tema em `gamesaver/gui/styles.qss` (escuro, accent `#007AFF`).
4. Persistência de settings via `Settings.save()` / `SettingsRepository`.

### Alterar collect/spread

1. Mudar `BackupService` e `path_policy`.
2. Cobrir com testes em `tests/test_backup_service.py`.
3. Adaptadores CLI/GUI consomem `BackupReport` — evitar lógica duplicada.

## Problemas conhecidos

Nenhum bug estrutural aberto no momento.

Consulte [reference.md](reference.md) para detalhes de CI/CD, testes e checklist de PR.

## Checklist antes de entregar

- [ ] Lógica no domínio (`BackupService`), UI só adapta
- [ ] Paths validados com `path_policy`
- [ ] Compatível com modo frozen (`constants.py`)
- [ ] `ruff check .` passa
- [ ] `mypy` passa
- [ ] `pytest -v --cov=gamesaver` passa
- [ ] Docs viva atualizadas se comportamento mudou
- [ ] Sem dependências desnecessárias
