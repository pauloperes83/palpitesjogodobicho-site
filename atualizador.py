import os
from datetime import datetime
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

def get_bicho_pela_dezena(dezena):
    d = int(dezena)
    if d == 0: d = 100
    for nome, dados in bichos_oficiais.items():
        gr = int(dados["gr"])
        if ((gr * 4) - 3) <= d <= (gr * 4) or (gr == 25 and (d >= 97 or d == 0)): return nome
    return "Avestruz"

def gerar_palpites_html(dia):
    dz1 = str(dia).zfill(2)
    b1 = get_bicho_pela_dezena(dz1)
    dz2 = str(dia) + "0" if dia < 10 else str(dia)[::-1].zfill(2)
    b2 = get_bicho_pela_dezena(dz2)
    px = random.sample(bichos_oficiais[b1]["puxa"].split(", "), 2) + random.sample(bichos_oficiais[b2]["puxa"].split(", "), 2)
    final = list(dict.fromkeys([(b1, dz1), (b2, dz2)] + [(p, random.choice(bichos_oficiais[p]["dz"])) for p in px]))[:6]
    html = ""
    for n, d in final:
        info = bichos_oficiais[n]
        html += f'''<div class="palpite-box"><div class="bicho-title"><h3>{info["gr"]} - {n.upper()} {info["e"]}</h3></div><div class="numbers-grid"><div class="num-card"><label>Milhares</label><span>{random.randint(1,9)}{random.randint(1,9)}{d}</span></div><div class="num-card"><label>Centenas</label><span>{random.randint(1,9)}{d}</span></div><div class="num-card"><label>Dezenas</label><span>{d}</span></div></div></div>'''
    return html

