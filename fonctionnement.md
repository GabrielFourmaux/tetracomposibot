### 1. "Diviser pour Régner"

Plutôt que d'avoir 4 robots identiques, on va créer des spécialistes.

*   **Robot 0 (Le Maçon Gaucher) :** *Wall-Follower Left*. Il longe les murs par la gauche. Il garantit de peindre tout le contour extérieur et les obstacles internes dans le sens anti-horaire.
*   **Robot 1 (Le Maçon Droitier) :** *Wall-Follower Right*. Il longe les murs par la droite (sens horaire). Il coupe la route aux adversaires qui tenteraient de faire le tour.
*   **Robot 2 (Le Mutant) :** *Genetic Bot*. C'est celui exigé par le sujet. Il utilise des poids calculés par un algorithme génétique pour maximiser la couverture de surface en milieu ouvert (là où les suiveurs de murs ne vont pas).
*   **Robot 3 (Le Débloqueur / Chaos) :** *Subsumption Explorer*. Un robot utilisant une architecture de subsomption (comportement par priorités) avec utilisation intelligente de la mémoire pour se débloquer s'il est coincé (ce qui arrive souvent dans les coins).

### 2. Étape 1 : L'Entraînement Génétique (Pré-requis)

Avant de coder le fichier final, on doit obtenir les poids du Robot 2. Pour cela, on va créer un script d'entraînement temporaire : `robot_genetic_trainer.py`

L'idée est d'entraîner le robot seul sur la première arène, sur une quantité absurde de répétitions jusqu'à convergence (et à ce moment là j'interromps moi-même le processus), puis de noter les meilleurs poids et reprendre l'entraînement à partir de ceux-ci sur l'arène suivante, et ainsi de suite. On obtient donc des poids qui ont été entraînés sur chaque type d'arène. 

Par exemple, à la fin de l'entraînement sur la première arène, on obtient :

```text
Gen 3054 | NEW BEST: 242.4
POIDS A COPIER = [0.38373421902436117, 1.0, 1.0, -0.7086317889735636, -0.7845668325370423, -0.6670387411540175, 0.462602556394181, 0.9098338505518675, 0.2004646664156112, -0.5716636905164719, 0.2902846481585632, -0.6196725855908973, -0.13951852004176057, 0.2534460861493339, -0.4367475996747681, 0.36775647568135444]
Gen 4963 | NEW BEST: 242.5
POIDS A COPIER = [0.38373421902436117, 1.0, 1.0, -0.7086317889735636, -0.7845668325370423, -0.6670387411540175, 0.462602556394181, 0.9098338505518675, 0.2004646664156112, -0.5716636905164719, 0.2902846481585632, -0.6196725855908973, -0.13951852004176057, 0.2534460861493339, -0.4367167564550657, 0.36775647568135444]
### iteration 2000000 / 5000000 ###
### iteration 3000000 / 5000000 ###
### iteration 4000000 / 5000000 ###
Gen 11742 | NEW BEST: 242.5
POIDS A COPIER = [0.3837567308388483, 1.0, 1.0, -0.7086317889735636, -0.7845668325370423, -0.6670387411540175, 0.462602556394181, 0.9098338505518675, 0.2004646664156112, -0.5716636905164719, 0.2902846481585632, -0.6196725855908973, -0.13951852004176057, 0.2534460861493339, -0.4367167564550657, 0.36775647568135444]
[STOP]  2026-02-12 12:46:12 GMT
```

On reprend donc avec les dernières valeurs.

V2 : après avoir essayé cette méthode, on se rend compte que le robot finit par converger vers un déplacement circulaire car il a compris que c'était une bonne manière d'éviter le malus des murs. On change donc la punition pour la rendre plus sévère sur la rotation et pour récompenser la "vue dégagée" (rien devant lui)

V3 : La stratégie de départ ne fonctionne pas pour battre professor x, donc on va passer à une nouvelle stratégie :
    
    Robot 0 (Follower - Gauche) : Un Wall Follower amélioré qui colle au mur de gauche de manière agressive. Il est vital pour les arènes 2, 3 et 4.

    Robot 1 (Follower - Droite) : Idem, mais à droite.

    Robot 2 (Le Pilote de F1 - Génétique) : On va le ré-entraîner spécifiquement pour ne pas avoir peur des murs. Il doit foncer dans les couloirs.

    Robot 3 (Le Rebondisseur - Bouncer) : On remplace l'architecture complexe par une géométrie simple. S'il tape un mur, il rebondit selon un angle fixe. C'est redoutable dans les petits espaces où l'IA réfléchit trop.

    Pour le train : on va se focaliser sur les arènes fermées, et on va faire une technique de brute force : 
    Si au bout de 100 pas, le score est négatif, on considère que le génome est "né-mort". On le tue immédiatement, on réinitialise tout, et on génère un nouveau cerveau aléatoire sans même attendre la fin de la génération.
    On va aussi en lancer plusieurs à la fois pour chercher à maximiser les résultats. 