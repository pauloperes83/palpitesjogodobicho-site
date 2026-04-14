import datetime
import random
import re
import os

# CONFIGURAÇÕES
ARQUIVO_HTML = "/var/www/meusite/palpite-do-bicho-maluca-bahia.html"
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

# PUXADAS DA BAHIA (Focado em Gato e Tigre conforme seu SEO)
PUXADAS_BAHIA = [14, 22, 5, 9, 16, 13] 

def gerar_milhar(grupo):
    dezena = random.choice(TABELA_BICHOS[grupo]["dezenas"])
    return f"{random.randint(10, 99)}{dezena:02d}"

# --- LÓGICA DE HORÁRIO E CALENDÁRIO ---
agora = datetime.datetime.now()
data_alvo = agora.date()

if agora.hour >= 21:
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

# --- GERAÇÃO DOS BICHOS ---
bicho_dia_grupo = dia_num if dia_num <= 25 else (dia_num - 25)
bichos_finais = [bicho_dia_grupo]
for p in PUXADAS_BAHIA:
    if p not in bichos_finais and len(bichos_finais) < 6:
        bichos_finais.append(p)

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

    # Atualiza Data
    conteudo = re.sub(r"\d{2}/\d{2}/\d{4}", data_str, conteudo)

    # Atualiza dias COM e SEM "-feira" (IGNORECASE garante que pega "Segunda" ou "segunda")
    regex_com = r"(segunda-feira|terça-feira|quarta-feira|quinta-feira|sexta-feira|sábado|domingo)"
    conteudo = re.sub(regex_com, nome_com_feira, conteudo, flags=re.IGNORECASE)

    regex_sem = r"(?<!-)(segunda|terça|quarta|quinta|sexta)(?!-feira)"
    conteudo = re.sub(regex_sem, nome_sem_feira, conteudo, flags=re.IGNORECASE)

    partes = conteudo.split(CHAVE)
    if len(partes) >= 3:
        novo_html = partes[0] + html_cards + partes[2]
        with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
            f.write(novo_html)

        os.system(f"cd /var/www/meusite && git add {ARQUIVO_HTML}")
        os.system(f'cd /var/www/meusite && git commit -m "Auto Update Maluca {data_str}"')
        os.system("cd /var/www/meusite && git push origin main -f")
        print(f"✅ SUCESSO BAHIA! Atualizado para {nome_com_feira} ({data_str}).")
