# Build

```bash
docker build -t registry.insecurity-insa.fr/insecurity/captcha-audio .
```

# Run

```bash
docker run -it \
           -d --restart=always \
           --name captcha-audio \
           -p 2052:8070 \
           --cpu-period="100000" --cpu-quota="90000" \
           --ulimit nproc=1024:1024 \
           registry.insecurity-insa.fr/insecurity/captcha-audio
docker stop captcha-audio && docker rm -v captcha-audio
docker exec -u 0 -it captcha-audio bash
```
