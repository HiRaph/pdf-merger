# pdf-merger

Piccolo programma che unisce **PDF e foto in un unico PDF**, pensato per chi deve raccogliere ogni giorno documenti scansionati e foto fatte col telefono in un solo file da archiviare o inviare.

L'ho scritto per velocizzare un lavoro che prima facevo a mano, file per file.

## Cosa fa

- prende tutti i PDF e le immagini (`.png`, `.jpg`, `.jpeg`) dalla cartella `input_files`
- raddrizza da solo le foto scattate col telefono (orientamento EXIF)
- crea `output_files/<nome>_<data>.pdf`: prima i PDF, poi le immagini, in ordine alfabetico
- sposta gli originali in `Archivio/<nome>_<data>/`, così `input_files` è pronta per il giro successivo
- non sovrascrive mai niente: se il file esiste già aggiunge `_2`, `_3`, …
- se qualcosa va storto durante l'unione non sposta né cancella nessun file

## Come si usa

```bash
pip install -r requirements.txt
python pdf_merger.py
```

1. Metti PDF e foto in `input_files` (la cartella viene creata al primo avvio)
2. Avvia il programma e scrivi il nome del file finale
3. Il PDF unito è in `output_files`

## Creare l'eseguibile per Windows

```bash
pip install pyinstaller
pyinstaller --onefile pdf_merger.py
```

L'eseguibile finisce in `dist/`. Mettilo in una cartella qualsiasi: `input_files`, `output_files` e `Archivio` vengono create accanto all'`.exe`.

## Tecnologie

Python 3 · [pypdf](https://pypi.org/project/pypdf/) · [Pillow](https://pypi.org/project/pillow/) · PyInstaller
