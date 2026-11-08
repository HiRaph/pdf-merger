"""
pdf_merger - unisce PDF e foto in un unico PDF.

Come funziona:
  1. metti i PDF e le immagini (.png, .jpg, .jpeg) nella cartella input_files
  2. avvia il programma e scrivi il nome del file finale
  3. trovi il PDF unito in output_files/<nome>_<data>.pdf
  4. i file originali vengono spostati in Archivio/<nome>_<data>/ e input_files si svuota

Prima vengono i PDF, poi le immagini, ciascun gruppo in ordine alfabetico.
Le foto scattate col telefono vengono raddrizzate in automatico (orientamento EXIF).
"""

import io
import os
import re
import shutil
import sys
from datetime import datetime

from PIL import Image, ImageOps
from pypdf import PdfWriter

# Quando gira come .exe (PyInstaller) le cartelle stanno accanto all'eseguibile
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "input_files")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_files")
ARCHIVE_DIR = os.path.join(BASE_DIR, "Archivio")

PDF_EXT = (".pdf",)
IMG_EXT = (".png", ".jpg", ".jpeg")


def fine(codice=0):
    """Aspetta Invio prima di chiudere, così la finestra del .exe non sparisce subito."""
    input("\nPremi Invio per uscire...")
    sys.exit(codice)


def pulisci_nome(testo):
    """Toglie i caratteri non validi nei nomi file e usa _ al posto degli spazi."""
    testo = re.sub(r'[<>:"/\\|?*]', "", testo)
    return re.sub(r"[\s_]+", "_", testo).strip("_")


def percorso_libero(percorso):
    """Se il file o la cartella esiste già, aggiunge _2, _3, ... invece di sovrascrivere."""
    if not os.path.exists(percorso):
        return percorso
    base, ext = os.path.splitext(percorso)
    n = 2
    while os.path.exists(f"{base}_{n}{ext}"):
        n += 1
    return f"{base}_{n}{ext}"


def immagine_in_pdf(path):
    """Converte un'immagine in una pagina PDF (in memoria)."""
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode != "RGB":
            img = img.convert("RGB")
        buffer = io.BytesIO()
        img.save(buffer, format="PDF", resolution=150)
    buffer.seek(0)
    return buffer


def main():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = sorted(f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f)))
    pdf_files = [f for f in files if f.lower().endswith(PDF_EXT)]
    image_files = [f for f in files if f.lower().endswith(IMG_EXT)]
    ignorati = [f for f in files if f not in pdf_files and f not in image_files and f.lower() != "desktop.ini"]

    print(f"Trovati {len(pdf_files)} PDF e {len(image_files)} immagini.")
    if ignorati:
        print("Ignoro questi file (non sono PDF o immagini):", ", ".join(ignorati))
    if not pdf_files and not image_files:
        print("La cartella input_files è vuota, niente da fare.")
        fine(1)

    nome = pulisci_nome(input("Scrivi il nome per il PDF finale: "))
    if not nome:
        print("Nessun nome inserito, annullo.")
        fine(1)

    data = datetime.now().strftime("%Y-%m-%d")
    nome_finale = f"{nome}_{data}"
    output_path = percorso_libero(os.path.join(OUTPUT_DIR, nome_finale + ".pdf"))

    writer = PdfWriter()
    try:
        for f in pdf_files:
            writer.append(os.path.join(INPUT_DIR, f))
        for f in image_files:
            writer.append(immagine_in_pdf(os.path.join(INPUT_DIR, f)))
        with open(output_path, "wb") as out:
            writer.write(out)
    except Exception as e:
        print(f"Errore durante la creazione del PDF: {e}")
        print("Non ho spostato né cancellato niente.")
        fine(1)
    finally:
        writer.close()

    print(f"PDF creato: {output_path}")

    # Sposta gli originali in archivio così input_files è pronta per il prossimo giro
    archivio = percorso_libero(os.path.join(ARCHIVE_DIR, nome_finale))
    os.makedirs(archivio, exist_ok=True)
    non_spostati = []
    for f in pdf_files + image_files:
        try:
            shutil.move(os.path.join(INPUT_DIR, f), os.path.join(archivio, f))
        except OSError as e:
            non_spostati.append(f"{f} ({e})")

    if non_spostati:
        print("Questi file non sono stati spostati (forse sono aperti in un altro programma):")
        for f in non_spostati:
            print(" -", f)
    else:
        print(f"Originali spostati in: {archivio}")
        if not ignorati:
            print("input_files svuotata.")

    fine(0)


if __name__ == "__main__":
    main()
