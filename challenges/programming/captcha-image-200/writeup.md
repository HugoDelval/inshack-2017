On peut remarquer que lors de l'inscription le site bloque le CAPTCHA, 
et nous dit que l'on est un humain.

On peut alors supposer que l'on répond trop lentement au CAPTCHA (peut-être donner des indices en + )

Il suffit donc de récupérer l'image sur le site, de la décoder (B64), d'enlever le bruit et de réaliser un traitement pour 
enlever le bruit et de faire une reconnaissance de caractères (gocr par exemple).

On obtiens alors une bonne piste pour réussir mais peu de chance d'y arriver, car les lettres sont décalées les unes par rapport aux autres. 
mais on peut les augmenter en repérant les charactères et en les décalant pour les mettre toutes sur la même ligne,
ou en remarquant que les couleurs sont toujours constantes avec la position des charactères et faire un OCR par
couleur afin d'avoir une meilleure probabilité. 


