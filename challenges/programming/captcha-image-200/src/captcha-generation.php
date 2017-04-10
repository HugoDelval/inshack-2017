<?php
session_start();

function random_str($length){
    $alphabet = 'abcdefghijklmnopqrstuvwxyz012345679';
    $size = strlen($alphabet);
    $str = '';
    for ($i = 0; $i < $length; $i++) {
    		$rand = mt_rand(0, $size-1);
    		$str .= $alphabet[$rand];
    }
    return $str;
}

function image($mot){

    $size = 35;
    $marge = 15;

    #Police pour dessiner le texte
    $font = './font.ttf';

    #On dessine une boite de taille fixe (pour eviter le guessing par rapport a la taille)
    $largeur = 410;
    $hauteur = 60;

    #Volontairement grand pour ne pas rendre trop dur le challenge non plus
    $largeur_lettre = 40;

    #Image initiale
    $img = imagecreate($largeur+$marge, $hauteur+$marge);

    #Differentes couleurs qui vont etre utilisees
    $blanc = imagecolorallocate($img, 255, 255, 255);
    $noir = imagecolorallocate($img, 0, 0, 0);
    $red = imagecolorallocate($img, 100, 0, 0);
    $blue = imagecolorallocate($img, 0, 0, 100);
    $green = imagecolorallocate($img, 0, 100, 0);
    $purple = imagecolorallocate($img, 100, 0, 100);
    $yellow = imagecolorallocate($img, 100, 100, 0);

    #Rotation des couleurs
    $colors = [$red,$blue,$green,$purple,$yellow];

    #On remplis avec 50 rectangles de tailles aleatoires en fond afin de complexifier le captcha
    $nbrect = 50;
    for($i = 0; $i < $nbrect;++$i){

      #Position initiale
      $pX = mt_rand(0,$largeur-20);
      $pY = mt_rand(0,$hauteur-10);

      #Taille
      $sX = mt_rand(10,40);
      $sY = mt_rand(10,40);

      #Couleur aleatoire qui seront des nuances de gris
      $randcolor = mt_rand(0,150);
      $color = imagecolorallocate($img, $randcolor, $randcolor, $randcolor);

      imagerectangle ( $img , $pX , $pY , $pX+$sX , $pY+$sY , $color );
    }

    #On ecrit lettre par lettre le mot du captcha
    for($i = 0; $i < strlen($mot);++$i){
        $l = $mot[$i];

        #On effectue un padding de hauteur une lettre sur deux pour plus de challenge
        $pad = 20*($i%2==0);
        $color = $colors[$i%5];

        #On ajoute un angle pour plus de complexite, attention a ne pas trop en mettre car les ocr classiques ont du mal avec ça
        $angle = mt_rand(-2,2);

        imagettftext($img,mt_rand($size-7,$size),$angle,($i*$largeur_lettre)+$marge, $hauteur-$pad,$color, $font, $l);
    }

    ob_start();
    $im = imagepng($img);
    $stringdata = ob_get_contents();
    ob_end_clean();
    return base64_encode($stringdata);
}

for ($i=0; $i < 20000 ; $i++) {
  $mot = random_str(10);
  file_put_contents("captchas/".$i , $mot.":".image($mot) );
}
?>
