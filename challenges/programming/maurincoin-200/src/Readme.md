# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/maurincoin .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name maurincoin \
           -p 2052:5000 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           --ulimit fsize=10000:10000 \
           --ulimit data=1000000:1000000 \
           registry.insecurity-insa.fr/insecurity/maurincoin
docker stop maurincoin && docker rm -v maurincoin
docker exec -u 0 -it maurincoin bash
```
