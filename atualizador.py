import os
from datetime import datetime, timedelta
import random
import subprocess

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
    "Leão": {"gr": "16", "dz": ["61", "62", "63", "64"], "e": "🦁", "puxa": "Elefante, Gato, Tigre, Urso"},
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

def gerar_palpites_html():
    res = ""
    for _ in range(6):
        b = random.choice(list(bichos_oficiais.keys()))
        info = bichos_oficiais[b]
        dz = random.choice(info["dz"])
        res += f'<div class="palpite-box"><h3>{info["gr"]} - {b.upper()} {info["e"]}</h3><div class="numbers-grid"><div>Milhar: {random.randint(1,9)}{random.randint(1,9)}{dz}</div><div>Centena: {random.randint(1,9)}{dz}</div><div>Dezena: {dz}</div></div></div>'
    return res

def salvar():
    agora = datetime.now()
    hoje = agora.strftime("%d/%m/%Y")
    p = gerar_palpites_html()
    css = '<style>body{font-family:sans-serif;padding:20px;line-height:1.6}.container{max-width:800px;margin:0 auto}.palpite-box{background:#f4f4f4;padding:15px;margin:10px 0;border-radius:8px;border-left:5px solid #b8860b}.numbers-grid{display:grid;grid-template-columns:1fr 1fr 1fr;font-weight:bold;color:#b8860b}.btn-apostar{display:inline-block;background:#b8860b;color:#fff;padding:10px 20px;text-decoration:none;border-radius:5px;margin:10px 0}.btn-whats{display:block;background:#25d366;color:#fff;padding:15px;text-align:center;text-decoration:none;font-weight:bold;border-radius:50px;margin-top:20px}</style>'
    header = f'<header style="background:#121722;padding:20px;text-align:center"><a href="index.html"><img src="images/logo-palpites.png" height="80"></a></nav></header>'
    
    # RIO
    html_rio = f'<html><head><title>Palpite Rio {hoje}</title>{css}</head><body>{header}<div class="container"><h1>Palpite Rio de Janeiro {hoje}</h1><p>Confira os palpites para PTM, PT, PTV, PTN e Corujinha do Rio. Veja o <a href="https://resultadosdojogo.com/">resultado do jogo do bicho de hoje rio</a>.</p><div style="text-align:center"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU" class="btn-apostar">APOSTAR NO RIO</a></div>{p}<hr><h2>Palpite Federal</h2><p>Palpites válidos para quarta e sábado.</p></div></body></html>'
    with open("palpite-do-bicho-rj.html", "w", encoding="utf-8") as f: f.write(html_rio)

    # LOOK
    html_look = f'<html><head><title>Palpite Look Goiás {hoje}</title>{css}</head><body>{header}<div class="container"><h1>Palpite Look Loterias Goiás {hoje}</h1><p>Palpites para a Look de Goiás e Goiânia. Confira o <a href="https://resultadosdojogo.com/">resultado look loterias de hoje</a> e Lotece.</p><div style="text-align:center"><a href="https://app.valedasorteloterias.club/pr/g5P71dlw" class="btn-apostar">APOSTAR NA LOOK</a></div>{p}<a href="https://chat.whatsapp.com/HyYz0zMD1ovAaWeY99Jfpi" class="btn-whats">WHATSAPP LOOK GOIÁS</a></div></body></html>'
    with open("palpite-do-bicho-look.html", "w", encoding="utf-8") as f: f.write(html_look)

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Update {hoje}"])
    subprocess.run(["git", "push", "origin", "main", "--force"])

if __name__ == "__main__": salvar()
