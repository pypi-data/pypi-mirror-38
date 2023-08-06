import os
import sys
from getopt import getopt
from traceback import print_exc


def find_and_uninstall(parent, deep):
    deep = deep - 1
    files = os.listdir(parent)


    # deep = deep - 1
    # files = os.listdir(parent)
    # if dir_hook in files and os.path.isdir(parent):
    #     dir_hook_file = parent + os.sep + dir_hook
    #     pre_receive_file = dir_hook_file + os.sep + pre_receive
    #     pre_receive_backup_file = dir_hook_file + os.sep + pre_receive_backup
    #
    #     print("found git repository : " + os.path.abspath(pre_receive_file))
    #
    #     hooks = os.listdir(dir_hook_file)
    #     if pre_receive in hooks and os.path.isfile(pre_receive_file):
    #         os.rename(pre_receive_file, pre_receive_backup_file)
    #     os.symlink(gitcepter_path, pre_receive_file)
    # elif deep > 0:
    #     for file in files:
    #         suffix = os.path.splitext(file)[1]
    #         basename = os.path.basename(file)
    #         if os.path.isdir(file) and (suffix == '.git' or basename == '.git'):
    #             unfind_and_install(parent + os.path.sep + file, deep)



def main():
    deep = 0
    try:
        opts, args = getopt(sys.argv[1:], "d:")
        for op, value in opts:
            if op == '-d':
                deep = value

        if deep == 0 and len(sys.argv) > 1:
            deep = int(sys.argv[1])

        find_and_uninstall(os.getcwd(), deep)
    except Exception:
        # Flush the problems we have printed so far to avoid the traceback
        # appearing in between them.
        sys.stdout.flush()
        print(file=sys.stderr)
        print('An error occurred, but the commits are accepted.', file=sys.stderr)
        print_exc()
