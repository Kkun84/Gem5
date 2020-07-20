import hydra
from hydra.utils import to_absolute_path
from logging import getLogger
import subprocess
import pandas


logger = getLogger(__name__)


def get_clock(csv_path, l1size, l1assoc):
    df = pandas.read_csv(csv_path)
    access_time = df[(df['cache_size'] == l1size) & (df['associativity'] == l1assoc)]['access_time[ns]']
    print(access_time)
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


def write_sim_ticks(csv_path, core, clock, l1size, l1assoc, l2size, l2assoc, latency, save_params):
    df = pandas.DataFrame(dict(
        core=[core],
        clock=[clock],
        l1size=[l1size],
        l1assoc=[l1assoc],
        l2size=[l2size],
        l2assoc=[l2assoc],
        latency=[latency],
        **save_params
    ))
    df.to_csv(csv_path, mode='a', header=False)
    return


@hydra.main(config_path='config.yaml')
def main(config):
    clock = get_clock(to_absolute_path(config.access_time.csv_path), config.l1size, config.l1assoc)
    command = []
    for key, value in config.command.items():
        logger.info(key)
        logger.info(value)
        if value is None:
            if key == '--cpu-clock':
                command += [f"{key}={clock}Hz"]
        elif isinstance(value, bool) and value:
            command += [str(key)]
        else:
            command += [f"{key}={value}"]
        logger.info(command[-1])
    logger.info(command)
    result = subprocess.run(command)
    logger.info(result)

    with open(f"{config.outdir}stats.txt") as f:
        s = f.read()
        if not s:
            logger.info('File is empty.')
            return

    save_params = dict()
    for param_name in config.result.save_params:
        param = get_from_stats(f"{config.outdir}", param_name)
        if len(param) > 1:
            for i, p in enumerate(param):
                save_params[f"{param_name}[{i}]"] = p
        else:
            save_params[param_name] = param[0]
    logger.info(save_params)

    logger.info('Save CSV.')
    write_sim_ticks(to_absolute_path(config.result.csv_path), config.core, clock, config.l1size, config.l1assoc, config.l2size, config.l2assoc, config.latency, save_params)

    logger.info('Done all.')


if __name__ == "__main__":
    main()
