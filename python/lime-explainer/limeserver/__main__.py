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

import argparse
import kfserving

from limeserver import LIMEModel

DEFAULT_MODEL_NAME = "limeserver"
DEFAULT_MODEL_CLASS_NAME = "LIMEModel"
DEFAULT_NUM_SAMPLES = "1000"
DEFAULT_SEGMENTATION_ALGORITHM = "quickshift"
DEFAULT_TOP_LABELS = "10"
DEFAULT_FLATTENED_SIZE = "0"
DEFAULT_MIN_WEIGHT = "0.01"
DEFAULT_POSITIVE_ONLY = "true"
# The required parameters are num_classes and predictor_host                                

parser = argparse.ArgumentParser(parents=[kfserving.kfserver.parser])
parser.add_argument('--model_name', default=DEFAULT_MODEL_NAME,
                    help='The name that the model is served under.')
parser.add_argument('--model_class_name', default=DEFAULT_MODEL_CLASS_NAME,
                    help='The class name for the model.')
parser.add_argument('--num_samples', default=DEFAULT_NUM_SAMPLES,
                    help='The number of samples the explainer is allowed to take')
parser.add_argument('--segmentation_algorithm', default=DEFAULT_SEGMENTATION_ALGORITHM,
                    help='The algorithm used for segmentation.')
parser.add_argument('--top_labels', default=DEFAULT_TOP_LABELS,
                    help='The number of most likely classifications to return.')
parser.add_argument('--flattened_size', default=DEFAULT_FLATTENED_SIZE,
                    help='The size of the flattened input or 0 if it shouldn\'t be flattened.')
parser.add_argument('--min_weight', default=DEFAULT_MIN_WEIGHT,
                    help='The minimum weight needed by a pixel to be considered useful as an explanation.')
parser.add_argument('--positive_only', default=DEFAULT_POSITIVE_ONLY,
                    help='Whether or not to show only the explanations that positively indicate a classification')

parser.add_argument('--predictor_host', help='The host for the predictor', required=True)
args, _ = parser.parse_known_args()

if __name__ == "__main__":
    model = LIMEModel(name=args.model_name, flattened_size=args.flattened_size, predictor_host=args.predictor_host, 
                        segm_alg=args.segmentation_algorithm, num_samples=args.num_samples, 
                        top_labels=args.top_labels, min_weight=args.min_weight, positive_only=args.positive_only)
    model.load()
    kfserving.KFServer().start([model])