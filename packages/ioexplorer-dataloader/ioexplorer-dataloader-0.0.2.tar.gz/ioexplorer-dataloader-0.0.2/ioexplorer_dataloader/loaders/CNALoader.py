import pandas as pd
from sqlalchemy import MetaData, Table

from .BaseLoader import BaseLoader
from .common import ingesters

class CNALoader(BaseLoader):
    file_name = ''
    cna_type = ''
    chunksize = 1000000

    def __init__(self, *args, sample_label_to_id=None, **kwargs):
        self.sample_label_to_id = sample_label_to_id
        super(CNALoader, self).__init__(*args, **kwargs)

    def load(self):
        return pd.read_csv(self.path, sep="\t")

    def pre_ingest_transform(self, D):
        melt_ids = {"Hugo_Symbol", "Entrez_Gene_Id"}.intersection(set(D.columns.values))
        D = pd.melt(D, id_vars=melt_ids)
        D.columns = map(lambda x: x.lower(), D.columns.values)
        D.rename(
            columns={
                'variable': 'sampleId',
                'value': self.cna_type
            },
            inplace=True
        )
        D['discrete'] = D['discrete']\
                        .apply(lambda x: x if pd.isnull(x) else str(int(x)))
        return D

    def ingest(self, D):
        ingesters.df_with_progress(D, 'cnas', self.engine, self.chunksize)

class DiscreteCNALoader(CNALoader):
    file_name = 'data_CNA.txt'
    cna_type = 'discrete'

class ContinuousLinearCNALoader(CNALoader):
    file_name = 'data_CNA.txt'
    cna_type = 'continuous_linear'

class ContinuousLog2CNALoader(CNALoader):
    file_name = 'data_CNA.txt'
    cna_type = 'continuous_log2'