import datetime
import random
import re
import os
from git_safe import enviar_pro_github

# CONFIGURAÇÕES
ARQUIVO_HTML = "/var/www/meusite/palpite-do-bicho-sp.html"
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

def gerar_milhar(grupo):
    dezena = random.choice(TABELA_BICHOS[grupo]["dezenas"])
    return f"{random.randint(10, 99)}{dezena:02d}"

# Lógica de Horário (as 22h vira o dia para o palpite de amanhã)
agora = datetime.datetime.now()
data_alvo = agora.date()
if agora.hour >= 20:
    data_alvo = data_alvo + datetime.timedelta(days=1)

data_str = data_alvo.strftime("%d/%m/%Y")
dia = data_alvo.day
mes = data_alvo.month

# LÓGICA EXCLUSIVA SP: SOMA BASE 9
b1 = ((dia + mes) * 9) % 25
if b1 == 0: b1 = 25

bichos_finais = []
atual = b1
for _ in range(25): # Tenta encontrar 6 bichos únicos usando saltos de 9
    if atual not in bichos_finais:
        bichos_finais.append(atual)
    if len(bichos_finais) == 6:
        break
    atual = (atual + 9) % 25
    if atual == 0: atual = 25

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

# Gravação e Git
if os.path.exists(ARQUIVO_HTML):
    os.system("git config --global --add safe.directory /var/www/meusite")
    with open(ARQUIVO_HTML, "r", encoding="utf-8") as f:
        conteudo = f.read()

    conteudo = re.sub(r"\d{2}/\d{2}/\d{4}", data_str, conteudo)
    partes = conteudo.split(CHAVE)

    if len(partes) >= 3:
        novo_html = partes[0] + html_cards + partes[2]
        with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
            f.write(novo_html)

        enviar_pro_github(data_str, "São Paulo")
        print(f"✅ SUCESSO SP! Soma Base 9 enviada para {data_str}")
    else:
        print(f"❌ ERRO: Marcas {CHAVE} não encontradas em SP!")
