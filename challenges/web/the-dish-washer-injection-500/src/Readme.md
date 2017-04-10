# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/the-dish-washer-injection .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name the-dish-washer-injection \
           -p 2052:8080 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           --ulimit data=1000000:1000000 \
           registry.insecurity-insa.fr/insecurity/the-dish-washer-injection
docker stop the-dish-washer-injection && docker rm -v the-dish-washer-injection
docker exec -u 0 -it the-dish-washer-injection bash
```
