import qrcode
from PIL import Image
import os


#Configuración

nombreArchivo = "casambi"
url_android = "https://play.google.com/store/apps/details?id=com.casambi.CBU"
url_ios = "https://apps.apple.com/es/app/casambi/id731859317"
logo_path = "logo.png"
output_folder = r"C:\Users\Lina\OneDrive\Escritorio\Python\Apuntes2024\casambi-redirect"

# === HTML inteligente ===

html_redireccion = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Redirigiendo a Casambi...</title>
  <style>
    body {{
      font-family: sans-serif;
      text-align: center;
      padding-top: 50px;
    }}
    img {{
      width: 200px;
      height: 200px;
    }}
  </style>
  <script>
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;

    if (/android/i.test(userAgent)) {{
      window.location.href = "{url_android}";
    }} else if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {{
      window.location.href = "{url_ios}";
    }} else {{
      document.write("Por favor, abre este enlace desde tu dispositivo móvil.");
    }}
  </script>
</head>
<body>
  <h2>Escanea el código QR</h2>
  <img src="{nombreArchivo}_qr.png" alt="Código QR Casambi">
</body>
</html>
"""
# === Crear carpeta de salida si no existe ===
#os.makedirs(output_folder, exist_ok=True)

# === Guardar HTML ===
html_path = os.path.join(output_folder, f"{nombreArchivo}.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_redireccion)

# === Crear QR ===
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data(f"https://linaramdez.github.io/casambi-redirect/casambi.html")  # Sustituye por la URL real de tu hosting
qr.make()
img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# === Insertar logo en el centro ===
if os.path.exists(logo_path):
    logo = Image.open(logo_path)

    # Redimensionar logo
    basewidth = int(img.size[0] / 4)  # el logo será 1/4 del tamaño del QR
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)
    
    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

# === Guardar QR ===
qr_output_path = os.path.join(output_folder, f"{nombreArchivo}_qr.png")
img.save(qr_output_path)

print("✅ ¡Listo! Se generaron:")
print(f" - {html_path}")
print(f" - {qr_output_path}")

