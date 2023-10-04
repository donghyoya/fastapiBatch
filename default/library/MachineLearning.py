#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pymysql')


# In[37]:


import numpy as np 
import pandas as pd 
from IPython.core.interactiveshell import InteractiveShell
import warnings
from sklearn.model_selection import train_test_split
import xgboost as xgb
import pymysql
from sklearn.metrics import accuracy_score
import math
from datetime import datetime
from datetime import date, timedelta


# 결과 확인을 용이하게 하기 위한 코드

InteractiveShell.ast_node_interactivity = 'all'


pd.options.display.max_columns = 39

# 모든 경고 비활성화
warnings.filterwarnings("ignore")

ddd = pd.read_csv('센서데이터_20220401_라벨링(1).csv')

ddd = ddd[['cSenTime','cSenAccX','cSenAccY','cSenAccZ','cSenGyrX','cSenGyrY','cSenGyrZ','cSenAngX','cSenAngY','cSenAngZ','gpsSpeed','Class']]

ddd = ddd.dropna()

new_column_names = {'Class': 'Label'}
ddd.rename(columns=new_column_names, inplace=True)

# 'Label' 컬럼 값이 134인 행을 제거
ddd= ddd[ddd['Label'] != '유턴(보류)']
ddd= ddd[ddd['Label'] != '유턴']

df_train = pd.read_csv('df_label_1.csv')
df_train


df_train = pd.concat([df_train,ddd],axis=0)

df_train = df_train.reset_index(drop=True)
df_train


# # 데이터 모델링

x_features = df_train.iloc[:,1:11]
y_labels = df_train.iloc[:,-1]
x_train,x_test,y_train,y_test = train_test_split(x_features,y_labels,test_size=0.3,random_state=156)

# 클래스 레이블 매핑
class_mapping = {'직진':0,"우회전":0,'좌회전':0,'정차':0,'급가속':1,'급감속':2,'급정차':3,'급회전':4}

# 클래스 레이블 변환
y_train = [class_mapping[label] for label in y_train]
y_test = [class_mapping[label] for label in y_test]

# XGBoost 모델 초기화 및 원하는 하이퍼파라미터 설정
model = xgb.XGBClassifier(
    objective="multi:softmax",  # 다중 클래스 분류
    num_class=7,               # 클래스 수
    max_depth=7,                # 트리 최대 깊이
    learning_rate=0.06,          # 학습률 (eta)
    n_estimators=700,           # 부스팅 반복 횟수
    eval_metric='mlogloss',     # 평가 지표
    random_state=42             # 랜덤 시드
)

# 모델 학습
model.fit(x_train, y_train)

# 테스트 데이터로 예측
y_pred = model.predict(x_test)

# 정확도 계산
accuracy = accuracy_score(y_test, y_pred)
print('정확도:', accuracy)


# # DB연동하여 데이터 불러오기

# 현재 날짜 가져오기
current_date = date.today()

# 하루 전 날짜 계산
yesterday = current_date - timedelta(days=1)

# 날짜를 원하는 형식으로 출력
#formatted_yesterday = yesterday.strftime("%Y%m%d")
formatted_yesterday = ['20220409']
sql = f"SELECT distinct(cSenID) FROM tb_sensordata_{formatted_yesterday[0]};"
#sql1 = 'SELECT * FROM tb_sensordata_20220401'
cursor.execute(sql)
#cucu.execute(sql1)
cSenID_list = [row[0] for row in cursor.fetchall()]
result = cursor.fetchall()
#result1 = cucu.fetchall()
dfs = []
for y in formatted_yesterday:
    for i in cSenID_list:
        sql1 = f"SELECT * FROM tb_sensordata_{y} WHERE cSenID={i};"
        cucu.execute(sql1)
        result1 = cucu.fetchall()
        new_column_names = [
            'cSenID',
            'cSenDate',
            'cSenTime',
            'cSenType',
            'cSenAccY',
            'cSenAccX',
            'cSenAccZ',
            'cSenGyrY',
            'cSenGyrX',
            'cSenGyrZ',
            'cSenAngY',
            'cSenAngX',
            'cSenAngZ',
            'cSenTemp',
            'gpsLatitude',
            'gpsLongitude',
            'gpsAltitude',
            'gpsSpeed',
            'movingDistance',
            'datelog',
            'riskChkLevel_1',
            'riskChkLevel_2']
        df_t = pd.DataFrame(result1,columns=new_column_names)
        df_t = df_t[['cSenTime','gpsLatitude','gpsLongitude','cSenAccX', 'cSenAccY', 'cSenAccZ', 'cSenGyrX', 'cSenGyrY', 'cSenGyrZ', 'cSenAngX', 'cSenAngY', 'cSenAngZ','gpsSpeed']]
        df_t[['gpsLatitude','gpsLongitude','cSenAccX', 'cSenAccY', 'cSenAccZ', 'cSenGyrX', 'cSenGyrY', 'cSenGyrZ', 'cSenAngX', 'cSenAngY', 'cSenAngZ','gpsSpeed']] = df_t[['gpsLatitude','gpsLongitude','cSenAccX', 'cSenAccY', 'cSenAccZ', 'cSenGyrX', 'cSenGyrY', 'cSenGyrZ', 'cSenAngX', 'cSenAngY', 'cSenAngZ','gpsSpeed']].astype(float)
        dfs.append(df_t)

