import numpy as np
from Constans.constans import DATA_DIRECTORY
import pandas as pd
from pathlib import Path
from datetime import datetime


class DataLoader:
    _instance = None
    _file_content = None
    _dataPath = None
    _providersLabels = None
    _providersPaths = None
    _datasets = None

    def __new__(cls, file_path=None):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._dataPath = Path(DATA_DIRECTORY)
            cls._providersLabels = cls._computeProvidersLabels(cls._dataPath)
            cls._providersPaths = cls._computeProvidersPaths(cls._dataPath, cls._providersLabels)
            cls._datasets = cls._loadDataSets(cls._providersPaths)

        return cls._instance

    @staticmethod
    def _computeProvidersLabels(dataPath: Path) -> list:
        return [provider.name for provider in dataPath.iterdir() if provider.is_dir()]

    @staticmethod
    def _computeProvidersPaths(dataPath: Path, providersLabels: list) -> dict:
        return {label: (dataPath.joinpath(label)) for label in providersLabels}

    @staticmethod
    def _loadDataSets(providersPaths: dict) -> dict:
        print("DUPAAA")
        def loadDataSetsForProvider(providerPath: Path) -> dict:
            dataframes = {}
            for file in providerPath.glob('*.csv'):
                df = pd.read_csv(file)
                fileWithNoExtension = file.stem
                dataframes[fileWithNoExtension] = df

            return dataframes

        dataPerProviders = {}
        for label, path in providersPaths.items():
            dataPerProviders[label] = loadDataSetsForProvider(path)

        return dataPerProviders

    def getProvidersLabels(self) -> list:
        return self._providersLabels

    def getProvidersPaths(self) -> dict:
        return self._providersPaths

    def getDatasets(self) -> dict:
        return self._datasets

    def getCount(self, data_dict: dict, dateRange: list) -> pd.DataFrame:
        startDate = dateRange[0]
        stopDate = dateRange[1]

        contsDict = {date_str: wartosc.shape[0] for date_str, wartosc in data_dict.items()
                     if startDate <= datetime.strptime(date_str, '%d-%m-%Y').date() <= stopDate}

        df = pd.DataFrame(list(contsDict.items()), columns=['Data', 'count'])
        df['Data'] = pd.to_datetime(df['Data'], format='%d-%m-%Y')
        df = df.sort_values(by='Data')

        return df

    def getOffersCount(self, dataProvider: str, dateRange: list) -> pd.DataFrame:
        providerDatasets = self.getDatasets().get(dataProvider)

        return self.getCount(providerDatasets, dateRange)

    def getOffersCountPerCategory(self, dataProvider: str, category: str, dateRange: list):
        providerDatasets = self.getDatasets().get(dataProvider)

        filtered_providerDatasets = {}
        for key, df in providerDatasets.items():
            filtered_df = df[df['Category'].str.upper() == category]

            if not filtered_df.empty:
                filtered_providerDatasets[key] = filtered_df

        return self.getCount(filtered_providerDatasets, dateRange)

    def getOffersCountPerRequirement(self, dataProvider: str, requirement: str, dateRange: list):
        providerDatasets = self.getDatasets().get(dataProvider)

        filtered_providerDatasets = {}
        for key, df in providerDatasets.items():
            x = df[df['Requirements'].apply(
                lambda x: requirement.upper() in list(str(x).strip().upper()[1:-1].split('" "')) if pd.notnull(
                    x) else False)]
            y = df[df['Optionals'].apply(
                lambda x: requirement.upper() in list(str(x).strip().upper()[1:-1].split('" "')) if pd.notnull(
                    x) else False)]

            if not x.empty and not y.empty:
                temp = pd.concat([x, y], ignore_index=True)
                filtered_providerDatasets[key] = temp

        return self.getCount(filtered_providerDatasets, dateRange)

    def getOffersCountPerLevel(self, dataProvider: str,level: str, dateRange: list):
        providerDatasets = self.getDatasets().get(dataProvider)

        filtered_providerDatasets = {}
        for key, df in providerDatasets.items():
            filtered_df = df[df['Level'].str.lower() == level.lower()]

            if not filtered_df.empty:
                filtered_providerDatasets[key] = filtered_df

        return self.getCount(filtered_providerDatasets, dateRange)


    def getOffersCountPerOperationMode(self, dataProvider: str,mode: str, dateRange: list):
        providerDatasets = self.getDatasets().get(dataProvider)
        filtered_providerDatasets = {}

        for key, df in providerDatasets.items():
            filtered_df = df[df['OperationMode'].str.lower() == mode.lower()]

            if not filtered_df.empty:
                filtered_providerDatasets[key] = filtered_df

        total=[]
        for key,value in self.getCount(providerDatasets, dateRange).values:
            total.append(value)

        df2 = self.getCount(filtered_providerDatasets, dateRange).assign(Total=total)
        df2['Ratio'] = df2.apply(lambda row: round(row['count'] / row['Total'] * 100,2), axis=1)

        return df2


    def getOffersCountPerOperationMode2(self, dataProvider: str,isRemote: bool, dateRange: list):
        providerDatasets = self.getDatasets().get(dataProvider)
        filtered_providerDatasets = {}


        for key, df in providerDatasets.items():
            if isRemote:
                filtered_df = df[df['Location'].str.lower() == "remote"]
            else:
                filtered_df = df[df['Location'].str.lower() != "remote"]

            if not filtered_df.empty:
                filtered_providerDatasets[key] = filtered_df


        total=[]
        for key,value in self.getCount(providerDatasets, dateRange).values:
            total.append(value)

        df2 = self.getCount(filtered_providerDatasets, dateRange).assign(Total=total)
        df2['Ratio'] = df2.apply(lambda row: round(row['count'] / row['Total'] * 100,2), axis=1)

        return df2

    def transform_dataframe(self, df, date_value):
        new_df = df[df['UOP'].notna() & df['UOP'].str.contains('PLN')][['UOP', 'Level']]
        new_df['Date'] = pd.to_datetime(date_value, format='%d-%m-%Y')

        def process_uop(uop):
            parts = uop.replace('  ', ' ').split()
            if '-' in parts:
                zero_index = float(parts[0]) if parts[0] != '-' else 0
                second_index = float(parts[2]) if len(parts) > 2 and parts[2] != '-' else 0
                return (zero_index + second_index) / 2
            else:
                return float(parts[0])

        new_df['UOP'] = new_df['UOP'].apply(process_uop)

        return new_df

    def combine_dataframes(self, provider):
        providerDatasets = self.getDatasets().get(provider)

        transformed_dfs = []

        for key, df in providerDatasets.items():
            transformed_dfs.append(self.transform_dataframe(df, key))

        combined_df = pd.concat(transformed_dfs, ignore_index=True)
        grouped_median = combined_df.groupby(['Date', 'Level']).median().reset_index()
        grouped_median = grouped_median.sort_values(by='Date')

        return grouped_median
