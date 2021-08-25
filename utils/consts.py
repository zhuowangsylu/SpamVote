# path = 'D:\\e\\pyworkspace\\e-book-deeplearning\\'
#path = 'F:\\IntEvalCourse\\IntEval5.1\\'
path = 'C:\\Users\\syluw\\OneDrive\\研究生教学\\李慧\\SpamVote\\'
# 文件名，别名
collueagle_file = [
    ['ColluEagle_NT_d=0.5_e=0.5_90_3_0.6(e4wij)_allsize', 'CE_NT(0.6)'],
    ['ColluEagle_NT_d=0.5_e=0.5_90_3_0.7(e4wij)_allsize', 'CE_NT(0.7)'],
    ['ColluEagle_NT_d=0.5_e=0.5_90_3_0.8(e4wij)_allsize', 'CE_NT(0.8)'],
    ['ColluEagle_NT_d=0.5_e=0.5_90_3_0.9(e4wij)_allsize', 'CE_NT(0.9)'],
    ['ColluEagle_ZIP_SpEagle_Review2Reviewer_Prior_90_3_0.6(e4wij)_allsize', 'CE_ALL(0.6)'],
    ['ColluEagle_ZIP_SpEagle_Review2Reviewer_Prior_90_3_0.7(e4wij)_allsize', 'CE_ALL(0.7)'],
    ['ColluEagle_ZIP_SpEagle_Review2Reviewer_Prior_90_3_0.8(e4wij)_allsize', 'CE_ALL(0.8)'],
    ['ColluEagle_ZIP_SpEagle_Review2Reviewer_Prior_90_3_0.9(e4wij)_allsize', 'CE_ALL(0.9)'],
    ['speagle_zip_all.txt', 'SpEagle'],
    ['fraudeagle_zip_0.8.txt', 'FraudEagle'],
    ['GSBP_Zip.txt', 'GSBP'],
    ['GSBC_Zip.txt', 'GSBC'],
    ['prior_zip_ALL.txt', 'Prior_ALL'],
    ['prior_zip_NT.txt', 'prior_NT']#,

    # ['ColluEagle_NT_jaccard_0.5_scan_e0.5_90_3_0.6(e4wij)_allsize', 'CE_NT(0.6)'],
    # ['ColluEagle_NT_jaccard_0.5_scan_e0.5_90_3_0.7(e4wij)_allsize', 'CE_NT(0.7)'],
    # ['ColluEagle_NT_jaccard_0.5_scan_e0.5_90_3_0.8(e4wij)_allsize', 'CE_NT(0.8)'],
    # ['ColluEagle_NT_jaccard_0.5_scan_e0.5_90_3_0.9(e4wij)_allsize', 'CE_NT(0.9)'],
    # ['ColluEagle_nyc_reviewfeatures_ALLreviewToreviewer_90_3_0.6(e4wij)_allsize', 'CE_ALL(0.6)'],
    # ['ColluEagle_nyc_reviewfeatures_ALLreviewToreviewer_90_3_0.7(e4wij)_allsize', 'CE_ALL(0.7)'],
    # ['ColluEagle_nyc_reviewfeatures_ALLreviewToreviewer_90_3_0.8(e4wij)_allsize', 'CE_ALL(0.8)'],
    # ['ColluEagle_nyc_reviewfeatures_ALLreviewToreviewer_90_3_0.9(e4wij)_allsize', 'CE_ALL(0.9)'],

    # ['speagle_nyc_ALL.txt', 'SpEagle'],
    # ['fraudeagle_nyc_0.8.txt', 'FraudEagle'],
    # ['GSBP_NYC.txt', 'GSBP'],
    # ['GSBC_NYC.txt', 'GSBC'],
    # ['prior_nyc_ALL.txt', 'ALL'],
    # ['prior_nyc_NT.txt', 'NT']
    # ['random.txt','Random']
    ]

Top = 20000

#alg_color = ['b','purple','orange','pink','cyan']
#alg_lstyle = ['--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', '-',':',':', '--']


#alg_color = ['b','skyblue','purple','orange','pink','cyan','g','springgreen']
#alg_lstyle = ['--','-.','-.', ':', '-', '--', '-.', ':', '-', '--', '-.', '-',':',':', '--']

#alg_color = ['b','b','b','b','skyblue','skyblue','skyblue','skyblue']
#alg_lstyle = ['--','-.','-', ':', '--', '-.', '-', ':']

alg_color = ['b','b','b','b','skyblue','skyblue','skyblue','skyblue',
            'purple','orange','pink','cyan','g','springgreen']
alg_lstyle = ['--','-.','-', ':', '--', '-.', '-', ':',
             '-.', ':', '-', '--', '-.', ':']

#alg_lstyle = ['--','-.','-.', ':', '-', '--', '-.', ':', '-', '--', '-.', '-',':',':', '--']

#alg_marker = ['*', '+', '.', 'o','D', '>', 'P', 'X']
# alg_marker = [None] * 8

#P = len(collueagle_file)  # 算法的个数
#rl_dict = {}  # 输入排序列表
#r_dict = {}  # key= rid, value=[score, label, rij, P+1 positions]