for i in dfs:
    pred_1 = model.predict(i.iloc[:,3:])
    i['Class'] = pred_1
    


# # 안전점수 도출


def calculate_label_counts(df, label_weights):
    label_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}  # 각 데이터프레임의 label_counts 초기화
    for label in label_counts.keys():
        label_counts[label] += (df['Class'] == label).sum()

    # 레이블별 비율 계산
    total_count = sum(label_counts.values())
    label_ratios = {label: count / total_count for label, count in label_counts.items()}

    # 각 레이블의 점수 계산
    label_scores = {label: ratio * 100 * weight for label, ratio, weight in zip(label_ratios.keys(), label_ratios.values(), label_weights.values())}

    # 최종 운전 점수 계산
    safety_score = min(int(sum(label_scores.values())), 100)  # 최대값을 100으로 제한하고 정수로 내림 처리
    
    return safety_score, label_counts

def calculate_safety_scores(dfs, label_weights):
    all_safety_scores = []  # 모든 데이터프레임의 점수를 저장할 리스트
    all_label_counts = []  # 모든 데이터프레임의 레이블 개수를 저장할 리스트

    for i, df in enumerate(dfs):
        safety_score, label_counts = calculate_label_counts(df, label_weights)
        all_safety_scores.append(safety_score)
        all_label_counts.append(label_counts)
        
        print(f"DataFrame {i+1} Safety Score: {safety_score}")
        print(f"DataFrame {i+1} Label Counts: {label_counts}")

    return all_safety_scores, all_label_counts

# 라벨별 가중치 부여
label_weights = {
    0: 0.9,  # 안전
    1: -0.3,  # 급가속
    2: -0.3,  # 급감속
    3: -0.2,  # 급정거
    4: -0.2   # 급회전
}

# 여러 데이터프레임 생성 (dfs 변수에 저장)

# 함수 호출
all_safety_scores, all_label_counts = calculate_safety_scores(dfs, label_weights)
all_label_counts
all_safety_scores


# # 운전거리 계산

# In[131]:


def remove_zero_coordinates(df):
    return df[(df['gpsLatitude'] != 0) & (df['gpsLongitude'] != 0)]

# 각 데이터프레임에 대해 제거 함수를 적용하고 결과를 새로운 리스트에 저장합니다.
dfs = [remove_zero_coordinates(df) for df in dfs]




# Haversine 공식 함수
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (킬로미터)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# 시간 문자열을 초로 변환하는 함수
def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

# 주행 거리 계산 함수
def calculate_total_distance(df_km, threshold=300):
    total_distance = 0.0
    prev_latitude = None
    prev_longitude = None
    prev_time = None

    for index, row in df_km.iterrows():
        if prev_latitude is not None and prev_longitude is not None:
            if prev_time is not None:
                time_diff = time_to_seconds(row['cSenTime']) - time_to_seconds(prev_time)
                if time_diff > threshold:
                    # 중간에 시간이 5분 이상 끊긴 경우
                    distance_before = haversine(prev_latitude, prev_longitude, row['gpsLatitude'], row['gpsLongitude'])
                    # 끊긴 시간 이후 주행 거리 계산을 위해 이후 데이터의 시작점 설정
                    prev_latitude = row['gpsLatitude']
                    prev_longitude = row['gpsLongitude']
                    prev_time = row['cSenTime']
                    continue  # 끊긴 시간 이전 거리만 누적, 이후 거리 계산을 위해 다음 루프로 건너뜁니다.
                else:
                    # 시간이 연속된 경우 주행 거리 추가 계산
                    distance = haversine(prev_latitude, prev_longitude, row['gpsLatitude'], row['gpsLongitude'])
                    total_distance += distance
            else:
                # 첫 번째 데이터 포인트
                distance_after = 0.0
        prev_latitude = row['gpsLatitude']
        prev_longitude = row['gpsLongitude']
        prev_time = row['cSenTime']

    # 끊긴 시간 이후의 주행 거리 계산
    distance_after = haversine(prev_latitude, prev_longitude, df_km.iloc[-1]['gpsLatitude'], df_km.iloc[-1]['gpsLongitude'])

    # 총 주행 거리 출력
    total_distance += distance_after
    return total_distance

