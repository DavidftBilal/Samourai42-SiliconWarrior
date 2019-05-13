# Samurai42 Silicon Warrior

Auteurs: 
- Amadou Bilal 17060
- Sanchez Arguello David 17098

Pour simplifier l'encodage des coups, nous avons transformé la liste body['game'] en matrice 5x5 grâce au module Numpy.
Une simple transposée de cette matrice permet de naviguer entre les colonnes plutôt qu'entre les lignes.

Le programme commence par choisir un coup aléatoire par défaut et donc par securité, ce qui se fait grâce à la fonction choice du module random.

Les 3 premiers coups sont pré-enregistrés, le but étant de prendre 2 à 3 coins, ce qui nous a semblé nous donner un avantage non négligeable.

Notre algorithme est par défaut offensif, il ne réagit aux coups de l'adversaire que si celui-ci aligne 4 pions.

Il commence par vérifier qu'il n'y ait pas de victoire immédiate ; par la diagonale principale, puis la secondaire, puis par les lignes et enfin par les colonnes.

Il vérifie ensuite qu'il n' y ait pas de risque de défaite due à 4 pions déjà placés que se soit par les diagonales ou par les lignes et colonnes.

Si aucune victoire ni défaite au prochain coup n'est annoncée, il compte le nombre de pions par ligne et par colonne afin de choisir le moyen le plus court de gagner; en identifiant les lignes et colonnes les plus favorables.

Pour finir il fait tout pour compléter la ligne ou colonne la plus prometteuse.
