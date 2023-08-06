import os
import sys


def main():
    if len(sys.argv) < 4:
        print('''
    add-header-mv <arg1> <arg2> <arg3>
    - arg1 : file name postfix, use it to get files, such as '.py' or '.java'
    - arg2 : header you want to add, such as 'import os' or 'package what.you.want;'
    - arg3 : target dir you want to move files to
        '''.strip())
        return None
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
        os.rename(p_abspath, os.path.join(target_path, java_file))
