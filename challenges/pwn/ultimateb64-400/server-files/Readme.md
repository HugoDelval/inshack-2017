# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/ultimateb64 .
```

# Run
```bash
apt-get install docker.io
touch /usr/local/bin/ultimateb64shell
chmod +x /usr/local/bin/ultimateb64shell
echo '/usr/local/bin/ultimateb64shell' >> /etc/shells
useradd ultimateb64 -s /usr/local/bin/ultimateb64shell -G docker -d /tmp
passwd ultimateb64 # ultimateb64

echo '#!/bin/sh' > /usr/local/bin/ultimateb64shell
echo "docker run -it --rm --cpu-period=100000 --cpu-quota=10000 --ulimit nproc=100:100 --ulimit fsize=5000:5000 --ulimit data=50000:50000 registry.insecurity-insa.fr/insecurity/ultimateb64" >> /usr/local/bin/ultimateb64shell
```
