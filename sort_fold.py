from pathlib import Path

# 1. Hauptordner definieren
basis_ordner = Path(r"C:\Users\graym\Desktop\Ablauf")

# 2. Schleife über alle Elemente im Hauptordner
for i, unterordner in enumerate(basis_ordner.iterdir(), start=1):
    
    # 3. Prüfen, ob es wirklich ein Ordner ist
    if unterordner.is_dir():
        
        # 4. Neuen Namen generieren (z. B. Thema_01)
        neuer_name = f"Thema_{i:02d}"
        
        # 5. Neuen Pfad zusammenbauen
        ziel_pfad = basis_ordner / neuer_name
        
        # 6. Umbenennen ausführen
        unterordner.rename(ziel_pfad)