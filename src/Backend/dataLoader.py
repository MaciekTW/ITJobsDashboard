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
            print("Hello")

        return cls._instance

    @staticmethod
    def _computeProvidersLabels(dataPath: Path) -> list:
        return [provider.name for provider in dataPath.iterdir() if provider.is_dir()]

    @staticmethod
    def _computeProvidersPaths(dataPath: Path, providersLabels: list) -> dict:
        return {label: (dataPath.joinpath(label)) for label in providersLabels}

    @staticmethod
    def _loadDataSets(providersPaths : dict) -> dict:

        def loadDataSetsForProvider(providerPath : Path) -> dict:
            dataframes = {}
            for file in providerPath.glob('*.csv'):
                df = pd.read_csv(file)
                fileWithNoExtension = file.stem
                dataframes[fileWithNoExtension] = df

            return dataframes

        dataPerProviders = {}
        for label,path in providersPaths.items():
            dataPerProviders[label] = loadDataSetsForProvider(path)

        return dataPerProviders

    def getProvidersLabels(self) -> list:
        return self._providersLabels

    def getProvidersPaths(self) -> dict:
        return self._providersPaths

    def getDatasets(self) -> dict:
        return self._datasets

    def getCount(self, data: dict, dateRange:list) -> pd.DataFrame:
        startDate =dateRange[0]
        stopDate= dateRange[1]

        contsDict = {data: wartosc.shape[0] for data, wartosc in data.items()
                     if startDate <= datetime.strptime(data, '%d-%m-%Y').date()  <= stopDate}

        df = pd.DataFrame(list(contsDict.items()), columns=['Data', 'count'])
        df['Data'] = pd.to_datetime(df['Data'], format='%d-%m-%Y')
        df = df.sort_values(by='Data')

        return df

    def getOffersCount(self,dataProvider: str, dateRange:list) -> pd.DataFrame:
        providerDatasets=self.getDatasets().get(dataProvider)

        return  self.getCount(providerDatasets,dateRange)


    def getOffersCountPerCategory(self,dataProvider: str, category: str, dateRange:list):
        providerDatasets=self.getDatasets().get(dataProvider)


        for data,wartosc in providerDatasets.items():
            print(str(wartosc["Category"]))

        filtered_providerDatasets = {}
        for key, df in providerDatasets.items():
            filtered_df = df[df['Category'].str.upper() == 'AI']

            if not filtered_df.empty:
                filtered_providerDatasets[key] = filtered_df

        return self.getCount(filtered_providerDatasets,dateRange)


    def getOffersCountPerRequirement(self,dataProvider: str, requirement: str):
        pass