import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv
from csv import DictReader
from copy import copy
from collections import defaultdict

#regular
LINE_STYLE = ['b:+', 'g-', 'r-s', 'c--', 'k-.', 'r--', 'g-x']
#increasingk
#LINE_STYLE = ['b--s', 'b-s', 'g--x', 'g-x', 'r--', 'r-', 'k-.']
#reqnum
#LINE_STYLE = ['b-.', 'r--', 'g-', 'c:+', 'k:']

def create_example_csv():
    with open('output_demo.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["sys_util", "Alg_A", "Alg_B"])
        writer.writerow([0, 1.0, 1.0])
        writer.writerow([0.2, 0.9, 0.8])
        writer.writerow([0.4, 0.5, 0.4])
        writer.writerow([0.6, 0.2, 0.1])
        writer.writerow([0.8, 0, 0])

def main():
    create_example_csv()
    file = 'output_demo.csv'
    f = open(file, 'r')
    d = DictReader(f)
    data = defaultdict(list)
    for row in d:
        for key, value in row.items():
            data[key].append(value)

    cols = copy(d.fieldnames)
    cols.remove("sys_util")

    plt.figure(figsize=(8,4))
    for style, col in enumerate(cols):
        plt.plot(data["sys_util"], data[col], LINE_STYLE[style], label=col, linewidth=2.0)

    #plt.legend(loc="lower left")
    plt.legend(loc="best")
    
    plt.ylabel("HRT Schedulability")
    plt.xlabel("System Utilization")

    plt.savefig(file[:-4]+".pdf")
    plt.savefig(file[:-4]+".png")
    plt.close()

if __name__ == '__main__':
    main()