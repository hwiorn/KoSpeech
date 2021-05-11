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

import torch.nn as nn
from typing import Tuple, Optional
from torch import Tensor

from kospeech.models.modules.convolution import MaskConv1d


class JasperSubBlock(nn.Module):
    """
    Jasper sub-block applies the following operations: a 1D-convolution, batch norm, ReLU, and dropout.

    Args:
        in_channels (int): number of channels in the input feature
        out_channels (int): number of channels produced by the convolution
        kernel_size (int): size of the convolving kernel
        stride (int): stride of the convolution. (default: 1)
        dilation (int): spacing between kernel elements. (default: 1)
        padding (int): zero-padding added to both sides of the input. (default: 0)
        bias (bool): if True, adds a learnable bias to the output. (default: False)
        dropout_p (float): probability of dropout
        activation (str): activation function

    Inputs: inputs, input_lengths, residual
        - **inputs**: tensor contains input sequence vector
        - **input_lengths**: tensor contains sequence lengths
        - **residual**: tensor contains residual vector

    Returns: output, output_lengths
        - **output**: tensor contains output sequence vector
        - **output**: tensor contains output sequence lengths
    """
    supported_activations = {
        'hardtanh': nn.Hardtanh(0, 20, inplace=True),
        'relu': nn.ReLU(inplace=True),
        'elu': nn.ELU(inplace=True),
        'leaky_relu': nn.LeakyReLU(inplace=True),
        'gelu': nn.GELU(),
    }

    def __init__(
            self,
            in_channels: int,
            out_channels: int,
            kernel_size: int,
            stride: int = 1,
            dilation: int = 1,
            padding: int = 0,
            bias: bool = False,
            dropout_p: float = 0.2,
            activation: str = 'relu',
    ) -> None:
        super(JasperSubBlock, self).__init__()

        self.conv = MaskConv1d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            bias=bias,
            dilation=dilation,
        )
        self.batch_norm = nn.BatchNorm1d(out_channels, eps=1e-3, momentum=0.1)
        self.activation = self.supported_activations[activation]
        self.dropout = nn.Dropout(p=dropout_p)

    def forward(self, inputs: Tensor, input_lengths: Tensor, residual: Optional[Tensor] = None) -> Tuple[Tensor, Tensor]:
        outputs, output_lengths = self.conv(inputs, input_lengths)
        outputs = self.batch_norm(outputs)

        if residual is not None:
            outputs += residual

        outputs = self.dropout(self.activation(outputs))

        return outputs, output_lengths
