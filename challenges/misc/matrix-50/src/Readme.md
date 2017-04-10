# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/matrix .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name matrix \
           -p 2052:12345 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           registry.insecurity-insa.fr/insecurity/matrix
docker stop matrix && docker rm -v matrix
docker exec -u 0 -it matrix bash
```
