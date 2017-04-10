# Bugbounties writeup

We had 2 majors vulnerabilities during the CTF and 1 small one. Let's start with the major ones then the small one.

## Dirty cow

Yes we were vulnerable to dirty cow! How lame isn't it? We built the VMs for the 3 "easy" pwn a long time ago and just before starting the CTF we did an `upgrade` silly us we forgot the `dist-upgrade` ! Thanks to @jbz for reporting it. I think they tried a 64bits exploit because they only managed to DoS the machines, but we know that it could lead to root so it was considered a big vuln.

## docker run --privileged

We were using docker for some challenges. For **lost file** we created a docker for each login over ssh. Sadly the exploit we built did not work with the default docker capabilities and we did not found which caps to add soon enough (we did this chall the day before the competition..). As a quick fix we launched docker with ```--privileged``` and dropped some cappabilities. But we did not know that this option mounted the whole root file system in read/write access into docker. So it was possible to totally root the host! Thanks to @OpenToAll and @synssirene for reporting this.

## CSRF in the scoreboard

In the website you had the possibility to add a GIF to your profile, there was a CSRF on the ```/user/logout``` endpoint using a HTTP 302 redirection to bypass filters (you were not able to add a gif we ```insecurity-insa``` in it). Nice bypass, thanks @Hexpresso.

## Conclusion

It was nice to add a bugbounty challenge to the CTF, that way we learned stuff too :D
