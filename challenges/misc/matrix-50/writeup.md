# Writeup QRcode

## Français
Quand on se connecte sur le port de l'application, on voit apparaitre une suite de carré blanc et noir. Avec le nom du challenge et en s'aidant d'internet on trouve que c'est un code barre de type Data Matrix!

En regardant plus en détail comment ce code barre est construit, on s'aperçoit qu'il faut une ligne noir complète à gauche et en bas.
En ajustant la taille du terminal, il y a une position qui nous permet de voir apparaitre le barcode. Une fois correctement affiché, on peut le decoder soit en utilisant une application smartphone ou bien en prennant une capture d'écran et en le décodant en ligne (https://online-barcode-reader.inliteresearch.com/ ==> fonctionne relativemement bien). 
Une fois décodé, on la le flag.

## English
When you connect to the service, you have many white and black square. With the name matrix, we find it's a Data Matrix barcode!

This barcode need the first column with only black square and the last line with only black square. To get the right picture you adjust the size of your terminal.
Once you have it, you can decode it with your smartphone or on some website like https://online-barcode-reader.inliteresearch.com.

And you have the flag!
