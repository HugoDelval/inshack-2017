# Solution

When accessing the website (https://captcha.insecurity-insa.fr) you get an audio file and you have to type what you ear before submitting.
You will eventually be too long, as the time limit is 5seconds.

You can notice the /debug link in the source code, that bring a password protected zip.
With bruteforce and John you find the password and all the audio files included in the file.

You just have to sample the captcha into this files in order to get the correct result.
Use a 44 bytes(classic)header.
