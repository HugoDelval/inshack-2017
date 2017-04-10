# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/lost-file .
```

# Run
```bash
apt-get install docker.io
touch /usr/local/bin/lost-file-shell
chmod +x /usr/local/bin/lost-file-shell
echo '/usr/local/bin/lost-file-shell' >> /etc/shells
useradd lost-file -s /usr/local/bin/lost-file-shell -G docker -d /tmp
passwd lost-file # lost-file

echo '#!/bin/sh' > /usr/local/bin/lost-file-shell
echo "docker run -it --rm --security-opt seccomp=unconfined --ulimit nproc=100:100 --cap-add=SYS_PTRACE registry.insecurity-insa.fr/insecurity/lost-file" >> /usr/local/bin/lost-file-shell
```

