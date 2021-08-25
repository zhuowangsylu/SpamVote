import math
import matplotlib.pyplot as plt
from utils.consts import *
import sklearn.metrics as metrics
import os

#输入A*排序结果，分析并计算其精度，ndcg@k, ap@k等。
# vbelief的结构：index，rid，score,label
def result_anal(vbelief, dirname):
    # if not os.path.exists(dirname):
    #     os.mkdir(dirname)
    fp = open(dirname, 'w')
    # fpshort = open(dirname + '_A_star_ri_2000000' + '_short.csv', 'w')
    correct = 0
    dcg = 0
    idcg = 0
    sumAP = 0
    nAP = 0
    label = []
    probs = []
    for i, b in enumerate(vbelief):
        label.append(int(b[3]))
        probs.append(float(b[2]))
        idcg += 1 / math.log(i + 2, 2)
        if int(b[3]) == 1:
            correct += 1
            dcg += 1 / math.log(i + 2, 2)
            sumAP += correct / (i + 1)
            nAP += 1
        else:
            #dcg += 1 / math.log(i + 2, 2)
            sumAP += correct / (i + 1)
            nAP += 1
        # auc = metrics.roc_auc_score(label, probs)
        b.extend([sumAP / nAP if nAP != 0 else 0, correct / (i + 1), dcg / idcg])

    # r, spam, label, neighbor, pri, gsize, gindex
    # fp.writelines("pos\trid\tspam\tAP\tPrecision\tNDCG\tlabel\n")
    # fpshort.writelines("top\tpos\trid\tspam\tAP\tPrecision\tNDCG\tlabel\n")

    for k, b in enumerate(vbelief):
        fp.writelines("%s\t%s\t%.4f\t%.4f\t%.4f\t%.4f\t%s\n" % (
            b[0], b[1], b[2], b[4], b[5], b[6], b[3]))
        # if (k + 1) % 10 == 0:
        #     fpshort.writelines("%s\t%s\t%s\t%.4f\t%.4f\t%.4f\t%.4f\t%s\n" % (
        #         str(k+1), b[0], b[1], b[2], b[4], b[5], b[6], b[3]))
    fp.close()
    # fpshort.close()


def plot(P, file, TopPlot=50000, name='YelpZip'):
    if TopPlot > 30000:
        TopPlot = 30000
    alg_c = alg_color[:P]+['black', 'r']
    alg_l = alg_lstyle[:P]+['-.', '-']
    # 画图
    fig1 = plt.figure(str(name) + ' NDCG@k (Top = ' + str(Top)+ ')')
    plt.title(str(name) + ' (T = ' + str(Top)+ ')', fontsize=20)
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示字体为黑体
    # plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号
    plt.xlabel('k', fontsize=14)
    plt.ylabel('NDCG@k', fontsize=14)
    plt.tick_params(labelsize=10)  # 设置横纵轴标签的字体大小
    plt.grid(axis='y', linestyle=':')  # 画网格，只画与y相关的网格

    # Precision
    fig2 = plt.figure(str(name) + ' precision@k (Top = ' + str(Top)+')')
    plt.title(str(name) + ' (T = ' + str(Top)+')', fontsize=20)
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示字体为黑体
    # plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号
    plt.xlabel('k', fontsize=14)
    plt.ylabel('Precision@k', fontsize=14)
    plt.tick_params(labelsize=10)  # 设置横纵轴标签的字体大小
    plt.grid(axis='y', linestyle=':')  # 画网格，只画与y相关的网格

    # Precision
    fig3 = plt.figure(str(name) + ' AP@k (Top = ' + str(Top)+")")
    plt.title(str(name) + ' (T = ' + str(Top)+')', fontsize=20)
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示字体为黑体
    # plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号
    plt.xlabel('k', fontsize=14)
    plt.ylabel('AP@k', fontsize=14)
    plt.tick_params(labelsize=10)  # 设置横纵轴标签的字体大小
    plt.grid(axis='y', linestyle=':')  # 画网格，只画与y相关的网格

    # AUC
    fig4 = plt.figure(str(name) + ' AUC@k (Top = ' + str(Top)+')')
    plt.title(str(name) + ' (T = ' + str(Top)+')', fontsize=20)
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示字体为黑体
    # plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号
    plt.xlabel('k', fontsize=14)
    plt.ylabel('AUC@k', fontsize=14)
    plt.tick_params(labelsize=10)  # 设置横纵轴标签的字体大小
    plt.grid(axis='y', linestyle=':')  # 画网格，只画与y相关的网格

    for i in range(len(file)):
        if os.access(path + 'data\\' + file[i][0], os.F_OK):
            f1 = open(path + 'data\\' + file[i][0])
        else:
            f1 = open(path + 'output\\' + file[i][0])
        rf1 = f1.readlines()

        x = []  # x轴
        ndcg_y = []  # y轴
        precision_y = []  # y轴
        ap_y = []
        label = []  # 标签列
        probs = []  # 概率列
        auc = []
        auc_x = []
        auc_label = []
        auc_probs = []

        # read data from ranking list file
        for j, line in enumerate(rf1):
            if j >= TopPlot: break
            if j % 100 != 99: continue
            line = line.replace(" ", "").replace("\n", "")
            line = line.split("\t")

            x.append(int(line[0]))  # 序号
            ndcg_y.append(float(line[5]))  # NDCG
            precision_y.append(float(line[4]))  # precision
            ap_y.append(float(line[3]))  # AP
            label.append(int(line[6]))  # 标签列
            probs.append(float(line[2]))  # 概率列

            auc_label.append(int(line[6]))  # 标签列
            auc_probs.append(float(line[2]))  # 概率列

        ax1 = fig1.add_subplot(1, 1, 1)
        ax1.plot(x, ndcg_y, linestyle=alg_l[i], color=alg_c[i],  label=file[i][1])
        ax1.legend()  # 显示图例

        ax2 = fig2.add_subplot(1, 1, 1)
        ax2.plot(x, precision_y, linestyle=alg_l[i], color=alg_c[i], label=file[i][1])
        ax2.legend()  # 显示图例

        ax3 = fig3.add_subplot(1, 1, 1)
        ax3.plot(x, ap_y, linestyle=alg_l[i], color=alg_c[i], label=file[i][1])
        ax3.legend()  # 显示图例
        try:
            for k in range(100, TopPlot + 1, 100):
                auc_x.append(k)
                AUC = metrics.roc_auc_score(auc_label[0:k], auc_probs[0:k])
                auc.append(AUC)
                # print("auc=", auc)
            ax4 = fig4.add_subplot(1, 1, 1)
            ax4.plot(auc_x, auc, linestyle=alg_l[i], color=alg_c[i],  label=file[i][1])
            ax4.legend()  # 显示图例
        except:
            print("没有作弊标签！AUC计算失效！")
        print("第" + str(i + 1) + "个文件结束！")

    # 保存图像
    fig1.savefig(path + 'output\\' + str(name) + '_NDCG@k=' + str(Top) + '.pdf', format='pdf')
    fig1.show()

    fig2.savefig(path + 'output\\' + str(name) + '_precision@k=' + str(Top) + '.pdf', format='pdf')
    fig2.show()

    fig3.savefig(path + 'output\\' + str(name) + '_AP@k=' + str(Top) + '.pdf', format='pdf')
    fig3.show()

    fig4.savefig(path + 'output\\' + str(name) + '_AUC@k=' + str(Top) + '.pdf', format='pdf')
    fig4.show()

    print("全部读取结束")
    f1.close()


