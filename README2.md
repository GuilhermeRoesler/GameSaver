# 🎮 GameSaver - Gerencie seus Saves de Jogos com Facilidade

## 📌 Sobre o Projeto
O **GameSaver** é uma ferramenta poderosa para gerenciar os saves de todos os jogos encontrados no computador do usuário. Ele permite:
✅ **Backup automático** dos saves de todos os jogos detectados.
✅ **Restauração rápida** para evitar perdas de progresso.
✅ **Sincronização** de uma pasta de saves personalizada com os respectivos jogos.
✅ **Suporte a múltiplos jogos**, garantindo compatibilidade com diversas plataformas.

## 🚀 Como Funciona?
O GameSaver escaneia o computador em busca de saves de jogos e os armazena de maneira organizada. Ele também pode distribuir saves previamente armazenados para os respectivos diretórios dos jogos, garantindo que o usuário tenha sempre seu progresso salvo e disponível.

## 🛠️ Tecnologias Utilizadas
- **Python 3.13.2**
- **Bibliotecas:** `os`, `sys`, `shutil`, `json`, `tkinter` (para interface gráfica, se aplicável)

## 📥 Instalação
1. **Clone este repositório:**
   ```sh
   git clone https://github.com/seu-usuario/SaveSync.git
   cd SaveSync
   ```
2. **Instale as dependências necessárias:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Execute o script:**
   ```sh
   python savesync.py
   ```

## 🎛️ Como Usar?
1. **Abra o SaveSync**
2. **Selecione a opção desejada:**
   - Fazer backup de todos os saves.
   - Restaurar saves de uma pasta específica.
3. **Aguarde o processo ser concluído!**

## 📂 Estrutura do Projeto
```
SaveSync/
│── savesync.py          # Arquivo principal do programa
│── config.json          # Arquivo de configuração do usuário
│── saves/               # Pasta onde os backups são armazenados
│── spread/              # Pasta contendo saves a serem espalhados
│── logs/                # Arquivos de log para depuração
│── README.md            # Documentação do projeto
```

## ❗ Observações
- Certifique-se de executar o script com permissões adequadas para acessar as pastas dos jogos.
- O programa pode exigir ajustes manuais para compatibilidade com alguns jogos.

## 🤝 Contribuição
Contribuições são bem-vindas! Siga os passos:
1. Fork este repositório
2. Crie uma branch (`git checkout -b feature-minha-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona minha feature'`)
4. Envie um push para a branch (`git push origin feature-minha-feature`)
5. Abra um Pull Request

## 📜 Licença
Este projeto está sob a licença **MIT**. Sinta-se livre para usá-lo e modificá-lo conforme necessário.

---
Desenvolvido com 💙 por [Seu Nome](https://github.com/seu-usuario)

