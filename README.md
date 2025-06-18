# ⚽ Quiz Interativo de Futebol - Champions League

Este projeto é um *quiz interativo sobre futebol* focado na UEFA Champions League, com perguntas baseadas em *dados reais da Base dos Dados (basedosdados.org). Desenvolvido em **Python, o sistema conta com uma **interface gráfica (Tkinter), integração com a **Google Cloud, geração dinâmica de perguntas e funcionalidades completas de **CRUD para perguntas personalizadas*.

---

## 📌 Funcionalidades

- 🧠 Perguntas automáticas com dados reais da Champions League
- 🧾 CRUD completo (Adicionar, Editar, Excluir perguntas)
- 🎯 Pontuação automática ao final do quiz
- 🔁 Botão “Jogar Novamente”
- 🎨 Interface gráfica com Tkinter
- ☁ Integração com a [Base dos Dados](https://basedosdados.org/) via API
- 🔐 Autenticação com credentials.json da Google Cloud

---

## 🧠 Exemplos de Perguntas Geradas

- Quantos jogos foram decididos por pênaltis na temporada 2013/14?
- Qual foi o maior público registrado na temporada 2016/17?
- Quantos gols de bola parada o time mandante marcou em 2020/21?

As perguntas são geradas com base em consultas SQL feitas diretamente à base da Champions League.

---

## 💻 Tecnologias Utilizadas

| Tecnologia     | Finalidade                              |
|----------------|------------------------------------------|
| Python 3       | Lógica e integração de dados             |
| Tkinter        | Interface gráfica do quiz                |
| Basedosdados   | Consulta de dados públicos em SQL        |
| Pandas         | Manipulação de dados tabulares           |
| Google Cloud   | Autenticação para acesso aos dados       |
| OS / JSON      | Gerenciamento de arquivos e credenciais  |

---
Tela das Perguntas 
![Imagem do WhatsApp de 2025-06-18 à(s) 11 00 22_29053d9d](https://github.com/user-attachments/assets/b04ad01f-bb82-4857-bf3b-8ad23ce89cf5)

Tela Final do Quiz
![Imagem do WhatsApp de 2025-06-18 à(s) 11 01 32_3d6b3a71](https://github.com/user-attachments/assets/58ec4bf6-2aee-4c79-831b-bc1ef522f5c8)

Tela de Geração e gerenciamento de Perguntas

![Imagem do WhatsApp de 2025-06-18 à(s) 11 04 37_ce4b77a8](https://github.com/user-attachments/assets/b3cda22d-07a5-4153-a835-4e81f51a396e)


## 🚀 Como Executar

1. *Clone o repositório:*

```bash
git clone https://github.com/Joaomendes31/Quiz-Interativo-da-Champions-League.git
cd quiz-champions

2 . *pip install basedosdados pandas*

3. *Configure as credenciais do Google Cloud:*

Crie um projeto no Google Cloud

Ative o billing e a API da BigQuery

Baixe o arquivo credentials.json e importe no seu codigo
