# Copyright (c) 2021, Soohwan Kim. All rights reserved.
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
# limitations under the License.

from omegaconf import DictConfig
from torch import Tensor
from typing import Tuple

from kospeech.metrics import WordErrorRate, CharacterErrorRate
from kospeech.models.encoder.jasper import JasperEncoder
from kospeech.models.kospeech_model import KospeechEncoderModel
from kospeech.vocabs import KsponSpeechVocabulary
from kospeech.vocabs.vocab import Vocabulary


class JasperModel(KospeechEncoderModel):
    """
    Deep Speech2 model with configurable encoder and decoder.
    Paper: https://arxiv.org/abs/1512.02595
    """
    def __init__(
            self,
            configs: DictConfig,
            num_classes: int,
            vocab: Vocabulary = KsponSpeechVocabulary,
            wer_metric: WordErrorRate = WordErrorRate,
            cer_metric: CharacterErrorRate = CharacterErrorRate,
    ):
        super(JasperModel, self).__init__(configs, num_classes, vocab, wer_metric, cer_metric)

    def build_encoder(self, configs: DictConfig, num_classes: int):
        self.encoder = JasperEncoder(
            num_classes=num_classes,
            version=configs.version,
        )

    def forward(self, inputs: Tensor, input_lengths: Tensor) -> Tuple[Tensor, Tensor]:
        return super(JasperModel, self).forward(inputs, input_lengths)

    def training_step(self, batch: tuple, batch_idx: int) -> Tensor:
        """
        Forward propagate a `inputs` and `targets` pair for training.

        Inputs:
            batch (tuple): A train batch contains `inputs`, `targets`, `input_lengths`, `target_lengths`
            batch_idx (int): The index of batch

        Returns:
            loss (torch.FloatTensor): Loss for training.
        """
        return super(JasperModel, self).training_step(batch, batch_idx)

    def validation_step(self, batch: tuple, batch_idx: int) -> Tensor:
        """
        Forward propagate a `inputs` and `targets` pair for validation.

        Inputs:
            batch (tuple): A train batch contains `inputs`, `targets`, `input_lengths`, `target_lengths`
            batch_idx (int): The index of batch

        Returns:
            loss (torch.FloatTensor): Loss for training.
        """
        return super(JasperModel, self).validation_step(batch, batch_idx)

    def test_step(self, batch: tuple, batch_idx: int) -> Tensor:
        """
        Forward propagate a `inputs` and `targets` pair for test.

        Inputs:
            batch (tuple): A train batch contains `inputs`, `targets`, `input_lengths`, `target_lengths`
            batch_idx (int): The index of batch

        Returns:
            loss (torch.FloatTensor): Loss for training.
        """
        return super(JasperModel, self).test_step(batch, batch_idx)
