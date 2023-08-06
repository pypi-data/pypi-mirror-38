import os
import sys


def main():
    file_postfix = sys.argv[1]
    added_header = sys.argv[2]
    target_path = sys.argv[3]
    all_dirs_and_files = os.listdir()
    java_files = tuple(
        filter(lambda x: x.endswith(file_postfix), all_dirs_and_files))
    for java_file in java_files:
        p = open(java_file, 'rt')
        privious = p.read()
        p.close()
        f = open(java_file, 'wt')
        f.write(added_header + '\n')
        f.write(privious)
        f.close()
        p_abspath = os.path.abspath(java_file)
        os.rename(p_abspath, target_path + '/' + java_file)
