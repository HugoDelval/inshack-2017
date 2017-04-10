# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/dga .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name dga \
           -p 2052:8060 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           registry.insecurity-insa.fr/insecurity/dga
docker stop dga && docker rm -v dga
docker exec -u 0 -it dga bash
```
