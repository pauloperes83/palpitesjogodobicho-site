import os
from datetime import datetime, timedelta
import random
import subprocess

# ==========================================
# CONFIGURAÇÃO GITHUB
# ==========================================
USUARIO_GITHUB = "pauloperes83"
TOKEN_GITHUB = "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"
REPO_NOME = "pauloperes83/palpitesjogodobicho-site"
URL_AUTENTICADA = f"https://{USUARIO_GITHUB}:{TOKEN_GITHUB}@github.com/{REPO_NOME}.git"

bichos_oficiais = {
    "Avestruz": {"gr": "01", "dz": ["01", "02", "03", "04"], "e": "🦩", "puxa": "Vaca, Águia, Galo, Pavão, Peru"},
    "Águia": {"gr": "02", "dz": ["05", "06", "07", "08"], "e": "🦅", "puxa": "Coelho, Avestruz, Galo, Pavão, Peru"},
    "Burro": {"gr": "03", "dz": ["09", "10", "11", "12"], "e": "🫏", "puxa": "Cavalo, Elefante, Touro, Veado, Coelho, Cobra"},
    "Borboleta": {"gr": "04", "dz": ["13", "14", "15", "16"], "e": "🦋", "puxa": "Cabra, Elefante, Gato, Leão, Cachorro, Galo"},
    "Cachorro": {"gr": "05", "dz": ["17", "18", "19", "20"], "e": "🐕", "puxa": "Galo, Gato, Camelo, Macaco, Porco, Pavão"},
    "Cabra": {"gr": "06", "dz": ["21", "22", "23", "24"], "e": "🐐", "puxa": "Carneiro, Macaco, Elefante, Touro, Tigre, Urso"},
    "Carneiro": {"gr": "07", "dz": ["25", "26", "27", "28"], "e": "🐏", "puxa": "Cabra, Coelho, Vaca"},
    "Camelo": {"gr": "08", "dz": ["29", "30", "31", "32"], "e": "🐪", "puxa": "Cachorro, Elefante, Urso"},
    "Cobra": {"gr": "09", "dz": ["33", "34", "35", "36"], "e": "🐍", "puxa": "Jacaré, Porco, Burro, Gato"},
    "Coelho": {"gr": "10", "dz": ["37", "38", "39", "40"], "e": "🐰", "puxa": "Carneiro, Águia, Burro"},
    "Cavalo": {"gr": "11", "dz": ["41", "42", "43", "44"], "e": "🐎", "puxa": "Burro, Cabra, Touro"},
    "Elefante": {"gr": "12", "dz": ["45", "46", "47", "48"], "e": "🐘", "puxa": "Cabra, Urso, Tigre, Leão, Burro"},
    "Galo": {"gr": "13", "dz": ["49", "50", "51", "52"], "e": "🐓", "puxa": "Cachorro, Avestruz, Águia, Pavão, Peru"},
    "Gato": {"gr": "14", "dz": ["53", "54", "55", "56"], "e": "🐈", "puxa": "Cachorro, Leão, Tigre, Cobra"},
    "Jacaré": {"gr": "15", "dz": ["57", "58", "59", "60"], "e": "🐊", "puxa": "Cobra, Porco, Borboleta, Macaco"},
    "Leão": {"gr": "16", "gr_num": "16", "dz": ["61", "62", "63", "64"], "e": "🦁", "puxa": "Elefante, Gato, Tigre, Urso"},
    "Macaco": {"gr": "17", "dz": ["65", "66", "67", "68"], "e": "🐒", "puxa": "Cachorro, Cabra, Peru, Jacaré"},
    "Porco": {"gr": "18", "dz": ["69", "70", "71", "72"], "e": "🐷", "puxa": "Cobra, Peru, Jacaré, Cachorro"},
    "Pavão": {"gr": "19", "dz": ["73", "74", "75", "76"], "e": "🦚", "puxa": "Avestruz, Águia, Galo, Peru"},
    "Peru": {"gr": "20", "dz": ["77", "78", "79", "80"], "e": "🦃", "puxa": "Avestruz, Águia, Galo, Pavão, Veado"},
    "Touro": {"gr": "21", "dz": ["81", "82", "83", "84"], "e": "🐂", "puxa": "Vaca, Burro, Cabra"},
    "Tigre": {"gr": "22", "dz": ["85", "86", "87", "88"], "e": "🐅", "puxa": "Gato, Leão, Cabra"},
    "Urso": {"gr": "23", "dz": ["89", "90", "91", "92"], "e": "🐻", "puxa": "Leão, Elefante, Camelo, Cabra"},
    "Veado": {"gr": "24", "dz": ["93", "94", "95", "96"], "e": "🦌", "puxa": "Peru, Burro, Cabra"},
    "Vaca": {"gr": "25", "dz": ["97", "98", "99", "00"], "e": "🐄", "puxa": "Touro, Avestruz, Carneiro"}
}

