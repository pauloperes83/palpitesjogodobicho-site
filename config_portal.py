# config_portal.py
COOKIES_HTML = """
<div id="cookie-banner" style="display: none; position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 400px; background: #1c222e; color: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); z-index: 9999; text-align: center; font-family: sans-serif; border: 1px solid #333;">
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
    (function() {
        if (!localStorage.getItem('cookiesAceitos')) {
            document.getElementById('cookie-banner').style.display = 'block';
        }
    })();
</script>
"""
