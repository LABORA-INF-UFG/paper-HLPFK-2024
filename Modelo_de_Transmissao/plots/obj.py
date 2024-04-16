import pandas as pd
import matplotlib.pyplot as plt 



def read_data(file_name):
    data = []
    # Using readlines()
    file = open(file_name, 'r')
    lines = file.readlines()

    count = 0
    
    for line in lines:
        count += 1
        data.append(float(line.strip().split()[0]))
        
    return data

if __name__ == "__main__":
    timeOpt = read_data('../outputs/model.txt')
    timeSA = read_data('../outputs/metaheuristica.txt')

    x = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
    fig,ax = plt.subplots()

    fig.set_size_inches(10, 4.5)
    ax.plot(x, timeOpt, "-o", label="Ótimo - ILP", linewidth=2.0, markersize=12, color='red')
    ax.plot(x, timeSA, "-^", label="Meta-heurística", linewidth=2.0, markersize=12, color='#006bb3')

    ax.set_xlabel("Número de usuários", fontsize=22, labelpad=8)
    ax.set_ylabel(r"BIP $(\sum_{i \in \mathcal{U}} P_i)$",fontsize=22)

    ax.set_xticks(x)
    ax.set_xticklabels(x, fontsize=22)

    ticks = [0, 1000, 2000, 3000, 4000]

    for i,j,l  in zip(timeOpt,timeSA,x):

        gap = (1-(i/j))*100

        label = "{:.2f}%".format(gap)
        if l == 300:
            ax.annotate("*",(l,i), textcoords="offset points", xytext=(0,-40), ha='center', fontsize=40, color='red') 

        
    ax.set_yticks(ticks)
    ax.set_yticklabels(ticks, fontsize=22)

    ax.legend(fontsize=20)
    ax.grid(axis='y', which='major', linestyle='--')
    plt.savefig("obj.pdf", bbox_inches='tight')
    plt.savefig("obj.png", bbox_inches='tight')
    #plt.show()