# HumanSI
Un nom complétement original créer et pensé par un groupe fanatique pas très intelligent qui me ne manque pas d'égo 

HumanSI (contraction de Human et NSI ou SImulation c'est comme vous voulez) est un projet de simulation de 
civilisation. Au début de chaque simulation vous vous retrouverez sur une carte générer aleatoirement,
a vous d'y créer la vie, construiser des hotel de ville pour etablir des civilisations, ou faite apparaitre
simplement quelques habitans lambda. Voyer comment les civilisations vont réagir en se rencontrant,
vont elle s'entretuer ou s'ignorer mutuellement. Choisisez un favoris et aider le pour ça 
conquete du monde avec les outils proposé.

________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

# Info Utiles
n'oubliez pas d'installer les modules requis :
    - pip install pyglet
    - pip install Pillow
    - pip install perlin_noise

Pour commencer une partie allez dans le script main.py et executer le.
Pour changer des parametres allez dans le script Settigns.py
(des presets de parametre sont trouvable dans la documentation pour les meilleurs perfomances)

le liens du site : https://humansiweb.vercel.app/

________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

# Comment ajoutez de nouvelles civilisations ?
<!> la configuation des presets est expliquer apres <!>

Si vous voulez ajouter (ou modifier) des civilisations commencez par :
 - Aller dans le fichier Civilisation.csv (Assets/Presets/Civilisation.cvs)
puis modifier les parametres que vous souhaitez (chaque nouvelle ligne est une autre civilisation)

 - Pour ajouter les maisons / habitant de votre nouvelle civilisation, allez dans Preset.csv 
 (Assets/Presets/Presets.csv) et créez de nouvelle ligne pour vos unités, une civilisation a besoin
 d'un chef, d'un habitant, d'une maison, d'un hotel de ville et optionellement d'une merveille
 <!> l'hotel de ville est l'objet servant a faire apparaitre une civilisation, pour dire
 que votre hotel de ville en ai bien un ajouter "CityHall" a la fin du nom de l'hotel de ville <!>

pour ajouter les sprites qui composeront votre civilisation créez un nouveau dossier dans 
Assets/Graphics/Civilisation/le-nom-de-votre-civilisation
<!> Il faut que le nom du dossier soit le même que celui dans les presets <!>
dans le dossier créé ajouter en un dossier pour chaque objet convernant votre civilisation
(n'oublier pas de mettre le chemin d'acces dans les presets)

________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

# Plus d'information sur les Presets :

Preset.csv : 
name - le nom de l'unité
speed - la vittesse de déplacement de l'unité
moveTimer - tout les x seconde l'unité ce déplacera 
sociability - plus cette valuer est grande plus l'unité sera gentil et pacifique
damage - les dégats de l'unité par frame
attackSpeed - <!> cette option n'est plus utiliser <!>
health - la vie de l'unité
lifeSpan - au bout de combien de seconde l'unité mourrera de veillesse
civilisation - la civilisation auquel l'unité appartient
category - la categorie auquel l'unit appartient (tools, ressources, buildings, etc...)
unitCost - combien de ressources sont necessaire pour faire apparatre l'unité
spritesPath - le chemin d'acces au dossier contenant les sprites de l'unité
isSpawnable - est ce que l'utilisiteur peut faire apparaitre manuellement l'unité
    <!> si il y a plusieurs iamge dans le dossier, alors l'une d'entre elle sera choisi aléatoirement <!>
updateWeight - tous les combiens la fonction update vas run (0.2 pour les population, 1 pour les l'hotel de ville)
    <!> si la valeur est égale a -1 l'update ne se lancera jamais, a utilisé pour les batiments except l'HDV <!>
animationDuration - la duré entre chaque frame d'animations (une frame = une image du dossier de l'unité)
    <!> si la valeur est égale a -1 l'animation ne se lancera jamais <!>

Civilisation.csv :
name - le nom de la civilisation 
cityHallName - le nom du preset de l'hotel de ville (ex : yellow -> YellowCityHall)
religion - le nom de la religion de la civilisation (influe sur les calcules pour les guerres)
    <!> si la religion est "none" alors la civilisation n'aura pas de religion <!>
aggressivity - l'aggresivité de la civilisation
maxBasePop - le nombre maximal d'habitant que la civilisation peut faire stocker a son apparition
    <!> cette valuer augmentera au fil du temps avec l'aparrition de maisons <!>
maxPopIncrease - de combien la valeur maxBasePop augmentera avec la construction de maison
popName - le nom du preset des habitants de la civilisation
houseName - le nom du preset des maisons de la civilisation
wonderName - le nom du preset de la merveille de la civilisation
    <!> optionel <!>
updateWeight - tout les x seconde la fonction update vas run (1 est la meilleur valeur)
    <!> si la valeur est égale a -1 l'update ne se lancera jamais <!>
chiefName - le nom du preset du chef de la civilisation
    <!> le chef réapparait après un certain temps après ça mort <!>
wonderRessourcesIncomes - le bonus de ressources attribuer a chaque update par la merveille
    <!> si la civilisation n'a pas de preset de merveille ça ne sert a rien <!>
desiredHeight - la hauteur préférer de la civilisation : sert a déterminer si la civilisation est avantagé ou non
    <!> la valeur doit être comprise en 0 et 1 <!>

________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
wtf je savais pas que des gens lisais ça. Si t'as vraiment tout alors gg t'es le meilleurs.
༼ つ ◕_◕ ༽つ
