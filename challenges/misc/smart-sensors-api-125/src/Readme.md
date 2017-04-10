# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/smartsensors .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name smartsensors \
           -p 2052:5000 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           --ulimit fsize=10000:10000 \
           --ulimit data=1000000:1000000 \
           registry.insecurity-insa.fr/insecurity/smartsensors
docker stop smartsensors && docker rm -v smartsensors
docker exec -u 0 -it smartsensors bash
```