def plot_comparison(P, ranking_files, N):
    #alg_color.extend(['black', 'r'])
    #alg_lstyle.extend(['-', ':'])
    # alg_marker.extend([None, None])
    ranking_files.extend([['A_bar.txt', r'$\overline{A}$'], ["A_star.txt", r'${A^*}$']])
    plot(P, ranking_files, N)


def plot_Astar_T(name='Astar'):
    ''' Compare A stars'''
    TopPlot = 30000
    alg_c = ['crimson', 'r', 'orangered', 'tomato', 'coral']
    alg_l = ['--', '-', '--',':','-']
    # 画图
    fig1 = plt.figure(str(name) + ' NDCG@k')
    plt.title('', fontsize=20)
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示字体为黑体
    # plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号
    plt.xlabel('k', fontsize=14)
    plt.ylabel('NDCG@k', fontsize=14)
    plt.tick_params(labelsize=10)  # 设置横纵轴标签的字体大小
    plt.grid(axis='y', linestyle=':')  # 画网格，只画与y相关的网格

    file=[['A_star_T50000.txt', 'T=50,000'],
          ['A_star_T20000.txt', 'T=20,000'],
          ['A_star_T10000.txt', 'T=10,000'],
          ['A_star_T5000.txt', 'T=5,000'],
          ['A_star_T2000.txt', 'T=2,000']
         ]
    for i in range(len(file)):
        f1 = open(path + 'output\\' + file[i][0])
        rf1 = f1.readlines()

        x = []  # x轴
        ndcg_y = []  # y轴
        precision_y = []  # y轴
        ap_y = []
        label = []  # 标签列
        probs = []  # 概率列

        # read data from ranking list file
        for j, line in enumerate(rf1):
            if j >= TopPlot: break
            if j % 100 != 99: continue
            line = line.replace(" ", "").replace("\n", "")
            line = line.split("\t")

            x.append(int(line[0]))  # 序号
            ndcg_y.append(float(line[5]))  # NDCG
            precision_y.append(float(line[4]))  # precision
            ap_y.append(float(line[3]))  # AP
            label.append(int(line[6]))  # 标签列
            probs.append(float(line[2]))  # 概率列

        ax1 = fig1.add_subplot(1, 1, 1)
        ax1.plot(x, ndcg_y, linestyle=alg_l[i], color=alg_c[i],  label=file[i][1])
        ax1.legend()  # 显示图例

        print("第" + str(i + 1) + "个文件结束！")

    # 保存图像
    fig1.savefig(path + 'output\\' + str(name) + '_NDCG@k.pdf', format='pdf')
    fig1.show()

    print("Comparing A stars finished.")
    f1.close()
