from utils.consts import *
from utils.analysisutil import result_anal
from utils.analysisutil import plot_comparison
import numpy as np
import matplotlib.pyplot as plt
import operator
import math

# rl1、rl2相似度，以字典存储，key= rid, value= position
def similarity(r_dict, i):
    '''sim(A*,Ai)'''
    dis = 0
    for rid, val in r_dict.items():
        dis += abs(val[0] - r_dict[rid][3][i])
    return 1 - dis / int(0.5*(len(r_dict) ** 2))

def similarity_ik(r_dict, i, k):
    '''sim(Ai,Ak)'''
    dis = 0
    for rid, val in r_dict.items():
        dis += abs(r_dict[rid][3][k] - r_dict[rid][3][i])
    return 1 - dis / int(0.5 * (len(r_dict) ** 2))

def Jaccard_ik(rl_dict, i, k):
    iset = set()
    kset = set()
    for key in rl_dict[i]:
        iset.add(key)
    for key in rl_dict[k]:
        kset.add(key)
    return len(iset & kset) / len(iset | kset)

def similarity_algo(cb, algo_rank, similarities):
    '''use similarities between an algorithm and A_star to evaluate ranking algorithms'''
    human_dict = {}
    sim_dict = {}
    human_list = []
    sim_list = []

    for i, algo_no in enumerate(cb):
        human_list.append([algo_no, algo_rank[algo_no]])
        sim_list.append([algo_no, similarities[i]])
    human_list.sort(key=operator.itemgetter(1))
    sim_list.sort(key=operator.itemgetter(1), reverse=True)
    for i, algo in enumerate(human_list):
        human_dict[algo[0]] = i
    for i, algo in enumerate(sim_list):
        sim_dict[algo[0]] = i

    s = 0
    for k, v in human_dict.items():
        s += abs(v - sim_dict[k])

    return 1 - s/int(0.5*(len(sim_dict)**2))


