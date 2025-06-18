import os
import random
import tkinter as tk
from tkinter import messagebox
import basedosdados as bd
import pandas as pd

# Configuração da chave de autenticação e billing
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais.json"
billing_id = "meuprojeto2732"

# --- CONSULTAS À BASE DOS DADOS ---

query_publico = """
SELECT temporada, publico_max
FROM basedosdados.mundo_transfermarkt_competicoes_internacionais.champions_league
WHERE publico_max IS NOT NULL AND temporada IS NOT NULL
"""
df_publico = bd.read_sql(query_publico, billing_project_id=billing_id)
df_publico = df_publico[df_publico['publico_max'] > 50000].drop_duplicates()

query_penalti = """
SELECT temporada, COUNT(CASE WHEN penalti = 1 THEN 1 END) AS jogos_penalti
FROM basedosdados.mundo_transfermarkt_competicoes_internacionais.champions_league
WHERE penalti IS NOT NULL AND temporada IS NOT NULL
GROUP BY temporada
HAVING jogos_penalti > 0
"""
df_penalti = bd.read_sql(query_penalti, billing_project_id=billing_id)

# --- GERAÇÃO DAS PERGUNTAS ---


def gerar_perguntas_publico(df, n=5):
    perguntas_geradas = []
    for _ in range(n):
        linha = df.sample(1).iloc[0]
        temporada = linha["temporada"]
        correta = linha["publico_max"]
        alternativas = set()
        alternativas.add(correta)
        while len(alternativas) < 4:
            delta = random.randint(1000, 15000)
            alt = correta + random.choice([-delta, delta])
            if alt > 0:
                alternativas.add(alt)
        alternativas = list(alternativas)
        random.shuffle(alternativas)
        perguntas_geradas.append({
            "pergunta": f"👥 Qual foi o maior público da temporada {temporada}?",
            "alternativas": {
                "A": f"{alternativas[0]} pessoas",
                "B": f"{alternativas[1]} pessoas",
                "C": f"{alternativas[2]} pessoas",
                "D": f"{alternativas[3]} pessoas"
            },
            "resposta": "ABCD"[alternativas.index(correta)]
        })
    return perguntas_geradas


def gerar_perguntas_penalti(df, n=5):
    perguntas = []
    for _ in range(n):
        linha = df.sample(1).iloc[0]
        temporada = linha["temporada"]
        correta = linha["jogos_penalti"]
        alternativas = set()
        alternativas.add(correta)
        while len(alternativas) < 4:
            delta = random.randint(1, 5)
            alt = correta + random.choice([-delta, delta])
            if alt >= 0:
                alternativas.add(alt)
        alternativas = list(alternativas)
        random.shuffle(alternativas)
        perguntas.append({
            "pergunta": f"⚽ Na temporada {temporada}, quantos jogos foram decididos nos pênaltis?",
            "alternativas": {
                "A": f"{alternativas[0]} jogos",
                "B": f"{alternativas[1]} jogos",
                "C": f"{alternativas[2]} jogos",
                "D": f"{alternativas[3]} jogos"
            },
            "resposta": "ABCD"[alternativas.index(correta)]
        })
    return perguntas


# Lista com todas as perguntas
perguntas = gerar_perguntas_publico(
    df_publico) + gerar_perguntas_penalti(df_penalti)

# --- INTERFACE GRÁFICA ---