def salvar_e_push():
    agora = datetime.now()
    hoje = agora.strftime("%d/%m/%Y")
    dia = agora.day
    palpites_txt = gerar_palpites_html(dia)
    key_principal = f"Palpite do dia do Jogo do Bicho de hoje Rio {hoje}"

    grid_bichos = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; margin-top: 20px;">'
    for nome, dados in bichos_oficiais.items():
        grid_bichos += f'<div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; text-align: center; background: #fff;"><div style="font-weight: bold; font-size: 0.9rem; color: #121722; margin-bottom: 5px;">{dados["gr"]}</div><div style="font-size: 2rem;">{dados["e"]}</div><div style="font-weight: bold; font-size: 0.8rem; margin: 5px 0;">{nome.upper()}</div><div style="font-size: 0.75rem; color: #d4a017; font-weight: bold;">{" ".join(dados["dz"])}</div></div>'
    grid_bichos += '</div>'

    css = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"><style>
        .dropdown-content { display: none; position: absolute; background-color: #121722; min-width: 160px; box-shadow: 0px 8px 16px rgba(0,0,0,0.5); z-index: 99; border: 1px solid rgba(255,255,255,0.1); text-align: left; }
        .dropdown-content a { margin: 0 !important; padding: 12px 16px !important; display: block !important; font-size: 14px !important; }
        .dropdown:hover .dropdown-content { display: block; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #ffffff; color: #333; margin: 0; padding: 0; line-height: 1.8; }
        .container { width: 95%; max-width: 1000px; margin: 0 auto; }
        header { background: #121722; padding: 20px 0; border-bottom: 3px solid #f6c945; text-align: center; }
        .logo img { height: 150px; width: auto; }
        nav { background: #121722; padding: 12px 0; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.08); }
        nav a { color: #d8dcec; text-decoration: none; margin: 0 15px; font-weight: 600; font-size: 15px; text-transform: uppercase; }
        .section { padding: 40px 0; }
        h1 { font-size: 2.2rem; color: #222; text-align: center; margin-bottom: 25px; }
        h2 { font-size: 1.6rem; color: #b8860b; border-left: 6px solid #f6c945; padding-left: 15px; margin: 35px 0 20px 0; }
        p { margin-bottom: 15px; font-size: 1.1rem; color: #444; text-align: justify; }
        .link-seo { color: #d4a017; font-weight: bold; text-decoration: underline; }
        .palpite-box { background: #f9f9f9; border: 1px solid #eee; border-radius: 12px; padding: 20px; margin: 25px 0; }
        .numbers-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; text-align: center; }
        .num-card { border: 1px solid #ddd; padding: 10px; border-radius: 8px; background: #fff; }
        .num-card span { display: block; font-weight: bold; font-size: 1.1rem; color: #d4a017; }
        .btn-apostar { display: inline-block; background: #b8860b; color: white; padding: 18px 40px; border-radius: 10px; text-decoration: none; font-weight: bold; text-transform: uppercase; margin-top: 20px; box-shadow: 0 4px 15px rgba(184,134,11,0.4); }
        .btn-whats { display: block; width: fit-content; margin: 30px auto; background: #25d366; color: white; padding: 15px 35px; border-radius: 50px; text-decoration: none; font-weight: bold; text-align: center; }
        .site-footer { background-color: #0d1016; border-top: 1px solid rgba(255,255,255,0.08); padding: 50px 0 30px 0; text-align: center; margin-top: 50px; color: #fff; }
        .footer-social svg { width: 30px; height: 30px; fill: #ffffff; margin: 0 10px; transition: 0.3s; }
        @media (max-width: 768px) { .logo img { height: 100px; } nav a { margin: 0 5px; font-size: 12px; } }
    </style>'''

    def build_page(title, kw, btn_link, btn_text):
        intro = f"Você está procurando pelo <strong>{kw}</strong>? Chegou ao lugar certo. O Jogo do Bicho é uma das tradições mais enraizadas no cotidiano fluminense."
        intro2 = f"Entender as tendências de cada extração é fundamental para quem busca um <strong>palpite fácil do jogo do bicho do rio de janeiro</strong>. Nossa equipe analisa diariamente milhares de resultados para oferecer a você as melhores indicações para PTM, PT, PTV, PTN e Corujinha."

        # LINKS INTERNOS DEFINIDOS PELO USUÁRIO
        link_puxadas = '<a href="https://palpitesjogodobicho.com.br/puxadas-do-bicho.html" class="link-seo">puxadas do bicho</a>'
        link_milheres = '<a href="https://palpitesjogodobicho.com.br/milhares-viciadas.html" class="link-seo">Milhares Viciadas</a>'
        link_palpite_dia = '<a href="https://palpitesjogodobicho.com.br/palpite-do-dia.html" class="link-seo">Palpite do Dia</a>'

        corpo_texto = f'''
        <h2>Análise Semântica: {kw}</h2>
        <p>Para obter um bom desempenho nas apostas, é essencial acompanhar o <strong>resultado pt rio</strong> e observar quais bichos estão com maior frequência de saída nos sorteios atuais.</p>
        <p>Nosso método de análise cruza dados históricos para gerar um <strong>palpite do dia</strong> que faça sentido com as extrações anteriores, como o importante <strong>resultado da rio ptm</strong>.</p>
        <p>Garantimos que você não jogue apenas na sorte, mas com base em estatística sólida para o seu <strong>{kw}</strong>, aumentando suas chances de acerto em todas as bancas.</p>
        
        <h2>Estratégia para o {kw}</h2>
        <p>Muitos jogadores buscam por um <strong>palpite fácil do jogo o bicho do rio de janeiro</strong> logo após as primeiras extrações da manhã, visando lucrar nas rodadas seguintes.</p>
        <p>Ao analisar o comportamento das dezenas, conseguimos identificar padrões que auxiliam na escolha de milhares e centenas viciadas, facilitando o seu <strong>{kw}</strong>.</p>
        <p>Lembre-se que o <strong>resultado do jogo do bicho de hoje rio</strong> serve como termômetro fundamental para as extrações da tarde e também para a Corujinha da noite.</p>
        
        <h2>Dicas para o {kw} e a Federal</h2>
        <p>A Loteria Federal de quartas e sábados é o momento mais esperado por quem segue o <strong>{kw}</strong>, pois define prêmios maiores em todo o território nacional.</p>
        <p>Para ter sucesso na Federal, é crucial analisar o <strong>resultado da federal</strong> anterior e cruzar com o nosso <strong>palpite fácil do jogo do bicho do rio de janeiro</strong> atualizado.</p>
        <p>O sorteio da Federal ocorre pontualmente às 20h, e nossos estudos indicam que as dezenas sugeridas para o <strong>{kw}</strong> possuem altíssima taxa de conversão nessa modalidade.</p>
        
        <h2>Como Jogar no Jogo do Bicho</h2>
        <p>O Jogo do Bicho consiste em apostar em animais que representam grupos de números. Cada bicho possui quatro dezenas específicas que definem o sorteio.</p>
        <p>Você pode apostar de diversas formas, como no grupo seco, dezenas, centenas ou milhares, sendo que cada modalidade possui um multiplicador de prêmio diferente.</p>
        <p>Uma excelente forma de planejar sua jogada é consultar o {link_palpite_dia} para ver quais animais estão com maior probabilidade de aparecer no dia de hoje.</p>

        <h2>Como ganhar no Jogo do Bicho</h2>
        <p>Aumentar suas chances envolve o uso de técnicas como o estudo das {link_puxadas}, que indicam quais bichos tendem a sair após uma determinada extração.</p>
        <p>Além disso, o uso de tabelas de {link_milheres} ajuda a identificar combinações que possuem um histórico de maior frequência nos sorteios do Rio e Goiás.</p>
        <p>Utilizando o nosso <strong>{kw}</strong>, você combina intuição com dados técnicos, transformando uma aposta comum em uma jogada estratégica e consciente.</p>
        '''

        return f'''<!DOCTYPE html><html lang="pt-BR"><head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9Y3FW10LC2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9Y3FW10LC2');</script>
<link rel="icon" type="image/png" href="images/favicon.png"><link rel="shortcut icon" href="images/favicon.png">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{css}</head><body>
<header><div class="container"><a href="index.html" class="logo"><img src="images/logo-palpites.png"></a></div></header>
<nav><div class="container">
    <a href="index.html">Início</a><a href="palpite-do-dia.html">Palpite do Dia</a>
    <div class="dropdown" style="display: inline-block; position: relative;"><a href="#" style="cursor: default; margin-right: 15px;">Bancas ▾</a>
    <div class="dropdown-content"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU" target="_blank">Águia Prime</a><a href="https://app.valedasorteloterias.club/pr/g5P71dlw" target="_blank">Vale da Sorte</a></div></div>
    <a href="puxadas-do-bicho.html">Puxadas</a><a href="milhares-viciadas.html">Milhares</a><a href="https://resultadosdojogo.com/" target="_blank" style="color: #f6c945;">Resultados</a>
</div></nav>
<section class="section"><div class="container">
    <div style="text-align: center; margin-bottom: 25px;"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU"><img src="images/aguia-posts.webp" style="width: 300px; border-radius: 8px;"></a></div>
    <h1>{kw}</h1>
    <p>{intro}</p><p>{intro2}</p>
    <div style="text-align: center;"><a href="{btn_link}" class="btn-apostar">{btn_text}</a></div>
    {palpites_txt}
    <a href="https://chat.whatsapp.com/HyYz0zMD1ovAaWeY99Jfpi" class="btn-whats" target="_blank">RECEBER PALPITES NO WHATSAPP</a>
    {corpo_texto}
    {grid_bichos}
    <p style="text-align: center; font-weight: bold; margin-top: 30px; font-size: 1.2rem; color: #b8860b;">🍀 Desejamos muita sorte em suas apostas e que os palpites de hoje tragam ótimos prêmios! 🍀</p>
</div></section>
<footer class="site-footer"><div class="container">
    <div class="footer-title" style="font-size:1.8rem; color:#f6c945; font-weight:bold;">Palpites Jogo do Bicho</div>
    <p style="font-size:0.85rem; color:#888ea1; max-width:700px; margin:20px auto; text-align: center;">Esclarecemos que não temos vínculo com o serviço ou pessoas que operam o Jogo do Bicho e que os resultados e estatísticas são meramente informativos.</p>
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 30px;">
        <a href="https://www.instagram.com/palpitess_jb"><svg viewBox="0 0 24 24"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm0 2.2A2.8 2.8 0 0 0 4.2 7v10A2.8 2.8 0 0 0 7 19.8h10a2.8 2.8 0 0 0 2.8-2.8V7A2.8 2.8 0 0 0 17 4.2H7Zm10.6 1.6a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2.2A2.8 2.8 0 1 0 12 14.8 2.8 2.8 0 0 0 12 9.2Z"/></svg></a>
        <a href="https://www.facebook.com/palpitesdobicho"><svg viewBox="0 0 24 24"><path d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.5 1.6-1.5h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.4v2.2H8v3.2h2.1V22h3.4Z"/></svg></a>
        <a href="https://www.youtube.com/@Palpitesdo_JogodoBicho"><svg viewBox="0 0 24 24"><path d="M23 12s0-3.1-.4-4.6a3 3 0 0 0-2.1-2.1C19 5 12 5 12 5s-7 0-8.5.4A3 3 0 0 0 1.4 7.4C1 8.9 1 12 1 12s0 3.1.4 4.6a3 3 0 0 0 2.1 2.1C5 19 12 19 12 19s7 0 8.5-.4a3 3 0 0 0 2.1-2.1c.4-1.5.4-4.5.4-4.5ZM9.8 15.5v-7L16 12l-6.2 3.5Z"/></svg></a>
    </div>
    <div style="display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-bottom:30px;">
        <a href="sobre.html" style="color:#d8dcec; text-decoration:none;">Sobre nós</a>
        <a href="contato.html" style="color:#d8dcec; text-decoration:none;">Contato</a>
        <a href="politica-de-privacidade.html" style="color:#d8dcec; text-decoration:none;">Privacidade</a>
        <a href="termos-de-uso.html" style="color:#d8dcec; text-decoration:none;">Termos de Uso</a>
    </div>
    <p style="font-size:0.8rem; color:#565d6d; border-top:1px solid rgba(255,255,255,0.05); padding-top:20px; text-align: center;">© 2026 Palpites Jogo do Bicho. Todos os direitos reservados.</p>
</div></footer></body></html>'''

    with open("/var/www/meusite/palpite-do-bicho-rj.html", 'w', encoding='utf-8') as f:
        f.write(build_page(f"Palpite Rio {hoje}", key_principal, "https://app.aguiaprime119000.com/pr/y8X6LEBU", "🎰 APOSTAR NO RIO"))
    
    with open("/var/www/meusite/palpite-do-bicho-look.html", 'w', encoding='utf-8') as f:
        f.write(build_page(f"Palpite Look {hoje}", f"Palpite da Look Loterias de hoje Goiás {hoje}", "https://app.valedasorteloterias.club/pr/g5P71dlw", "🎰 APOSTAR NA LOOK"))

    os.chdir("/var/www/meusite")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"SEO Internal Links Fix {hoje}"])
    subprocess.run(["git", "push", "origin", "main", "--force"])

if __name__ == "__main__":
    salvar_e_push()
