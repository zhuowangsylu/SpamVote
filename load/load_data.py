from utils.consts import *
import operator
from utils.analysisutil import result_anal

def load_ranking_list(filename):
    # matrix = np.loadtxt(filename, dtype=int)
    #k = 0
    dict = {}
    item_fetched = 0
    with open(filename, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if Top>0 and item_fetched >= Top: break
            items = line.strip().split()
            rid, label = items[1], items[6]
            #if 1000<=i<k+1000 and label =='0':
                #pass
            #else:
            dict[int(rid)] = [(i + 1), int(label)]  # 获取rid在算法中的排序位置,及其标签
            item_fetched += 1
    print(len(dict), 'items loaded from', filename)
    return dict

def get_reviewer_labels():
    file_meta = 'C:\\MyCode\\spamguard\\dataset\\Zip\\metadata (2).txt'
    r_label={}
    with open(file_meta,'r') as f:
        for i, line in enumerate(f.readlines()):
            items = line.strip().split()
            rid, label = int(items[0]), int(items[3])
            label = 1 if label == -1 else 0
            r_label[rid] = label

    file_alg = path + r'data\speagle_zip_userBelief_ALL.txt'
    file_alg_rank = path + r'data\speagle_zip_ALL.txt'

    reviewer_list = []
    with open(file_alg,'r') as f:
        for i, line in enumerate(f.readlines()):
            items = line.strip().split()
            rid, spam = int(items[0]), float(items[2])
            reviewer_list.append([rid, spam])

    reviewer_list.sort(key=operator.itemgetter(1), reverse=True)
    temp_list=[]
    for i, v in enumerate(reviewer_list):
        temp_list.append([i, v[0], v[1], r_label[v[0]]])

    result_anal(temp_list, file_alg_rank)
    print('File converted..')

