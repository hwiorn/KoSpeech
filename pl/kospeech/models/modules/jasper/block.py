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
from torch import Tensor
from typing import Tuple

from kospeech.models.modules.jasper.subblock import JasperSubBlock


class JasperBlock(nn.Module):
    """
    Jasper Block: The Jasper Block consists of R Jasper sub-block.

    Args:
        num_sub_blocks (int): number of sub block
        in_channels (int): number of channels in the input feature
        out_channels (int): number of channels produced by the convolution
        kernel_size (int): size of the convolving kernel
        stride (int): stride of the convolution. (default: 1)
        dilation (int): spacing between kernel elements. (default: 1)
        bias (bool): if True, adds a learnable bias to the output. (default: True)
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
    def __init__(
            self,
            num_sub_blocks: int,
            in_channels: int,
            out_channels: int,
            kernel_size: int,
            stride: int = 1,
            dilation: int = 1,
            bias: bool = True,
            dropout_p: float = 0.2,
            activation: str = 'relu',
    ) -> None:
        super(JasperBlock, self).__init__()
        padding = self._get_same_padding(kernel_size, stride, dilation)
        self.layers = nn.ModuleList([
            JasperSubBlock(
                in_channels=in_channels if i == 0 else out_channels,
                out_channels=out_channels,
                kernel_size=kernel_size,
                stride=stride,
                dilation=dilation,
                padding=padding,
                bias=bias,
                dropout_p=dropout_p,
                activation=activation,
            ) for i in range(num_sub_blocks)
        ])

    def _get_same_padding(self, kernel_size: int, stride: int, dilation: int):
        if stride > 1 and dilation > 1:
            raise ValueError("Only stride OR dilation may be greater than 1")
        return (kernel_size // 2) * dilation

    def forward(self, inputs: Tensor, input_lengths: Tensor, residual: Tensor) -> Tuple[Tensor, Tensor]:
        for layer in self.layers[:-1]:
            inputs, input_lengths = layer(inputs, input_lengths)

        outputs, output_lengths = self.layers[-1](inputs, input_lengths, residual)

        return outputs, output_lengths
