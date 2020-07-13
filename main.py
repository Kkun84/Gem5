import hydra
from logging import getLogger
import subprocess
import pandas


logger = getLogger(__name__)


def get_clock(csv_path, l1size, l1assoc):
    df = pandas.read_csv(csv_path)
    access_time = df[(df['cache_size'] == l1size) & (df['associativity'] == l1assoc)]['access_time[ns]']
    clock = float(1e9 / access_time)
    return clock


@hydra.main(config_path='config.yaml')
def main(config):
    clock = get_clock(hydra.utils.to_absolute_path(config.access_time.csv_path), config.l1size, config.l1assoc)
    command = []
    for key, value in config.command.items():
        logger.debug(key)
        logger.debug(value)
        if value is None:
            if key == '--cpu-clock':
                command += [f"{key}={clock}Hz"]
        elif isinstance(value, bool) and value:
            command += [str(key)]
        else:
            command += [f"{key}={value}"]
        logger.debug(command[-1])
    logger.info(command)
    result = subprocess.run(command)
    logger.info(result)


if __name__ == "__main__":
    main()