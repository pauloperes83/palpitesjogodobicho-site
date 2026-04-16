import os
from datetime import datetime

# Configurações
DOMINIO = "https://palpitesjogodobicho.com.br"
PASTA_SITE = "/var/www/meusite"
ARQUIVO_SITEMAP = os.path.join(PASTA_SITE, "sitemap.xml")

# Páginas que você quer indexar (Manuais + Loterias)
paginas = [
    "index.html",
    "palpite-do-dia.html",
    "sonhos.html",
    "milhares-viciadas.html",
    "puxadas-do-bicho.html",
    "sobre.html",
    "contato.html",
    "politica-de-privacidade.html",
    "termos-de-uso.html",
    "palpite-do-bicho-rj.html",
    "palpite-do-bicho-look.html",
    "palpite-do-bicho-nacional.html",
    "palpite-do-bicho-lotece-ceara.html",
    "palpite-do-bicho-lotep.html",
    "palpite-do-bicho-sp.html",
    "palpite-do-bicho-paratodos-bahia.html",
    "palpite-do-bicho-maluca-bahia.html",
    "palpite-do-bicho-caminho-da-sorte.html"
]

hoje = datetime.now().strftime("%Y-%m-%d")

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for pagina in paginas:
    prioridade = "1.0" if pagina == "index.html" else "0.8"
    # Remove o .html da URL se você preferir links limpos, 
    # mas como seu servidor é estático, o ideal é manter como está o arquivo.
    link = f"{DOMINIO}/{pagina}"

    xml += f'  <url>\n'
    xml += f'    <loc>{link}</loc>\n'
    xml += f'    <lastmod>{hoje}</lastmod>\n'
    xml += f'    <changefreq>daily</changefreq>\n'
    xml += f'    <priority>{prioridade}</priority>\n'
    xml += f'  </url>\n'

xml += '</urlset>'

with open(ARQUIVO_SITEMAP, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"✅ Sitemap.xml gerado com {len(paginas)} páginas!")
