from utils.consts import *
import utils.consts
import time
from load.load_data import *
from utils.analysisutil import plot_comparison
from utils.analysisutil import plot_Astar_T
from inteval.inteval_rij import *
import itertools

start = time.time()
#plot_Astar_T()
#input()

#get_reviewer_labels()  # 用于从SpEagle结果中提取标签信息
#algo_rank = [1,2,3,6,5,4,7,8] # human evaluation order for algorithms, 1 = best, then 2, 3, ...
algo_rank = [1,2,3,4,8,7,6,5,9,11,10,12,13,14]
#algo_rank = [1,2,3,4,5,6,7,8]

P = len(collueagle_file)
file_combinations = list(itertools.combinations(list(range(P)), 14))

sim_evaluation = []
for cb in file_combinations:
    # select files
    ranking_files = []
    for i in cb:
        ranking_files.append(collueagle_file[i])
        print(collueagle_file[i][1])

    # initialize global variables
    rl_dict = {}

    P = len(ranking_files)
    print('P=', P)
    for i in range(len(ranking_files)):
        rl_dict[i] = load_ranking_list(path + 'data\\' + ranking_files[i][0])

    similarities = inteval_rij(P, rl_dict, ranking_files)
    similarities.pop()
    print('similarities:', similarities)
    sim_alg_ranking = similarity_algo(cb, algo_rank, similarities)
    sim_evaluation.append(sim_alg_ranking)
    print('Evaluation by sim:', sim_alg_ranking)


print('Average similarity (Evaluation by Similarity):',
      np.mean(sim_evaluation))
print(*sim_evaluation)

end = time.time()
runtime = (end - start) / 60
print("Time elapsed：", runtime, "min")




