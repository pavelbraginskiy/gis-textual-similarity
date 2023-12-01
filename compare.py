import itertools
from collections import namedtuple
import pprint
import parse
import vectorize
import sys
import TrajectoryDistance
import glob
import csv

if __name__ == '__main__':
    files = glob.glob('books/**/*.txt', recursive=True)
    if len(sys.argv) > 1 and sys.argv[1] == '--train':
        vectorize.initialize(itertools.chain.from_iterable((parse.paragraphs(file)) for file in files))
        exit(0)

    trajectories = {file: vectorize.vectorize(parse.paragraphs(file)) for file in files}

    sample_size = (min(len(i) for i in trajectories.values()) - 10) // 2

    sampled = {file: trajectories[file][len(trajectories[file])//2-sample_size:len(trajectories[file])//2+sample_size]
               for file in files}

    trajectories = sampled

    print(trajectories.keys())

    Result = namedtuple('Result', 'dtw erp')
    results = {}

    for i in files:
        for j in files:
            if i == j or (i, j) in results or (j, i) in results:
                continue
            dtw = TrajectoryDistance.dtw(trajectories[i], trajectories[j])
            print(f'{i} <==> {j}, DTW: {dtw}')
            erp = TrajectoryDistance.erp(trajectories[i], trajectories[j])
            print(f'{i} <==> {j}, ERP: {erp}')

            results[(i, j)] = Result(dtw, erp)

    print('\n\n')
    print('=' * 40)
    print('\n\n')
    pp = pprint.PrettyPrinter(depth=4)
    pp.pprint(results)

    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow([''] + files)

        for method in (lambda i: i.dtw, lambda i: i.erp):
            for i in files:
                row = [i]
                for j in files:
                    if i == j:
                        row += ['']
                    else:
                        if (i, j) in results:
                            entry = results[(i, j)]
                        else:
                            entry = results[(j, i)]
                        row += [method(entry)]
                writer.writerow(row)
            writer.writerow([])
