import pandas as pd

'''
DataPreparation 클래스에는 다음과 같은 메서드들이 있습니다:

rename_columns: 주어진 컬럼명 매핑을 사용하여 컬럼명을 바꾼다.
drop_na: NaN 값을 포함하는 행을 삭제한다.
filter_rows_by_label: 주어진 레이블 리스트에 있는 레이블을 가진 행을 삭제한다.
reset_index: 데이터프레임의 인덱스를 재설정한다.
concat_dataframes: 주어진 데이터프레임을 현재 데이터프레임에 연결한다.
get_preprocessed_data: 전처리된 데이터를 반환한다.
'''


class DataPreparation:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def rename_columns(self, column_mapping):
        self.data.rename(columns=column_mapping, inplace=True)
        return self.data

    def drop_na(self):
        self.data = self.data.dropna()
        return self.data

    def filter_rows_by_label(self, labels_to_remove):
        for label in labels_to_remove:
            self.data = self.data[self.data['Label'] != label]
        return self.data

    def reset_index(self):
        self.data = self.data.reset_index(drop=True)
        return self.data

    def concat_dataframes(self, df_to_concat):
        self.data = pd.concat([self.data, df_to_concat], axis=0)
        return self.data

    def get_preprocessed_data(self):
        return self.data
