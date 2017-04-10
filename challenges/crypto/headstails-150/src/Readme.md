# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/headstails .
```

# Run

```bash
apt-get install docker.io
touch /usr/local/bin/headstailsshell
chmod +x /usr/local/bin/headstailsshell
echo '/usr/local/bin/headstailsshell' >> /etc/shells
useradd headstails -s /usr/local/bin/headstailsshell -G docker -d /tmp
passwd headstails # headstails

echo '#!/bin/sh' > /usr/local/bin/headstailsshell
echo "docker run -it --rm --cpu-period=100000 --cpu-quota=10000 --ulimit nproc=100:100 --ulimit fsize=5000:5000 --ulimit data=50000:50000 registry.insecurity-insa.fr/insecurity/headstails" >> /usr/local/bin/headstailsshell
```
