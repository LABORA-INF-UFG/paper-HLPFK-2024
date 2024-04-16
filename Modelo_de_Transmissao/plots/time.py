import pandas as pd
import matplotlib.pyplot as plt 


#things = '80'
#df = pd.read_csv('../saidas/SA/' + things + '_solution.csv', sep=';')

def read_data(file_name):
    data = []
    # Using readlines()
    file = open(file_name, 'r')
    lines = file.readlines()

    count = 0
    
    for line in lines:
        count += 1
        data.append(float(line.strip().split()[1]))
        
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
    ax.set_ylabel("tempo (s)",fontsize=22)

    ax.set_xticks(x)
    ax.set_xticklabels(x, fontsize=22)

    ticks = [0, 1000, 2000, 3000, 4000]
    
    for i,j,l  in zip(timeOpt,timeSA,x):

        labelI = "{:.2f}s".format(i)
        labelJ = "{:.2f}s".format(j)

        if l == 300:
            ax.annotate("*",(l,400), textcoords="offset points", xytext=(0,0), ha='center', color='red', fontsize=40) 
            
    ax.set_yticks(ticks)
    ax.set_yticklabels(ticks, fontsize=22)

    plt.yscale("log")
    
    ax.legend(fontsize=20)
    ax.grid(axis='y', which='major', linestyle='--')
    plt.savefig("time.pdf", bbox_inches='tight')
    plt.savefig("time.png", bbox_inches='tight')
    #plt.show()