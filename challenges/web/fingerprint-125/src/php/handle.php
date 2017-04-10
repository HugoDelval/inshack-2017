<?php
if(!isset($_POST['str'])||$_POST['str']!=175949){
  echo "You are not me !Learn to follow simple instructions";
  die();
}
if (!isset($_SERVER['HTTP_USER_AGENT']) || $_SERVER['HTTP_USER_AGENT']!="xXxGetSecretInfoxXx") {
    echo "You are not me !You did not hack Google";
    die();
}
if(!isset($_POST['h'])||$_POST['h']!=4578){
  echo "You are not me !My screen is far better...";
  die();
}
if(!isset($_POST['w'])||$_POST['w']!=8000){
  echo "You are not me !My screen...";
  die();
}
if (isset($_POST['f'])) {
    $boolFont=false;
    foreach ($_POST['f'] as $value) {

        if (strpos($value, 'Original by fnkfrsh') !== false) {
            $boolFont=true;
        }
    }
    if(!$boolFont){
      echo "You are not me!My font...";
      die();
    }
}

if(!isset($_POST['offset'])||$_POST['offset']!=-600){
  echo "You are not me !It's not the good time";
  die();
}


if (isset($_SERVER['HTTP_ACCEPT_LANGUAGE'])) {
    $LangueNav = explode(',', $_SERVER['HTTP_ACCEPT_LANGUAGE']);
    $boolLangue=false;
    foreach ($LangueNav as $value) {
        if (strpos($value, 'co') !== false) {
            $boolLangue=true;
        }
    }
    if(!$boolLangue){
      echo "You are not me !I will bomb you and eat saucisson";
      die();
    }
}
if (isset($_POST['d'])) {
    $boolFake=true;
    foreach ($_POST['d'] as $value) {

        if ($value==""||strpos(strtolower($value), 'fake') === false) {
            $boolFake=false;
        }
    }
    if(!$boolFake){
      echo "You are not me!Learn to hide devices";
      die();
    }
}

if(isset($_POST['ip'])){
  $boolIp=false;
  if (strpos($_POST['ip'], '13') !== false) {
      $boolIp=true;
  }
  if(!$boolIp){
    echo "You are not me !Be careful about your ip";
    die();
  }
}


echo "INSA{Tr4ck1ng_1s_E4sY}";
