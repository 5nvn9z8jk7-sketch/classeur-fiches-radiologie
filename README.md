# Classeur de fiches radiologie

Sauvegarde du classeur de fiches d'aide à la lecture en radiologie (site web statique + PDF).

## Ouvrir le classeur hors ligne
1. Bouton vert **Code** → **Download ZIP**, puis décompresser.
2. Ouvrir `site/index.html` dans un navigateur.
   Pour que tout fonctionne (navigation, mode hors ligne), il est préférable de lancer un petit serveur local :
   `cd site && python3 -m http.server 8000` puis ouvrir http://localhost:8000

## Contenu
- `site/` : le site complet (fiches HTML dans `site/f/`, PDF dans `site/pdf/`, outils, registre).
- `site/pdf/Classeur-fiches-radiologie.pdf` : le classeur complet en PDF.
