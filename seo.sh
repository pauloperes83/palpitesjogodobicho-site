#!/usr/bin/env python3
import os

# 1. Lê o código do Google do seu arquivo de texto
with open('header-seo.txt', 'r') as f:
    analytics_code = f.read()

# 2. Lista todos os arquivos .html do seu site
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 3. Se o código já não estiver na página, injeta após o <head>
        if 'G-9Y3FW10LC2' not in content:
            # Substitui <head> por <head> + código, ignorando se é maiúsculo ou minúsculo
            new_content = content.replace('<head>', '<head>\n' + analytics_code)
            new_content = new_content.replace('<HEAD>', '<HEAD>\n' + analytics_code)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Sucesso: Analytics injetado em {filename}")
        else:
            print(f"Aviso: Analytics já existia em {filename}")
