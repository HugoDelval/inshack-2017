# Challenges status monitoring

## Build

```bash
cd ..
docker build -t registry.insecurity-insa.fr/insecurity/challenges-monitoring -f challenges-monitoring/Dockerfile .
```

## Run

```bash
mkdir /dbdumps
docker run -d --restart=always --cpu-period="100000" --cpu-quota="90000" -e PASSWORD=FIXME -e USERNAME=FIXME --name monitoring -v /dbdumps:/backup -it -p 8080:5000 registry.insecurity-insa.fr/insecurity/challenges-monitoring
docker stop monitoring && docker rm -v monitoring
```

## Login as root

```bash
docker exec -u 0 -it monitoring bash
```
