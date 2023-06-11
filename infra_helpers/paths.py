import os


def GetInfraPath():
    base = os.path.realpath(os.path.dirname(__file__))
    return base + "/../.infra"
