import os

pasta = "/var/www/meusite"
rodape_limpo = """  </footer>

  <script>
    function toggleMenu() {
      document.querySelector(".nav-links").classList.toggle("show");
    }
  </script>

  <div id="cookie-banner" style="display: block; position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 400px; background: #1c222e; color: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); z-index: 9999; text-align: center; font-family: sans-serif; border: 1px solid #333;">
      <p style="margin-bottom: 15px; font-size: 14px; line-height: 1.5;">
          🍪 Utilizamos cookies para melhorar sua experiência. Ao continuar navegando, você concorda com nossa <a href="politica-de-privacidade.html" style="color: #f6c945; text-decoration: underline;">Política de Privacidade</a>.
      </p>
      <button onclick="acceptCookies()" style="background: #f6c945; color: #121722; border: none; padding: 10px 30px; border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 14px; transition: 0.3s;">
          Aceitar e Fechar
      </button>
  </div>

  <script>
      function acceptCookies() {
          localStorage.setItem('cookiesAceitos', 'true');
          document.getElementById('cookie-banner').style.display = 'none';
      }
      if (localStorage.getItem('cookiesAceitos')) {
          document.getElementById('cookie-banner').style.display = 'none';
      }
  </script>
</body>
</html>"""

for arquivo_nome in os.listdir(pasta):
    if arquivo_nome.endswith(".html"):
        caminho = os.path.join(pasta, arquivo_nome)
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Procura onde termina o conteúdo principal (antes da briga do Git começar)
        if "</footer" in conteudo:
            parte_superior = conteudo.split("</footer")[0]
            novo_conteudo = parte_superior + rodape_limpo

            with open(caminho, "w", encoding="utf-8") as f:
                f.write(novo_conteudo)
            print(f"✅ {arquivo_nome} reconstruído e limpo!")
