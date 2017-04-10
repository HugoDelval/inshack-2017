# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/coffee .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name coffee \
           -p 2052:8080 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           --ulimit fsize=10000:10000 \
           --ulimit data=1000000:1000000 \
           registry.insecurity-insa.fr/insecurity/coffee
docker stop coffee && docker rm -v coffee
docker exec -u 0 -it coffee bash
```
