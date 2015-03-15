def slurp(path):
    with open(path, "r") as fd:
        return [line.rstrip() for line in fd.readlines()]
