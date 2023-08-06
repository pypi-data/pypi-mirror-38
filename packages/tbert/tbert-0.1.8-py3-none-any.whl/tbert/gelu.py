# The MIT License
# Copyright 2019 Innodata Labs and Mike Kroutikov
#
# PyTorch port of
# https://github.com/google-research/bert/modeling.py
#
# Original code copyright follows:
#
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.import json
#
import torch
import math


def gelu(x):
    '''Gaussian Error Linear Unit - a smooth version of RELU'''
    cdf = 0.5 * (1.0 + torch.erf(x / math.sqrt(2.0)))
    return x * cdf
