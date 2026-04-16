import datetime
import random
import re
import os
from config_portal import COOKIES_HTML
from git_safe import enviar_pro_github

# CONFIGURAÇÕES
ARQUIVO_HTML = "/var/www/meusite/palpite-do-bicho-nacional.html"
CHAVE = "<!--MARCA_AQUI-->"

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

PUXADAS = {
    1: [3, 4, 13, 22], 2: [5, 12, 11, 21], 3: [1, 4, 13, 11], 4: [3, 1, 13, 14],
    5: [2, 12, 11, 18], 6: [7, 18, 14, 25], 7: [6, 18, 14, 21], 8: [9, 10, 23, 21],
    9: [8, 10, 15, 23], 10: [8, 9, 23, 11], 11: [12, 5, 2, 21], 12: [11, 5, 2, 21],
    13: [5, 1, 2, 19, 20], 14: [15, 6, 7, 18], 15: [14, 16, 9, 10], 16: [15, 14, 9, 10],
    17: [18, 1, 4, 24], 18: [17, 6, 7, 5], 19: [20, 1, 13, 22], 20: [19, 1, 13, 22],
    21: [22, 11, 12, 2, 25], 22: [21, 23, 1, 13], 23: [22, 21, 8, 9], 24: [25, 23, 1, 17],
    25: [24, 21, 6, 7]
}

def gerar_milhar(grupo):
    dezena = random.choice(TABELA_BICHOS[grupo]["dezenas"])
    return f"{random.randint(10, 99)}{dezena:02d}"

# --- LÓGICA DE HORÁRIO PARA NACIONAL (23:15) ---
agora = datetime.datetime.now()
data_alvo = agora.date()

# Se rodar a partir das 23h, vira o dia para amanhã
if agora.hour >= 23:
    data_alvo = data_alvo + datetime.timedelta(days=1)

data_str = data_alvo.strftime("%d/%m/%Y")
dia_num = data_alvo.day
dezena_inv = int(str(dia_num).zfill(2)[::-1])
# -----------------------------------------------

bicho_dia = dia_num if dia_num <= 25 else (dia_num - 25)
bichos_finais = [bicho_dia]

for p in PUXADAS[bicho_dia]:
    if p not in bichos_finais:
        bichos_finais.append(p)

proximo_bicho = bicho_dia + 1 if bicho_dia < 25 else 1
for p in PUXADAS[proximo_bicho]:
    if len(bichos_finais) < 6:
        if p not in bichos_finais:
            bichos_finais.append(p)

# Gerar HTML das 6 caixas
html_cards = "\n" + CHAVE + "\n"
for num in bichos_finais[:6]:
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

if os.path.exists(ARQUIVO_HTML):
    print(f"--- Iniciando Processo Nacional para: {ARQUIVO_HTML} ---")
    os.system("git config --global --add safe.directory /var/www/meusite")

    with open(ARQUIVO_HTML, "r", encoding="utf-8") as f:
        conteudo = f.read()

    contagem = conteudo.count(CHAVE)
    print(f"DEBUG: Encontrei a marca {CHAVE} -> {contagem} vezes no arquivo.")

    conteudo = re.sub(r"\d{2}/\d{2}/\d{4}", data_str, conteudo)
    texto_dezenas_novo = f"({dia_num:02d} e {dezena_inv:02d})"
    conteudo = re.sub(r"\(\d{2} e \d{2}\)", texto_dezenas_novo, conteudo)

    partes = conteudo.split(CHAVE)
    if len(partes) >= 3:
        novo_html = partes[0] + html_cards + partes[2]

        # Injeta o banner de cookies (Alinhado dentro do IF)
        if "cookie-banner" not in novo_html:
            novo_html = novo_html.replace("</body>", COOKIES_HTML + "</body>")

        # Salva o arquivo oficial (Alinhado dentro do IF)
        with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
            f.write(novo_html)

        # Envia para o GitHub com os 3 argumentos (Alinhado dentro do IF)
        enviar_pro_github(ARQUIVO_HTML, data_str, "Nacional")

        print(f"✅ SUCESSO NACIONAL! Cookies e Blindagem ativos ({data_str}).")
