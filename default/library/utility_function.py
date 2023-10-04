import math
from datetime import date, timedelta

'''
remove_zero_coordinates: GPS 좌표에서 0 값을 제거합니다.
haversine: 두 지점 간의 거리를 계산합니다.
time_to_seconds: 시간 문자열을 초로 변환합니다.
calculate_total_distance: 주어진 데이터 프레임의 주행 거리를 계산합니다.
'''

def haversine(lat1, lon1, lat2, lon2):
    """ 
    Haversine 공식을 사용하여 두 지점 간의 거리를 계산합니다.
    """
    R = 6371  # 지구 반지름 (킬로미터)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def time_to_seconds(time_str):
    """ 
    시간 문자열을 초로 변환합니다.
    """
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def get_previous_date(current_date=None, days=1):
    """ 
    주어진 날짜로부터 n 일 전의 날짜를 반환합니다.
    """
    if current_date is None:
        current_date = date.today()
    previous_date = current_date - timedelta(days=days)
    return previous_date

def class_mapping(y):
    """
    문자열 레이블을 숫자 레이블로 매핑합니다.
    """
    mapping = {'직진': 0, "우회전": 0, '좌회전': 0, '정차': 0, '급가속': 1, '급감속': 2, '급정차': 3, '급회전': 4}
    return [mapping[label] for label in y]

def calculate_safety_score(label_counts, label_weights):
    """
    레이블 개수와 레이블 가중치를 사용하여 안전 점수를 계산합니다.
    """
    label_ratios = {label: count / sum(label_counts.values()) for label, count in label_counts.items()}
    label_scores = {label: ratio * 100 * weight for label, ratio, weight in zip(label_ratios.keys(), label_ratios.values(), label_weights.values())}
    safety_score = min(int(sum(label_scores.values())), 100)
    return safety_score