def inteval_rij(P, rl_dict, ranking_files):
    r_dict = {}
    # find distinct items from all ranking lists, and initialize
    for i in range(P):
        for rid, val in rl_dict[i].items():
            if rid not in r_dict:
                # key= rid, value=[score, label, rij, P positions plus Abar positions]
                r_dict[rid] = [0, val[1], [2 / 3] * P, [0] * (P + 1)]

    N = len(r_dict)  # number of rids, for Top items of P algs
    print('Total number of items:', N)

    # sum up all the positions of items for all algs
    for rid, val in r_dict.items():
        for i in range(P):
            if rid in rl_dict[i]:
                pij = rl_dict[i][rid][0]
            else:
                pij = int((len(rl_dict[i]) + N) / 2)
            val[0] += pij
            val[3][i] = pij # store the positions of items in algs

    # init A_star
    A_star = []
    for rid, value in r_dict.items():
        A_star.append([rid, value[0]])
    A_star.sort(key=operator.itemgetter(1))
    # A bar (sort by average positions)

    for i, item in enumerate(A_star):
        r_dict[item[0]][0] = i + 1  # the new position of rid in A_star
        r_dict[item[0]][3][P] = i + 1  # save A bar

    # 输出初始的排序结果，计算其精度指标
    A_star_temp = []
    for i, a in enumerate(A_star):
        # a[1]: min-max normalization for probability transformation
        A_star_temp.append([i, a[0], 1 - (a[1] - A_star[0][1]) / (A_star[len(A_star) - 1][1] - A_star[0][1]), r_dict[a[0]][1]])  # index, rid, score, label
    # 输出列名"pos\trid\tspam\tlabel\tAP\tPrecision\tNDCG\n"
    result_anal(A_star_temp, path + "output\\A_bar.txt")

    # pre-vote analysis
    JList = []
    print('Jaccard co-efficient matrix among A1 to Ap:')
    for i in range(P):
        for k in range(i):
            J = Jaccard_ik(rl_dict, i, k)
            JList.append(J)
            print('{:.4f}'.format(J), end=' ')
        print()
    print('     mean J:', np.mean(JList), 'std J:', np.std(JList))
    print('Similarity matrix among A1 to Ap:')
    for i in range(P):
        for k in range(i):
            print('{:.4f}'.format(similarity_ik(r_dict, i, k)), end=' ')
        print()
    input('Press any key')

    eps = 1e-6
    Q = P # current number of algorithms for ensemble
    #while Q > P-1:
    iter = 0
    diff_sum_list = []

    while iter <= 200:  # True:
        iter += 1
        print('iter', iter, 'of Q', Q)
        max_diff = 0
        diff_sum = 0
        # estimate mean and variance of the deviations of positions
        dev = []
        for rid, val in r_dict.items():
            pstarj = val[0]
            for i in range(Q):
                pij = val[3][i]
                dev.append(pstarj - pij)
        miu_hat = np.mean(dev)
        var_hat = np.var(dev)

        # update rij
        for rid, val in r_dict.items():
            rij_old = val[2].copy()
            pstarj = val[0]

            for i in range(Q):
                pij = val[3][i]
                x = pstarj - pij

                try:
                    # Gaussian rij
                    #val[2][i] =  math.exp(-(x-miu_hat)**2/(2*var_hat)) / ((2*math.pi*var_hat)**0.5)
                    # Gaussian kernel rij
                    val[2][i] = math.exp(-(x-miu_hat)**2/(var_hat))
                    # Sigmoid rij
                    #val[2][i] = -2 * (1/(1+math.exp(-x/(var_hat**0.5))) - 1)
                except:
                    print('exp error:', pij, pstarj)
            for i in range(Q):
                diff = abs(val[2][i] - rij_old[i])
                if max_diff < diff :
                    max_diff = diff
                diff_sum += diff

        print('diff_sum=', diff_sum)
        diff_sum_list.append(diff_sum)
        if max_diff <= eps:
            break
        # update A_star
        A_star = []
        for rid, val in r_dict.items():
            score, score2 = 0, 0
            pstarj = val[0]
            for i in range(Q):
                pij = val[3][i]
                #score += val[2][i]*pij + (1-val[2][i])*pstarj # Balance of pij and p*j
                score += val[2][i] * pij # Weighted mean of pij
                score2 += val[2][i] # Weighted mean of pij

            score = score/score2  # Weighted mean of pij

            A_star.append([rid, score])

        A_star.sort(key=operator.itemgetter(1))

        for i, item in enumerate(A_star):
            r_dict[item[0]][0] = i + 1  # update the item position

    print('Finished!')

    A_star_temp = []
    for i, a in enumerate(A_star):
        A_star_temp.append([i, a[0], 1 - (a[1] - A_star[0][1]) / (A_star[len(A_star) - 1][1] - A_star[0][1]), r_dict[a[0]][1]]) # index, rid, score, label

    # 计算好A_star的各项精度并输出到文件输出A
    # 输出列名"pos\trid\tspam\tlabel\tAP\tPrecision\tNDCG\n"
    result_anal(A_star_temp, path + "output\\A_star.txt")

    # plot convergence
    if len(diff_sum_list)>0: del diff_sum_list[0]

    plt.title("diff_sum", fontsize=20)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示字体为黑体
    plt.plot(diff_sum_list, label="diff_sum", marker='o')
    plt.xlabel("iter")
    plt.ylabel("diff_sum")
    plt.legend()
    plt.show()

    print('similarity comparision:')
    sim = []
    for i in range(Q + 1):
        sim.append(similarity(r_dict, i))
    print('Sim:', end=' ')
    for s in sim:
        print('{:.4f}'.format(s), end=' ')
    print()

    # min_sim_alg = sim.index(min(sim))
    # print('removed alg:', min_sim_alg)
    #
    # for rid, val in r_dict.items():
    #     if Q != P:
    #         val[2].pop()
    #         val[3].pop()
    #     val[2].pop(min_sim_alg)
    #     val[3].pop(min_sim_alg)
    #     val[2].append(2/3)
    #     val[3].append(val[0])
    # Q -= 1

    # save rij
    with open(path + r'output\rij.txt', 'w') as f:
        for rid, val in r_dict.items():
            rij = ''
            for i in range(Q):
                rij += '{:.6f}\t'.format(val[2][i])
            f.write('{:8}\t'.format(rid)+ rij +'\n')

    plot_comparison(P, ranking_files, N)

    return sim