# 여러 데이터프레임에 대한 주행 거리 계산 및 반환
def calculate_total_distances(dfs, threshold=300):
    total_distances = []  # 주행 거리를 저장할 리스트
    for df_km in dfs:
        total_distance = calculate_total_distance(df_km, threshold)
        total_distances.append(total_distance)
    return total_distances


# 함수 호출하여 주행 거리 리스트 반환
total_distances = calculate_total_distances(dfs)

# 각 데이터프레임의 주행 거리 출력
for i, distance in enumerate(total_distances):
    print(f"DataFrame {i+1} 총 주행 거리: {distance} 킬로미터")


# 0 = 안전,
# 1 = 급가속,
# 2 = 급감속,
# 3 = 급정거,
# 4 = 급회전,


ad = []
sublist = []

for item in all_label_counts:
    sublist.extend(item.values())
    if len(sublist) == 5:
        ad.append(sublist)
        sublist = []

print(ad)


# # 데이터타입 변형

# # 상용화용

# In[134]:


# from datetime import datetime

# # 날짜를 문자열로 변환
# yesterday_str = yesterday.strftime("%Y%m%d")

# # 문자열을 날짜(date) 타입으로 변환
# yesterday_date = datetime.strptime(yesterday_str, "%Y%m%d").date()

# # 결과 출력
# print(yesterday_date)


# # 지금용

# In[135]:


cs = datetime.strptime('20220409', "%Y%m%d").date()


# In[136]:


# 모든 요소를 int로 변환
ad_int = [[int(val) for val in sublist] for sublist in ad]

# 결과 확인
print(ad_int)


# In[137]:


# 모든 요소를 float로 변환
all_safety_scores_float = [float(score) for score in all_safety_scores]

# 결과 확인
print(all_safety_scores_float)


# In[138]:


# 모든 요소를 float로 변환
total_distances_float = [float(distance) for distance in total_distances]

# 결과 확인
print(total_distances_float)


# In[139]:


# 문자열을 정수로 변환하여 새로운 리스트 생성
cSenID_int_list = [int(item) for item in cSenID_list]

print(cSenID_int_list)


# In[140]:


a = []
for i in range(len(cSenID_int_list)):
    tpl = (
        cSenID_int_list[i],
        cs,
        ad_int[i][0],
        ad_int[i][1],
        ad_int[i][2],
        ad_int[i][3],
        ad_int[i][4],
        all_safety_scores_float[i],
        total_distances_float[i]
    )
    a.append(tpl)


# # 데이터 적재

# 0 = 안전,
# 1 = 급가속,
# 2 = 급감속,
# 3 = 급정거,
# 4 = 급회전,

# In[141]:


import pymysql

# MySQL 데이터베이스 연결 설정
db = pymysql.connect(
    host="cg.navers.co.kr",
    user="gosafe",
    password="gogosafe0@",
    database="goSafe"
)

# 커서 생성
cursor = db.cursor()

# 데이터베이스에 데이터 적재
try:
    for data in a:
        sql = "INSERT INTO result_safe_score (SenID, Date,safe_driv_cnt,rapid_acc_cnt ,rapid_decel_cnt ,rapid_stop_cnt ,rapid_rot_cnt ,safe_score ,driv_dist  ) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, data)

    db.commit()  # 변경 내용을 데이터베이스에 반영
    print("데이터가 성공적으로 적재되었습니다.")
except Exception as e:
    db.rollback()  # 변경 내용 롤백
    print(f"데이터 적재 중 오류 발생: {str(e)}")
finally:
    cursor.close()  # 커서를 닫습니다.
    db.close()  # 데이터베이스 연결을 닫습니다.


# In[ ]:





# In[ ]:




