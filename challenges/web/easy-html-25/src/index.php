<?php

$username="admin";
$password="INSA{ThatWasATrainingOneDontWorry}";

if ($_POST["username"]!="" && $_POST["password"]!=""){
    if ($_POST["username"]==$username && $_POST["password"]==$password)
    {
      header('Location: success.html');
	  exit();
    } else {
      print("<h3>Error : no such user/password</h2><br />");

    }
}
?> 


<html >
  <head>
    <meta charset="UTF-8">
    <title>Log-in</title>

    <link rel='stylesheet prefetch' href='http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/themes/smoothness/jquery-ui.css'>

        <link rel="stylesheet" href="css/style.css">
  </head>

  <body>

    <div class="login-card">
    <h1>Log-in</h1><br>

	<form action="" method="post">
	  Login&nbsp;<br/>
	  <input type="text" name="username" placeholder="Username"/><br/><br/>
	  Password&nbsp;<br/>
	  <input type="password" name="password" placeholder="Password"/><br/><br/>
	  <br/><br/>
	  <input type="submit" name="login" class="login login-submit" value="connect" /><br/><br/>
	</form>
	    
  <div class="login-help">
    <a href="#">Register</a> • <a href="#">Forgot Password</a>
  </div>
</div>

<form action="#send_to_admin">
    <input type="hidden" value='TODO: change main password of "Admin" from "INSA{ThatWasATrainingOneDontWorry}" to "123456"' >
</form>
    <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
<script src='http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js'></script>

      </body>
      </html>

