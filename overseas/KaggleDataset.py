import kaggle
import zipfile
from os import listdir
from os.path import exists

from covid_19_au_grab.state_news_releases.overseas.GlobalBase import \
    GlobalBase


class KaggleDataset(GlobalBase):
    def __init__(self, output_dir, dataset):
        GlobalBase.__init__(self, output_dir)
        self.dataset = dataset

    def update(self):
        revision_dir = self.get_today_revision_dir(include_subid=False)
        if exists(revision_dir) and listdir(revision_dir):
            return

        self.client = kaggle.KaggleApi()
        self.client.authenticate()
        self.client.dataset_download_files(self.dataset, revision_dir)

        dataset_name = self.dataset.split('/')[-1]
        with zipfile.ZipFile(f'{revision_dir}/{dataset_name}.zip', 'r') as zip_ref:
            zip_ref.extractall(revision_dir)
