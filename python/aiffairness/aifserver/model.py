# Copyright 2019 kubeflow.org.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict

import kfserving
import numpy as np
import pandas as pd
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.datasets import BinaryLabelDataset


# Temp imports
# TODO: Remove this when we call predictor container directly
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from aif360.algorithms.preprocessing.optim_preproc_helpers.data_preproc_functions import load_preproc_data_german
from aif360.datasets import GermanDataset

np.random.seed(1)
dataset_orig = load_preproc_data_german(['age'])
dataset_orig_train, _ = dataset_orig.split([0.9], shuffle=True)
scale_orig = StandardScaler()
X_train = scale_orig.fit_transform(dataset_orig_train.features)
y_train = dataset_orig_train.labels.ravel()
lmod = LogisticRegression()
lmod.fit(X_train, y_train,
         sample_weight=dataset_orig_train.instance_weights)


class AIFModel(kfserving.KFModel):
    def __init__(self, name: str, predictor_host: str, feature_names: list, label_names: list, favorable_label: float, unfavorable_label: float, privileged_groups: list, unprivileged_groups: list):
        self.name = name
        self.predictor_host = predictor_host
        self.ready = False
        self.feature_names = feature_names
        self.label_names = label_names
        self.favorable_label = favorable_label
        self.unfavorable_label = unfavorable_label
        self.privileged_groups = privileged_groups
        self.unprivileged_groups = unprivileged_groups

    def load(self):
        print("LOADED")
        self.ready = True

    def _predict(self, inputs):
        # TEMP Use german dataset for predictions
        # TODO: call self.predict to make a prediction to the predictor_host parameter
        # predictions = self.predict(scoring_data)
        scale_input = StandardScaler()
        scaled_input = scale_input.fit_transform(inputs)

        predictions = lmod.predict(scaled_input)

        return predictions.tolist()

    def explain(self, request: Dict) -> Dict:
        print("EXPLAINING")
        inputs = request["instances"]
        predictions = self._predict(inputs)

        dataframe_predicted = pd.DataFrame(inputs, columns=self.feature_names)
        dataframe_predicted[self.label_names[0]] = predictions

        dataset_predicted = BinaryLabelDataset(favorable_label=self.favorable_label,
                                               unfavorable_label=self.unfavorable_label,
                                               df=dataframe_predicted,
                                               label_names=self.label_names,
                                               protected_attribute_names=['age'])

        metrics = BinaryLabelDatasetMetric(dataset_predicted,
                                           unprivileged_groups=self.unprivileged_groups,
                                           privileged_groups=self.privileged_groups)

        return {
            "predictions": predictions,
            "metrics": {
                "disparate_impact": metrics.disparate_impact()
            }
        }
