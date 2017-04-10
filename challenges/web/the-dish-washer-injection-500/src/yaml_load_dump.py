from ruamel import yaml
import sys


class DishWasher:
    def __init__(self, id: str, name: str, brand: str, cost: int, cve: str):
        self.id = id
        self.name = name
        self.brand = brand
        self.cost = cost
        self.cve = cve

if __name__ == "__main__":
    try:
        dumped = ""
        while True:
            try:
                dumped += input() + "\n"
                print(dumped, file=sys.stderr)
            except EOFError:
                break
        print("done", file=sys.stderr)
        print(dumped, file=sys.stderr)
        loaded = yaml.load(dumped[:-1])
        dumped = yaml.safe_dump(loaded.__dict__)
        sys.stdout.write(dumped)
    except Exception as e:
        print(e, file=sys.stderr)
