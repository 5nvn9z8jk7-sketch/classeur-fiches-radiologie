# Classeur de fiches radiologie

Sauvegarde du classeur de fiches d'aide à la lecture en radiologie (radiologues et internes), classées par organe.
Site en ligne : https://fiches-radiologie.pplx.app

## Ouvrir le classeur hors ligne
1. Bouton vert **Code** → **Download ZIP**, puis décompresser.
2. Ouvrir `site/index.html` dans un navigateur.
   Pour que tout fonctionne (navigation, mode hors ligne), il est préférable de lancer un petit serveur local :
   `cd site && python3 -m http.server 8000` puis ouvrir http://localhost:8000

## Contenu
- `site/` : le site complet, identique à la version en ligne (fiches HTML dans `site/f/`, PDF dans `site/pdf/`, calculateurs, registre des versions). C'est la version de référence.
- `site/pdf/Classeur-fiches-radiologie.pdf` : le classeur complet en PDF ; `site/pdf/Fiches-radiologie-par-organe.zip` : une fiche PDF par fichier.
- `site/f/CV-02-cr.html` : compte rendu type du score calcique, à remplir et à copier dans Word.
- `sources/` : fichiers de travail (contenu des fiches `src/fiches/`, scripts de génération des PDF `src/build.py` et `src/binder.py`, site `web/build_web.py`) et notes du projet (`NOTES-projet.md`).

## Attention
Les sources des fiches CV-02 (score calcique) et CO-02 (otospongiose) ne sont pas dans `sources/` : pour ces deux fiches, seule la version publiée dans `site/` existe. Ne pas reconstruire le site à partir de `sources/` sans les restaurer, sinon ces fiches disparaîtraient.

## Dernières modifications
- 30/10/2026 : CV-02, compte rendu type du score calcique (sans technique, bouton « Copier pour Word »), lien dans l'exemple et bouton en haut de la fiche.
- 29/10/2026 : fiches CV-02 et CO-02, onglet Cou renommé ORL, fiches OS-04 à OS-07, NE-04, DI-03, DI-04, 11 calculateurs, mode sombre, consultation hors ligne.
