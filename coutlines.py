import os
import glob
import json
import subprocess
import sys

from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

def wccount(filename):
    out = subprocess.Popen(['wc', '-l', filename],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT
                         ).communicate()[0]
    return int(out.partition(b' ')[0])


def countlines(directory):
    files = glob.glob(os.path.join(directory, '*'))
    with ThreadPool(10) as Tp:
        total_lines = sum(Tp.map(wccount, files))

    return {os.path.basename(directory): {
        'files': len(files),
        'estimated_total_lines': len(files) * 1000000,
        'total_lines': total_lines
    }}


def main():
    result = dict()
    directory = sys.argv[1]
    directories = [os.path.join(directory, i) for i in os.listdir(directory)]
    with Pool(10) as p:
        x = p.map(countlines, directories)
    for i in x:
        result.update(i)
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
