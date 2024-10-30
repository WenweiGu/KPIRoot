import pandas as pd
import os
import statsmodels.tools.sm_exceptions
from preprocess import Align
from sklearn.preprocessing import MinMaxScaler
from features import RFeatures, SAXFeatures
from sklearn.metrics import jaccard_score
from statsmodels.tsa.stattools import grangercausalitytests
from sklearn.metrics import f1_score
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

dataset_num = '1'
data_dir = f'./dataset{dataset_num}/'
instance_names = []
for root, dirs, files in os.walk(data_dir):
    for directory in dirs:
        instance_names.append(directory)

for instance_name in instance_names:
    start = time.time()
    if instance_name == 'label':
        break
    data_dir = f'./dataset{dataset_num}/{instance_name}'
    label_dir = f'./dataset{dataset_num}/label/{instance_name}_label.csv'
    label = pd.read_csv(f'{label_dir}')
    correlated = list(label['names'])
    k = 10
    n = label['labels'][label['labels'] == 1].count()
    correlation_scores = dict()

    # 增加
    for kpi in correlated:
        alarm_kpi = pd.read_csv(f'{data_dir}/origin_data.csv')
        correlation_kpi = pd.read_csv(f'{data_dir}/{kpi}')
        aligned = Align().realign_online(alarm_kpi, correlation_kpi)
        R_interval = RFeatures(5, 1.5, 0).get_rSegments(aligned.iloc[:, 0])

        similarity_score = 0
        causality_score = 0

        for interval in R_interval:
            alarm_kpi = aligned.iloc[:, 0][interval[0]: interval[1]]  # 定位区间
            correlation_kpi = aligned.iloc[:, 1][interval[0]: interval[1]]

            sax_bin = 26
            sax_alarm = SAXFeatures(sax_bin).sax_transform(alarm_kpi).flatten()
            sax_kpi = SAXFeatures(sax_bin).sax_transform(correlation_kpi).flatten()

            # encoding
            sax_alarm = [ord(ele) - ord('a') for ele in sax_alarm]
            sax_kpi = [ord(ele) - ord('a') for ele in sax_kpi]

            similarity_score += jaccard_score(sax_alarm, sax_kpi, average='weighted')

            granger_data = pd.concat([alarm_kpi, correlation_kpi], axis=1)
            granger_normalize = MinMaxScaler().fit_transform(granger_data)

            try:
                granger = grangercausalitytests(pd.DataFrame(granger_data), maxlag=1, verbose=False)
                p = granger[1][0]['lrtest'][0]
                causality_score += p
            except statsmodels.tools.sm_exceptions.InfeasibleTestError:
                continue

        if dataset_num != '3':
            similarity_score /= len(R_interval)
            causality_score /= len(R_interval)

        correlation_score = 1 * similarity_score + 0.1 * causality_score
        correlation_scores[kpi] = correlation_score

    end = time.time()
    print(end-start)

    threshold = sorted(correlation_scores.values())[-k]
    threshold_f1 = sorted(correlation_scores.values())[-n]

    predict = pd.DataFrame(columns=['names', 'predicts', 'predicts_f1'])
    predict['names'], predict['predicts'], predict['predicts_f1'] = \
        correlation_scores.keys(), correlation_scores.values(), correlation_scores.values()
    predict['predicts'] = predict['predicts'] >= threshold
    predict['predicts'] = predict['predicts'].astype('int')
    predict['predicts_f1'] = predict['predicts_f1'] >= threshold_f1
    predict['predicts_f1'] = predict['predicts_f1'].astype('int')

    result = pd.merge(label, predict, on='names')
    f1 = f1_score(result['predicts_f1'], result['labels'])
    # print(instance_name)
    # print(result)

    # hit rate直接算
    hit = result[(result['predicts'] == 1) & (result['labels']) == 1].shape[0] / n
    print(f1, hit)
