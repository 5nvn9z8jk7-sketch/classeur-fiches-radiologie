# Classeur de fiches d'aide à la lecture en radiologie

Public : radiologues et internes. Langue : français. Classement par organe ; chaque fiche regroupe les modalités utiles.

## Contenu (version du 29 octobre 2026)
- 33 fiches (88 pages), 12 onglets : Transversal, Neuro, Cou, Sein, Thorax, Cœur · vaisseaux, Foie, Pancréas, Tube digestif, Rein · surrénale, Pelvis, Ostéo-articulaire
- `Classeur-fiches-radiologie.pdf` : classeur complet (couverture, sommaire, registre des versions, intercalaires, signets)
- `Fiches-radiologie-par-organe/` (+ `.zip`) : une fiche PDF par fichier, rangées par organe

## Structure des sources
- `src/fiches.json` : métadonnées de chaque fiche (code, organe, couleur, titre, référence, sources avec URL, nombre de pages attendu)
- `src/fiches/<CODE>.html` : contenu de chaque fiche (`{{HEAD2}}` = saut de page avec en-tête « suite »)
- `src/FO-01.html` : fiche LI-RADS CT/IRM (document autonome, d'origine)
- `src/base.css` + polices Inter statiques : style commun
- `src/build.py [CODES…]` : génère les PDF des fiches dans `pdf/`
- `src/gen/perfusion.py` : schémas de la fiche NE-04 (`ne04.svg`)
- `src/gen/ortho.py` : schémas des fiches de mesures orthopédiques OS-04 à OS-07 (`os04.svg`…`os07.svg`), liens dans `src/gen/atlas.py`
- `src/binder.py` : assemble le classeur, le registre des versions (dictionnaire `veille`) et les dossiers par organe

## Procédure de mise à jour
1. Vérifier la recommandation en vigueur (source primaire de préférence)
2. Modifier `src/fiches/<CODE>.html` et, si besoin, `fiches.json` (référence, sources)
3. Mettre à jour l'entrée `veille` dans `binder.py` (référence, point à surveiller)
4. `python3 build.py <CODE>` puis `python3 binder.py`, puis zipper le dossier par organe
5. Contrôler visuellement chaque page modifiée (débordements, coupures)

## À surveiller
- PI-RADS : nouvelle version (« PI-RADS Pathway ») annoncée pour 2026
- O-RADS : nouvelle version attendue
- ESC embolie pulmonaire : mise à jour attendue (AHA/ACC 2026 déjà intégrée)
- AVC AHA/ASA 2026 : version actualisée signalée en mars 2026 à vérifier
- ESGAR rectum 2026 partie II (réévaluation) : fiche à ajouter
- I-TIRADS (international) : en cours d'élaboration

## Pistes d'extension
Kyste et masse rénale solide, VI-RADS (vessie), NI-RADS (cou traité), urgences abdominales (appendicite, occlusion), pédiatrie, cardio IRM, imagerie de l'hémorragie méningée, CT colonoscopie (C-RADS), réévaluation du rectum.

## Version web
- Source : `web/` (build_web.py, site.css, app.js, outils_body.html). Génère `site/` à partir des fiches construites par `src/build.py` et du classeur produit par `src/binder.py`.
- Reconstruire : `python3 src/build.py && python3 src/binder.py && python3 web/build_web.py`, puis redéployer le dossier `site/` (application « Classeur de fiches radiologie », asset 5e20da0b-6e2f-4b04-9073-b65564e50013).
- Calculateurs : ASPECTS (schéma cliquable `src/gen/aspects_i.svg`), LI-RADS CT/IRM v2018, ACR TI-RADS, Bone-RADS.
- Atlas visuel : chaque fiche reçoit automatiquement une page « Atlas visuel » (schéma + liens + QR codes) à partir de `src/gen/atlas.py` ; FO-01 = FO-01-base.pdf + FO-01X.pdf.

## Mise à jour du 29/10/2026
- Nouvelles fiches DI-03 (appendicite aiguë, WSES Jerusalem 2025) et DI-04 (occlusion du grêle sur bride, WSES Bologne 2017) ; classeur à 28 fiches, 76 pages.
- Site : 11 calculateurs avec phrase de compte rendu à copier (ASPECTS, PC-ASPECTS, EU-TIRADS, ACR TI-RADS, Fleischner, Lung-RADS, CAD-RADS 2.0, LI-RADS, Bosniak, PI-RADS, Bone-RADS), renvois entre fiches cliquables, mode sombre (suit l'appareil, bouton de bascule), consultation hors ligne via service worker (`web/sw_template.js`), mise en page aérée.
- L'hébergement de l'aperçu interdit localStorage : pas de favoris persistants ; le thème choisi se propage par le paramètre `?theme=`.

## Publication
- Site publié le 29/10/2026 : https://fiches-radiologie.pplx.app (site_id 9aa9f302-0c63-4951-82c0-8684464c2849, visibilité publique).
- Pour mettre à jour : reconstruire, `deploy_website` sur `site/`, puis republier avec le même site_id (après accord de l'utilisateur).
- Sauvegarde GitHub (demande de l'utilisateur, à faire à CHAQUE modification, sans redemander) : dépôt privé https://github.com/5nvn9z8jk7-sketch/classeur-fiches-radiologie. Remplacer son dossier `site/` par le site reconstruit, commit avec un message en français, push sur `main`.
- Installable comme application (manifest + icônes PNG + service worker) ; consultation hors ligne vérifiée.

## Ajout du 29 octobre 2026 · mesures orthopédiques
OS-04 télérachis (Cobb, Risser, PI/SS/PT, SVA, SRS-Schwab, Meyerding), OS-05 coxométrie (VCE, HTE, VCA, CC'D, alpha, Graf), OS-06 pangonogramme et fémoro-patellaire (HKA, MAD, mLDFA, MPTA, TA-GT, Caton-Deschamps, Dejour, torsions de Lerat), OS-07 pied et membre supérieur (Djian, Méary, hallux valgus, Böhler, poignet, CSA, coude). Sommaire resserré pour tenir sur une page.

## Ajout du 29 octobre 2026 · perfusion
NE-04 scanner de perfusion dans l'AVC aigu sur Philips IntelliSpace Portal : acquisition, cartes, pas à pas ISP, summary map (rouge rMTT > 150 % et CBV < 2 mL/100 g, vert), conversion au ratio des essais, critères EXTEND/DEFUSE 3/DAWN, recommandations AHA/ASA 2026 et ESO, pièges. Sommaire resserré (33 fiches).

## Mise à jour du 30/10/2026
- CV-02 : nouvelle page `f/CV-02-cr.html` (compte rendu type du score calcique à remplir, sans technique, bouton « Copier pour Word »), liée depuis l'exemple de compte rendu de la fiche. Copie dans `web/extra/f/`.
- Attention : les sources de CV-02 et CO-02 ne sont pas dans `src/` ; le site de référence est la sauvegarde GitHub (`site/`). Modifier ce dossier directement tant que les sources ne sont pas restaurées.
