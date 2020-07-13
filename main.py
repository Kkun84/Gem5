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


def get_from_stats(text_dir, param):
    with open(f"{text_dir}stats.txt") as f:
        for s_line in f:
            if param in s_line[:len(param)]:
                break
        else:
            return
    s_line = s_line[len(param):s_line.find('#')]
    s_list = [i for i in s_line.split(' ') if i]
    return s_list


def write_sim_ticks(csv_path, core, l1size, l1assoc, l2size, l2assoc, latency):
    df = pandas.csv_path
    df.to_csv(csv_path, mode='a', header=None)
    return


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

    save_params = dict()
    for param_name in config.result.save_params:
        param = get_from_stats(f"{config.outdir}", param_name)
        if len(param) > 1:
            for i, p in enumerate(param):
                save_params[f"{param_name}[{i}]"] = p
        else:
            save_params[param_name] = param[0]
    logger.info(save_params)


if __name__ == "__main__":
    main()