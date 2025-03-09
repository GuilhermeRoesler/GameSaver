# GameSave Manager 🎮

O **GameSave Manager** é uma ferramenta desenvolvida em Python que facilita o gerenciamento de saves de jogos no computador do usuário. Com ele, você pode **salvar automaticamente** os arquivos de save de todos os jogos encontrados no sistema, além de ter a opção de **espalhar** uma pasta de saves para todos os respectivos jogos. Ideal para quem deseja manter seus progressos seguros ou migrar saves entre diferentes máquinas.

---

## Funcionalidades ✨

- **Backup Automático**: Detecta e salva automaticamente os arquivos de save de todos os jogos instalados no computador.
- **Restauração de Saves**: Espalha uma pasta de saves para os respectivos jogos, garantindo que seus progressos sejam restaurados corretamente.
- **Interface Simples**: Fácil de usar, com opções claras para backup e restauração.
- **Compatibilidade**: Funciona com a maioria dos jogos, independentemente da plataforma (Steam, Epic Games, Origin, etc.).
- **Personalização**: Permite ao usuário escolher diretórios específicos para backup e restauração.

---

## Como Usar 🛠️

### Pré-requisitos
- Python 3.x instalado.
- Bibliotecas necessárias (listadas em `requirements.txt`).

### Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/gamesave-manager.git
Navegue até o diretório do projeto:

bash
Copy
cd gamesave-manager
Instale as dependências:

bash
Copy
pip install -r requirements.txt
Executando o Programa
Execute o script principal:

bash
Copy
python main.py
Siga as instruções no terminal para realizar backup ou restauração de saves.

Estrutura do Projeto 📂
Copy
gamesave-manager/
├── backups/                  # Pasta onde os saves são armazenados
├── logs/                     # Logs de operações realizadas
├── src/                      # Código-fonte do projeto
│   ├── backup_manager.py     # Lógica de backup
│   ├── restore_manager.py    # Lógica de restauração
│   └── utils.py              # Funções utilitárias
├── requirements.txt          # Dependências do projeto
├── main.py                   # Script principal
└── README.md                 # Este arquivo
Contribuição 🤝
Contribuições são bem-vindas! Se você deseja melhorar este projeto, siga os passos abaixo:

Faça um fork do repositório.

Crie uma branch para sua feature (git checkout -b feature/nova-feature).

Commit suas mudanças (git commit -m 'Adicionando nova feature').

Push para a branch (git push origin feature/nova-feature).

Abra um Pull Request.

Licença 📜
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

Contato 📧
Se tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato:

Email: seu-email@exemplo.com

GitHub: seu-usuario

GameSave Manager - Mantenha seus saves seguros e organizados! 🚀

Copy

Este README.md é profissional, organizado e esteticamente agradável, com emojis e formatação que facilitam a leitura e o entendimento do projeto.