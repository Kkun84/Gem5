import hydra
from logging import getLogger
import subprocess


logger = getLogger(__name__)


@hydra.main(config_path='config.yaml')
def main(config):
    command = []
    for key, value in config.items():
        logger.debug(key)
        logger.debug(value)
        if isinstance(value, bool) and value:
            command += [str(key)]
        else:
            command += [f"{key}={value}"]
    logger.info(command)
    result = subprocess.run(command)
    logger.info(result)



if __name__ == "__main__":
    main()