import pandas as pd

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
