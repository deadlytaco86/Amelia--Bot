import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def create_coef_plot(c_dir, *args):
    matplotlib.use('Agg')
    degree = len(args) - 3
    x1 = float(args[0])
    x2 = float(args[1])
    span = x2 - x1
    points = int(span*20)
    x = np.linspace(x1,x2,points)
    y = np.zeros(len(x))
    for i in range(degree + 1):
        y += float(args[i+2])*x**(degree-i)
    plt.plot(x,y,'b-')
    plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
    plt.grid(which='minor', color='#EEEEEE', linewidth=0.5)
    plt.minorticks_on()
    plt.title("Your polynomial Graph")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.savefig(f"{c_dir}/bot_data/graph_data/graph.png")
    plt.close()