def get_bicho_pela_dezena(dezena):
    d = int(dezena)
    if d == 0: d = 100
    for nome, dados in bichos_oficiais.items():
        gr = int(dados["gr"])
        if ((gr * 4) - 3) <= d <= (gr * 4) or (gr == 25 and (d >= 97 or d == 0)): return nome
    return "Avestruz"

def get_bicho_pelo_grupo(grupo):
    for nome, dados in bichos_oficiais.items():
        if int(dados["gr"]) == int(grupo): return nome
    return "Avestruz"

def gerar_palpites_html(dia):
    final_bichos = []
    lista_escolhidos = []
    def adicionar(n, d):
        if n not in lista_escolhidos and len(lista_escolhidos) < 6:
            lista_escolhidos.append(n); final_bichos.append((n, d))
    
    b_dia = get_bicho_pelo_grupo(dia)
    b_dir = get_bicho_pela_dezena(str(dia).zfill(2))
    dz_esp = str(dia*10) if dia < 10 else str(dia)[::-1].zfill(2)
    b_esp = get_bicho_pela_dezena(dz_esp)
    
    for b in [b_dia, b_dir, b_esp]: adicionar(b, str(dia).zfill(2) if b != b_esp else dz_esp)
    for b in [b_dia, b_dir, b_esp]:
        for p in bichos_oficiais[b]["puxa"].split(", "): 
            adicionar(p, random.choice(bichos_oficiais[p]["dz"]))

    palpites_html = ""
    for n, d in final_bichos:
        info = bichos_oficiais[n]
        palpites_html += f'<div class="palpite-box"><h3>{info["gr"]} - {n.upper()} {info["e"]}</h3><div class="numbers-grid"><div>Milhar: {random.randint(1,9)}{random.randint(1,9)}{d}</div><div>Centena: {random.randint(1,9)}{d}</div><div>Dezena: {d}</div></div></div>'
    return palpites_html

def salvar_e_push():
    agora = datetime.now()
    hoje_str = agora.strftime("%d/%m/%Y")
    dia = agora.day
    
    css = "<style>body{font-family:sans-serif;padding:20px;line-height:1.6}.container{max-width:800px;margin:0 auto}.palpite-box{background:#f4f4f4;padding:15px;margin:15px 0;border-radius:10px;border-left:5px solid #b8860b}.numbers-grid{display:grid;grid-template-columns:1fr 1fr 1fr;font-weight:bold;color:#b8860b}.btn-apostar{display:inline-block;background:#b8860b;color:#fff;padding:15px 30px;text-decoration:none;border-radius:8px;font-weight:bold;margin:10px 0}.btn-whats{display:block;background:#25d366;color:#fff;padding:15px;text-align:center;text-decoration:none;font-weight:bold;border-radius:50px;margin-top:20px}</style>"
    header = f'<header style="background:#121722;padding:20px;text-align:center"><a href="index.html"><img src="images/logo-palpites.png" height="80"></a></header>'

    # RIO
    p_rio = gerar_palpites_html(dia)
    html_rio = f'<html><head><title>Palpite Rio {hoje_str}</title>{css}</head><body>{header}<div class="container"><h1>Palpite Rio {hoje_str}</h1><p>Confira os palpites para PTM, PT, PTV, PTN e Corujinha. Veja o <a href="https://resultadosdojogo.com/">resultado do bicho de hoje rio</a>.</p><div style="text-align:center"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU" class="btn-apostar">APOSTAR NO RIO</a></div>{p_rio}</div></body></html>'
    with open("/var/www/meusite/palpite-do-bicho-rj.html", "w", encoding="utf-8") as f: f.write(html_rio)

    # LOOK
    p_look = gerar_palpites_html(dia)
    html_look = f'<html><head><title>Palpite Look Goiás {hoje_str}</title>{css}</head><body>{header}<div class="container"><h1>Palpite Look Goiás {hoje_str}</h1><p>Palpites para Look e Goiânia. Veja o <a href="https://resultadosdojogo.com/">resultado look loterias de hoje</a>.</p><div style="text-align:center"><a href="https://app.valedasorteloterias.club/pr/g5P71dlw" class="btn-apostar">APOSTAR NA LOOK</a></div>{p_look}<a href="https://chat.whatsapp.com/HyYz0zMD1ovAaWeY99Jfpi" class="btn-whats">WHATSAPP LOOK GOIÁS</a></div></body></html>'
    with open("/var/www/meusite/palpite-do-bicho-look.html", "w", encoding="utf-8") as f: f.write(html_look)

    os.chdir("/var/www/meusite")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Fix SEO Rio & Look {hoje_str}"])
    subprocess.run(["git", "push", URL_AUTENTICADA, "main", "--force"])

if __name__ == "__main__":
    salvar_e_push()
