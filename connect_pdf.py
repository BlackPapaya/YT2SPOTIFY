from pathlib import Path
from pypdf import PdfWriter

# 1. Zielordner definieren
neuer_ordner = Path(r"C:\Users\graym\Desktop\Fügen")

# 2. Leeres PDF-Objekt erstellen
merger = PdfWriter()

# 3. Alle PDFs im Ordner durchgehen
for pdf_pfad in neuer_ordner.glob("*.pdf"):
    # Das spätere Ergebnis überspringen, falls es schon existiert
    if pdf_pfad.name == "Zusammenpdf.pdf":
        continue
        
    merger.append(pdf_pfad)

# 4. Zusammengefügtes PDF am Zielort speichern
merger.write(neuer_ordner / "Zusammenpdf.pdf")

print("Alles zusammengefügt!")