import subprocess, os


def launch(port: int, headers: [str], backend1: str, backend2: str, ssl=None):
    assert (type(port) == type(1))
    name = "haproxy" + str(port)
    headers_str = ""
    for header in headers:
        headers_str += "http-request set-header " + header + "\n    "
    ssl_env = []
    if ssl:
        ssl_cert, ssl_key = ssl
        ssl_env = ["-e", "SSL_CERT=" + ssl_cert, "-e", "SSL_KEY=" + ssl_key]
    args_launch = ["docker", "run", "-d", "-it", "--rm", "--name", name, "-p", str(port) + ":" + str(port),
                   '--cpu-period=100000', '--cpu-quota=5000', "--ulimit", "nproc=10:10", "--ulimit",
                   "data=1000000:1000000", "-e", "CUSTOM_HEADERS=" + headers_str, "-e", "LISTEN_PORT=" + str(port),
                   "-e", "BACKEND1=" + backend1, "-e", "BACKEND2=" + backend2] + ssl_env + \
                  ["registry.insecurity-insa.fr/insecurity/haproxy"]
    args_delete = "(sleep 120 ; docker stop " + name + ") &"
    subprocess.call(args_launch)
    os.system(args_delete)


if __name__ == "__main__":
    launch(1234, ["test test"], "51.254.102.54:1234", "51.254.102.54:4321")
