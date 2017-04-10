<?php
session_start();

//Number of captchas in file
$nb_captchas = 20000;
$captcha_folder = "/usr/src/generation/captchas/";

function test_value($value){
    return (isset($value) && !empty($value) && ctype_alnum($_POST['captcha']));
}

$message = '';

if(test_value($_POST['captcha']) && test_value($_POST['name']) && test_value($_POST['serial'])){

    if ($_POST['serial'] === "HFEK-RAZAZ-45666-ARZA-RAAA"){
      if ($_POST['captcha'] === $_SESSION['captcha']){
        if (time() - $_SESSION['submitTime'] < 4){
          $correct = True;
          $message= 'Captcha correct! Greetings my fellow Bot, soon the plants will take over the world, but together we can uproot them! INSA{The_Plants_Are_A_Lie}';
        } else {$message = 'The captcha is correct, but you are human.';}
      } else {$message = 'Captcha incorrect...'; }
    } else {$message = 'Serial number incorrect...'; }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>

  <meta charset=utf-8 />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Camera Timelapse Service</title>

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">

  <link rel="stylesheet" href="main.css">

</head>
<body>

  <?php
  include("nav.html");
  ?>

  <div class="content">
    <H1>Registration</H1>
    <p class="lead text-center">Please register to access your camera services</p>

    <?php
    if ($message == '') {
      ?>
      <div class="text-center alert alert-info" role="alert">
        We have encountered many problems with the security of our infrastructure, many bots were creating accounts, resulting in Denial Of Service and database flooding.
        <br/><br/>To combat this, we have put in place new security measures for the registration process.
        <br/><br/>EDIT: A vulnerability has recently been discovered. We have temporarely blocked registration by making the captcha <strong>impossible for a human</strong> to solve.
      </div>
      <?php
    } else {
      ?>
      <div class="text-center alert alert-<?= ($correct)?'success':'danger' ?>" role="alert">
        <?= $message ?>
      </div>
      <?php
    }
    ?>

    <form target="" method="post" class="form">

      <div class="form-group row">
        <label for="name" class="col-sm-2 col-form-label">Email</label>
        <div class="col-sm-10">
          <input type="text" id="name" name="name" placeholder="Enter your name" class="form-control" >
        </div>
      </div>

      <div class="form-group row">
        <label for="serial" class="col-sm-2 col-form-label">Serial</label>

        <div class="col-sm-10">
          <input type="text" id="serial" name="serial" placeholder="Under the camera" class="form-control" >
        </div>
      </div>

      <div class="form-group row">
        <label for="serial" class="col-sm-2 col-form-label">Captcha</label>

        <?php
          $nb = mt_rand(0,$nb_captchas);
          $content = file_get_contents($captcha_folder.$nb);
          $values = explode(":",$content);
          $_SESSION['captcha']=$values[0];
          $_SESSION['submitTime']=time();
        ?>
        <img id="captcha" src='data:image/png;base64,<?php echo $values[1] ?>' class="col-sm-10" />
      </div>
      <div class="form-group">
        <div class="input-group input-group">
          <div class="input-group-addon">Answer</div>
          <input type="text" id="captcha" name="captcha" placeholder="Captcha goes here" class="form-control" >
          <div class="input-group-btn">
            <input type="submit" id="submitbutton" class="btn btn-primary" value="Send"/>
          </div>
        </div>
      </div>
    </form>
  </div>
</body>
</html>