class QuizFutebol:
    def _init_(self, master):
        self.master = master
        self.pontuacao = 0
        self.pergunta_atual = 0

        master.title("Quiz de Futebol")
        master.configure(bg="#1e1e2f")

        self.label_pergunta = tk.Label(master, text="", font=("Arial", 16, "bold"),
                                       fg="white", bg="#1e1e2f", wraplength=480, justify="left")
        self.label_pergunta.pack(pady=(30, 20))

        self.botoes = []
        for i in range(4):
            botao = tk.Button(master, text="", width=40, font=("Arial", 14),
                              bg="#3b3b5c", fg="white", activebackground="#5c5ca3",
                              relief="flat", command=lambda i=i: self.verificar_resposta(i))
            botao.pack(pady=6)
            self.botoes.append(botao)

        self.label_pontuacao = tk.Label(master, text="Pontuação: 0", font=("Arial", 14, "bold"),
                                        fg="white", bg="#1e1e2f")
        self.label_pontuacao.pack(pady=10)

        self.label_feedback = tk.Label(master, text="", font=("Arial", 16, "bold"),
                                       bg="#1e1e2f")
        self.label_feedback.pack(pady=10)

        # Botão "Gerenciar Perguntas" fixado no rodapé
        self.botao_gerenciar = tk.Button(master, text="Gerenciar Perguntas",
                                         font=("Arial", 12), bg="#2f2f4f", fg="white",
                                         activebackground="#4f4f7a", command=self.abrir_gerenciador)
        self.botao_gerenciar.pack(side="bottom", fill="x", pady=(20, 10))

        self.exibir_pergunta()

    def reiniciar_quiz(self):
        global perguntas
        perguntas = gerar_perguntas_publico(
            df_publico) + gerar_perguntas_penalti(df_penalti)
        self.pontuacao = 0
        self.pergunta_atual = 0
        self.botao_jogar_novamente.destroy()
        for botao in self.botoes:
            botao.pack()
        self.exibir_pergunta()

    def exibir_pergunta(self):
        if self.pergunta_atual < len(perguntas):
            p = perguntas[self.pergunta_atual]
            self.label_pergunta.config(
                text=f"Pergunta {self.pergunta_atual + 1}:\n{p['pergunta']}")
            for i, letra in enumerate("ABCD"):
                self.botoes[i].config(
                    text=f"{letra}) {p['alternativas'][letra]}", state="normal", bg="#3b3b5c")
            self.label_feedback.config(text="")
        else:
            self.label_pergunta.config(
                text=f"🏁 Fim do quiz! Você acertou {self.pontuacao} de {len(perguntas)}.")
            for botao in self.botoes:
                botao.pack_forget()
            self.label_feedback.config(
                text="Obrigado por jogar!", fg="#00BFFF")

            self.botao_jogar_novamente = tk.Button(
                self.master, text="🔁 Jogar Novamente", font=("Arial", 14, "bold"),
                bg="#4CAF50", fg="white", command=self.reiniciar_quiz
            )
            self.botao_jogar_novamente.pack(pady=20)

    def verificar_resposta(self, i):
        p = perguntas[self.pergunta_atual]
        letra = "ABCD"[i]
        if letra == p["resposta"]:
            self.pontuacao += 1
            self.label_feedback.config(text="✅ Correto!", fg="#7CFC00")
            self.botoes[i].config(bg="#7CFC00")
        else:
            certa = p["resposta"]
            texto_certo = f"{certa}) {p['alternativas'][certa]}"
            self.label_feedback.config(
                text=f"❌ Errado! Resposta certa: {texto_certo}", fg="#FF6347")
            self.botoes[i].config(bg="#FF6347")
            for j, letra_opcao in enumerate("ABCD"):
                if letra_opcao == certa:
                    self.botoes[j].config(bg="#7CFC00")

        self.label_pontuacao.config(text=f"Pontuação: {self.pontuacao}")
        for b in self.botoes:
            b.config(state="disabled")
        self.master.after(2000, self.proxima_pergunta)

    def proxima_pergunta(self):
        self.pergunta_atual += 1
        self.exibir_pergunta()

    def abrir_gerenciador(self):
        def atualizar_lista():
            listbox.delete(0, tk.END)
            for idx, p in enumerate(perguntas):
                listbox.insert(tk.END, f"{idx+1}. {p['pergunta']}")

        def adicionar():
            def salvar():
                nova = {
                    "pergunta": entrada_pergunta.get(),
                    "alternativas": {
                        "A": entrada_a.get(),
                        "B": entrada_b.get(),
                        "C": entrada_c.get(),
                        "D": entrada_d.get()
                    },
                    "resposta": resposta_var.get().upper()
                }
                perguntas.append(nova)
                atualizar_lista()
                janela.destroy()

            janela = tk.Toplevel(root)
            janela.title("Adicionar Pergunta")

            tk.Label(janela, text="Pergunta:").pack()
            entrada_pergunta = tk.Entry(janela, width=60)
            entrada_pergunta.pack()

            entrada_a = tk.Entry(janela, width=60)
            entrada_b = tk.Entry(janela, width=60)
            entrada_c = tk.Entry(janela, width=60)
            entrada_d = tk.Entry(janela, width=60)
            tk.Label(janela, text="Alternativa A:").pack()
            entrada_a.pack()
            tk.Label(janela, text="Alternativa B:").pack()
            entrada_b.pack()
            tk.Label(janela, text="Alternativa C:").pack()
            entrada_c.pack()
            tk.Label(janela, text="Alternativa D:").pack()
            entrada_d.pack()

            tk.Label(janela, text="Letra da resposta correta (A-D):").pack()
            resposta_var = tk.StringVar()
            tk.Entry(janela, textvariable=resposta_var, width=5).pack()

            tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

        def excluir():
            sel = listbox.curselection()
            if sel:
                perguntas.pop(sel[0])
                atualizar_lista()

        def editar():
            idx = listbox.curselection()
            if not idx:
                return
            p = perguntas[idx[0]]

            janela = tk.Toplevel(root)
            janela.title("Editar Pergunta")

            entrada_pergunta = tk.Entry(janela, width=60)
            entrada_pergunta.insert(0, p["pergunta"])
            entrada_pergunta.pack()

            entrada_a = tk.Entry(janela, width=60)
            entrada_b = tk.Entry(janela, width=60)
            entrada_c = tk.Entry(janela, width=60)
            entrada_d = tk.Entry(janela, width=60)
            entrada_a.insert(0, p["alternativas"]["A"])
            entrada_b.insert(0, p["alternativas"]["B"])
            entrada_c.insert(0, p["alternativas"]["C"])
            entrada_d.insert(0, p["alternativas"]["D"])

            entrada_a.pack()
            entrada_b.pack()
            entrada_c.pack()
            entrada_d.pack()

            resposta_var = tk.StringVar(value=p["resposta"])
            tk.Entry(janela, textvariable=resposta_var, width=5).pack()

            def salvar():
                p["pergunta"] = entrada_pergunta.get()
                p["alternativas"] = {
                    "A": entrada_a.get(),
                    "B": entrada_b.get(),
                    "C": entrada_c.get(),
                    "D": entrada_d.get()
                }
                p["resposta"] = resposta_var.get().upper()
                atualizar_lista()
                janela.destroy()

            tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

        win = tk.Toplevel(root)
        win.title("Gerenciar Perguntas")
        listbox = tk.Listbox(win, width=80)
        listbox.pack()
        atualizar_lista()

        tk.Button(win, text="Adicionar", command=adicionar).pack(
            side=tk.LEFT, padx=5)
        tk.Button(win, text="Editar", command=editar).pack(
            side=tk.LEFT, padx=5)
        tk.Button(win, text="Excluir", command=excluir).pack(
            side=tk.RIGHT, padx=5)


# --- EXECUTAR ---
root = tk.Tk()
root.geometry("560x560")
app = QuizFutebol(root)
root.mainloop()