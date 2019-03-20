Phase 3 du Sokoban : 
Binome PERRIN Baptiste - SCHNEIDER Leo


Extensions implementes :

Nous avons choisi d'implementer comme première extension un editeur de niveau graphique permettant de créer et enregistrer ses propres cartes, puis dans un second temps un menu permettant de choisir entre jouer, avec un second menu de selection des niveaux, ou utiliser l'editeur.


Organisation du programme :

Notre programme a garde une structure tres similaire a celle des phases precedentes, mais se distingue avec un bien plus grand nombre de fonctions auxiliaires, et l'ajout du menu, de la selection de niveau et d'un editeur graphique, toujours en gardant une structure ou chaque partie du jeu est decomposee en trois parties : une pour l'affichage, une pour la gestion des donnees et une pour la gestion des interactions.


Choix techniques :

Notre principal choix technique durant cette phase a ete de nous faciliter l'ecriture du programme en gardant une structure similaire a celle du programme en phase 1 (cf organisation du programme). De plus, nous avons choisi une fois de plus de garder la boucle principale controlant le jeu aussi allegee que possible en fractionnant notre code en de nombreuses fonctions, avec un grand nombre apparaissant uniquement dans d'autres fonctions. Enfin, nous avons reutilise autant que possible certaines fonctions auxiliaires, ou si cela etait impossible les reecrire en changeant quelques donnees a peine pour s'en reservir, une fois de plus, des que possible. Cela encore dans des fins de faciliter l'ecriture du programme.


Problemes rencontres :

Nous n'avons pas vraiment rencontres de réel probleme, si ce n'est une variable nommee de la meme maniere qu'une une fonction integree a Python, et qui a pose un tres court probleme. Nous avons egalement du modifier certaines fonctions gerant la carte datant de la precedente phase afin de les faire fonctionner non plus avec un argument precise dans une ligne de commande mais avec une selection issue du menu.


Source des sprites et images utilises, ainsi que de certaines cartes :

OpenGameArt.org -
https://opengameart.org/content/sokoban-pack
(credits a 1001.com)
https://opengameart.org/content/platformer-tiles
(credits a Kenney Vleugels, www.kenney.nl)

Sourcecode -
http://www.sourcecode.se/sokoban/levels
(cartes de David Holland, "The Bagatelle collection")
