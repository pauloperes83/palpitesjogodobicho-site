import datetime
import random
import re
import os
from config_portal import COOKIES_HTML
from git_safe import enviar_pro_github

# CONFIGURAÇÕES
ARQUIVO_HTML = "/var/www/meusite/palpite-do-bicho-paratodos-bahia.html"
CHAVE = "<!--MARCA_AQUI-->"

# Tabela Oficial
TABELA_BICHOS = {
    1: {"nome": "AVESTRUZ", "dezenas": [1, 2, 3, 4]}, 2: {"nome": "ÁGUIA", "dezenas": [5, 6, 7, 8]},
    3: {"nome": "BURRO", "dezenas": [9, 10, 11, 12]}, 4: {"nome": "BORBOLETA", "dezenas": [13, 14, 15, 16]},
    5: {"nome": "CACHORRO", "dezenas": [17, 18, 19, 20]}, 6: {"nome": "CABRA", "dezenas": [21, 22, 23, 24]},
    7: {"nome": "CARNEIRO", "dezenas": [25, 26, 27, 28]}, 8: {"nome": "CAMELO", "dezenas": [29, 30, 31, 32]},
    9: {"nome": "COBRA", "dezenas": [33, 34, 35, 36]}, 10: {"nome": "COELHO", "dezenas": [37, 38, 39, 40]},
    11: {"nome": "CAVALO", "dezenas": [41, 42, 43, 44]}, 12: {"nome": "ELEFANTE", "dezenas": [45, 46, 47, 48]},
    13: {"nome": "GALO", "dezenas": [49, 50, 51, 52]}, 14: {"nome": "GATO", "dezenas": [53, 54, 55, 56]},
    15: {"nome": "JACARÉ", "dezenas": [57, 58, 59, 60]}, 16: {"nome": "LEÃO", "dezenas": [61, 62, 63, 64]},
    17: {"nome": "MACACO", "dezenas": [65, 66, 67, 68]}, 18: {"nome": "PORCO", "dezenas": [69, 70, 71, 72]},
    19: {"nome": "PAVÃO", "dezenas": [73, 74, 75, 76]}, 20: {"nome": "PERU", "dezenas": [77, 78, 79, 80]},
    21: {"nome": "TOURO", "dezenas": [81, 82, 83, 84]}, 22: {"nome": "TIGRE", "dezenas": [85, 86, 87, 88]},
    23: {"nome": "URSO", "dezenas": [89, 90, 91, 92]}, 24: {"nome": "VEADO", "dezenas": [93, 94, 95, 96]},
    25: {"nome": "VACA", "dezenas": [97, 98, 99, 0]}
}

def gerar_milhar(grupo):
    dezena = random.choice(TABELA_BICHOS[grupo]["dezenas"])
    return f"{random.randint(10, 99)}{dezena:02d}"

# --- LÓGICA DE HORÁRIO E CALENDÁRIO ---
agora = datetime.datetime.now()
data_alvo = agora.date()

# Gatilho às 21h igual aos outros da Bahia
if agora.hour >= 19:
    data_alvo = data_alvo + datetime.timedelta(days=1)

data_str = data_alvo.strftime("%d/%m/%Y")
dia_num = data_alvo.day

dias_com_feira = {
    0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
    3: "quinta-feira", 4: "sexta-feira", 5: "sábado", 6: "domingo"
}
dias_sem_feira = {
    0: "segunda", 1: "terça", 2: "quarta",
    3: "quinta", 4: "sexta", 5: "sábado", 6: "domingo"
}

nome_com_feira = dias_com_feira[data_alvo.weekday()]
nome_sem_feira = dias_sem_feira[data_alvo.weekday()]

# --- ESTRATÉGIA PARATODOS: GRUPOS VIZINHOS + SEO ---
bicho_dia = dia_num if dia_num <= 25 else (dia_num - 25)

# Vizinhos de tabela (Cerca quem vem antes e depois)
vizinho_antes = bicho_dia - 1 if bicho_dia > 1 else 25
vizinho_depois = bicho_dia + 1 if bicho_dia < 25 else 1

# Lista baseada na estratégia + bicho do SEO (Camelo 08 e Peru 20)
bichos_finais = []
for b in [bicho_dia, vizinho_antes, vizinho_depois, 8, 20]:
    if b not in bichos_finais:
        bichos_finais.append(b)

# Preenche com aleatório se faltar para chegar em 6
while len(bichos_finais) < 6:
    r = random.randint(1, 25)
    if r not in bichos_finais:
        bichos_finais.append(r)

# Gerar HTML
html_cards = "\n" + CHAVE + "\n"
for num in bichos_finais:
    m = gerar_milhar(num)
    nome_bicho = TABELA_BICHOS[num]["nome"]
    html_cards += f'''    <div class="palpite-box">
        <div class="bicho-title"><h3>{num:02d} - {nome_bicho}</h3></div>
        <div class="numbers-grid">
            <div class="num-card"><label>Milhar</label><span>{m}</span></div>
            <div class="num-card"><label>Centena</label><span>{m[1:]}</span></div>
            <div class="num-card"><label>Dezena</label><span>{m[2:]}</span></div>
        </div>
    </div>\n'''
html_cards += CHAVE + "\n"

# --- GRAVAÇÃO E GITHUB ---
if os.path.exists(ARQUIVO_HTML):
    os.system("git config --global --add safe.directory /var/www/meusite")
    with open(ARQUIVO_HTML, "r", encoding="utf-8") as f:
        conteudo = f.read()

    conteudo = re.sub(r"\d{2}/\d{2}/\d{4}", data_str, conteudo)

    # Atualiza dias COM e SEM "-feira"
    regex_com = r"(segunda-feira|terça-feira|quarta-feira|quinta-feira|sexta-feira|sábado|domingo)"
    conteudo = re.sub(regex_com, nome_com_feira, conteudo, flags=re.IGNORECASE)

    regex_sem = r"(?<!-)(segunda|terça|quarta|quinta|sexta)(?!-feira)"
    conteudo = re.sub(regex_sem, nome_sem_feira, conteudo, flags=re.IGNORECASE)

    partes = conteudo.split(CHAVE)
    if len(partes) >= 3:
        novo_html = partes[0] + html_cards + partes[2]

        # Injeta o banner de cookies
        if "cookie-banner" not in novo_html:
            novo_html = novo_html.replace("</body>", COOKIES_HTML + "</body>")

        # Salva o arquivo oficial
        with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
            f.write(novo_html)

        # Envia para o GitHub (Com os 3 argumentos obrigatórios)
        enviar_pro_github(ARQUIVO_HTML, data_str, "Paratodos Bahia")

        print(f"✅ SUCESSO PARATODOS! Cookies e Blindagem ativos.")
