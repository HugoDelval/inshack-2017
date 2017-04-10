Challenge in 3 steps:

- First step is a classic sql injection on the insertion of a dishwasher. The parameter which is vulnerable is the cookie "user". You can insert any entry in the database
- Second step is to understand that the application uses *yaml.load() / yaml.dump()* as a (de)serialization method. This is insecure and if a user can control the data that is deserialized, it can lead to a RCE. Using the first vulnerability we can insert an object that will be evaluated.
- Third step, you now have a shell on the machine and see a file: *my.cnf*, but there is no interesting data in it. But now you know that the flag is the password of the user *flag*. You do a `ps aux` and see that the user is currently connected to mysql and set its password in the commandline -> FLAAG

Note: cf *exploit/exploit.py* for full exploit
