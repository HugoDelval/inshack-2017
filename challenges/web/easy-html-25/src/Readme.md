# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/easyhtml .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name easyhtml \
           -p 2053:8081 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           --ulimit fsize=10000:10000 \
           --ulimit data=1000000:1000000 \
           registry.insecurity-insa.fr/insecurity/easyhtml
docker stop easyhtml && docker rm -v easyhtml
docker exec -u 0 -it easyhtml bash
```
