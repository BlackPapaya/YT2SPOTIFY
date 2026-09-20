from pathlib import Path
from PIL import Image

# 1. Ordner festlegen
basis_ordner = Path(r"C:\Users\graym\Desktop\Ablauf")

# 2. Schleife über jede PNG-Datei im Ordner
for bild_pfad in basis_ordner.glob("*.png"):
    
    # 3. Zielpfad erzeugen (tauscht .png durch .jpg aus)
    ziel_pfad = bild_pfad.with_suffix(".jpg")
    
    # 4. Bild öffnen
    with Image.open(bild_pfad) as img:
        # 5. PNGs haben oft Transparenz (RGBA) -> in RGB umwandeln für JPG
        rgb_img = img.convert("RGB")
        
        # 6. Als JPG speichern
        rgb_img.save(ziel_pfad)

print("Alle PNGs wurden erfolgreich in JPGs umgewandelt!")