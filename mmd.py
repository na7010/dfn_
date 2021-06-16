# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import time
from pathlib import Path

# コマンドライン引数を格納


def create_cmd_util(save_dir, dfn_name, input_path, num_cpu, i):
    """return cmd to execute run.py in dfnworks.

    Args:
        save_dir (Path): dir to save dfns. It means base dir. 
        dfn_name (srt): dfn name
        input_path (Path): path to the input file. ex) ~/gen.dat
        num_cpu (int): the number of cpu to use
        i (int): this is like id.

    Returns:
        cmd (str): commands for run.py
    """
    cmd = 'python run.py -name ' + str(save_dir / dfn_name) + \
        str(i) + ' -input ' + str(input_path) + ' -ncpu ' + str(num_cpu)
    return cmd


def make_many_dfn():
    """make many dfns for usual use. for TD.
    Args: 
        params: parameta for settings
    """

    args = get_args()
    i = 0
    fail_num = 0
    while i < args.num_dfn:
        os.chdir('/dfnWorks/pydfnworks/bin')
        cmd = create_cmd_util(
            save_dir=args.save_dir, dfn_name=args.dfn_name,
            input_path=args.input_path, num_cpu=args.num_cpu, i=i
        )
        subprocess.call(cmd.split())
        os.chdir(args.save_dir)
        os.chdir('dfn_' + str(i))
        check_error = str(subprocess.check_output(['tail', '-1', 'DFN_output.txt']))
        if 'Try' in check_error:
            os.chdir('../')
            command = 'rm -r dfn_' + str(i)
            subprocess.call(command.split())
            fail_num += 1
        else:
            i += 1
    print('fail ' + str(fail_num))


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--save_dir',
        type=Path,
        default=Path('/root/src_hattori'),
        help='保存先dir'
    )
    parser.add_argument(
        '--dfn_name',
        default='dfn_',
        help='dfnのなまえ'
    )
    parser.add_argument(
        '--num_dfn',
        default=2,
        type=int,
        help='作るdfnの数'
    )
    parser.add_argument(
        '--num_cpu',
        default=20,
        help='使用cpu数'
    )
    parser.add_argument(
        '--input_path',
        type=Path,
        default=Path('/root/datadrive/predict_pathline/input/TD2.txt'),
        help='inputファイル'
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    print(args)

    make_many_dfn()


