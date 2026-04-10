import os
import re

with open('header-seo.txt', 'r', encoding='utf-8') as f:
    tag = f.read()

for nome in os.listdir('.'):
    if nome.endswith('.html'):
        with open(nome, 'r', encoding='utf-8') as f:
            html = f.read()
        if 'G-9Y3FW10LC2' not in html:
            novo_html = re.sub(r'(<head.*?>)', r'\1\n' + tag, html, flags=re.IGNORECASE)
            with open(nome, 'w', encoding='utf-8') as f:
                f.write(novo_html)
            print(f"OK: {nome}")
