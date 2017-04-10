# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/xoring .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name xoring \
           -p 2052:8081 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           --ulimit fsize=10000:10000 \
           --ulimit data=1000000:1000000 \
           registry.insecurity-insa.fr/insecurity/xoring
docker stop xoring && docker rm -v xoring
docker exec -u 0 -it xoring bash
```
