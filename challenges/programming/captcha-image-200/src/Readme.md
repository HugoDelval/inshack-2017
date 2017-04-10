# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/captcha-image .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name captcha-image \
           -p 2052:80 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           registry.insecurity-insa.fr/insecurity/captcha-image
docker stop captcha-image && docker rm -v captcha-image
docker exec -u 0 -it captcha-image bash
```
