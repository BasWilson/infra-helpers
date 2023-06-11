import datetime
import logging

from infra_helpers.paths import GetInfraPath


def PrintError(message):
    print(message)
    logging.error(message)


def PrintInfo(message):
    print(message)
    logging.info(message)


def SetupLogging():
    currentDate = datetime.datetime.now()
    logging.basicConfig(
        filename="{}/logs/{}.log".format(
            GetInfraPath(), datetime.datetime.isoformat(currentDate)
        ),
        level=logging.INFO,
    )
