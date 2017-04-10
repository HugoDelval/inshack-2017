`vuln` has setgid bit. If we could find a way to change the flow of vuln, we can do it with owner group's rights.

The `ls` call by `system()` is ambiguous. `System()` don't know where `ls` is located and will look into `$PATH` for paths where to find `ls`binary.
We just have to make our `ls` binary wich open a shell, and to add our `ls` path to `$PATH`.
