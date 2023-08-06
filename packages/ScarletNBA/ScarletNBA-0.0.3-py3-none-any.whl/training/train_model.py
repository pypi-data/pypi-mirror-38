import argparse
from datetime import datetime
import pandas as pd
import numpy as np

#model selection
from sklearn.model_selection import train_test_split

#models
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor

#model evaluation
from sklearn.metrics import mean_squared_error
from math import sqrt

#training utils
from training_utils import model_bakeoff, deploy_pickle

class TrainModel:
    def __init__(self, project, bucket, destination_path, season, partition_date):
        self.project = project
        self.bucket = bucket
        self.destination_path = destination_path
        self.season = season
        self.partition_date = partition_date

    @property
    def get_partition_date(self):
        if not self.partition_date:
            self.partition_date = datetime.today().strftime("%Y%m%d")
            return self.partition_date
        else:
            return self.partition_date

    def train(self):
        project = self.project
        query = 'select * from `{project}.basketball.training{season}_{partition_date}`'.format(project=self.project,
                                                                                                season= self.season,
                                                                                                partition_date=self.get_partition_date)
        df = pd.read_gbq(query=query, project_id=project, dialect="standard", verbose=False)
        training = df.drop(["bbrefID", "player", "date"], axis=1).dropna()

        #Basic Linear Model
        lm = linear_model.LinearRegression(normalize=True)
        ridge_lm = linear_model.Ridge(alpha=0.5)
        lasso_lm = linear_model.Lasso(alpha = 0.1)
        rfreg = RandomForestRegressor()

        lm_model = model_bakeoff(model=lm,
                  df=training,
                  dependent_var="dk",
                  test_size=0.3)

        ridge_model = model_bakeoff(model=ridge_lm,
                  df=training,
                  dependent_var="dk",
                  test_size=0.3)

        lasso_model = model_bakeoff(model=lasso_lm,
                  df=training,
                  dependent_var="dk",
                  test_size=0.3)

        rf_model = model_bakeoff(model=rfreg,
                  df=training,
                  dependent_var="dk",
                  test_size=0.3)

        return ridge_model

    def run(self):
        train_obj = self.train()

        deploy_pickle(obj=train_obj['model'],
                      project_id=self.project,
                      bucket=self.bucket,
                      destination_path=self.destination_path,
                      filename='model')

        deploy_pickle(obj=train_obj['preprocessing'],
                      project_id=self.project,
                      bucket=self.bucket,
                      destination_path=self.destination_path,
                      filename='preprocessing')

def main(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--project',
                        dest='project',
                        default = None,
                        help='This is the GCP project you wish to send the data')
    parser.add_argument('--bucket',
                        dest='bucket',
                        default = 'draftkings',
                        help='bucket to store train')
    parser.add_argument('--destination_path',
                        dest='destination_path',
                        default = 'nba_models',
                        help='This is the sport type (for now)')
    parser.add_argument('--season',
                        dest='season',
                        default = '2019',
                        help='This is the sport type (for now)')
    parser.add_argument('--partition_date',
                        dest='partition_date',
                        default = None,
                        help='partition date of data collection')

    args, _ = parser.parse_known_args(argv)

    train_pipeline = TrainModel(project=args.project,
                                bucket=args.bucket,
                                destination_path=args.destination_path,
                                season=args.season,
                                partition_date=args.partition_date)

    train_pipeline.run()

if __name__ == '__main__':
    main()
