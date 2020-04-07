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


class AIFModel(kfserving.KFModel):  # pylint:disable=c-extension-no-member
    def __init__(self, name: str, predictor_host: str):
        self.name = name
        self.predictor_host = predictor_host
        self.ready = False

    def load(self):
        print("LOADED")
        self.ready = True

    def _predict(self, inputs):
        inputs = np.array(inputs)
        scoring_data = {'instances': inputs.tolist()}

        predictions = self.predict(scoring_data)
        return predictions['predictions']

    def explain(self, request: Dict) -> Dict:
        print("Explaining now")
        instances = request["instances"]

        return {"explanations": {
            "inputs": instances,
        }}
