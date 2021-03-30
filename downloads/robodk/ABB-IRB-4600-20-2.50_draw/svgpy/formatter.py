# Copyright (C) 2017 Tetsuya Miura <miute.dev@gmail.com>
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


precision = 6
"""int: The precision is a decimal number indicating how many digits should
be displayed after the decimal point for a floating point value.
The precision must be greater than zero.
"""


def format_number_sequence(s):
    number_sequence = [
        '{:.{precision}f}'.format(
            x, precision=precision).rstrip('0').rstrip('.')
        for x in iter(s)]
    number_sequence = [x if x != '-0' else '0' for x in iter(number_sequence)]
    return number_sequence


def format_coordinate_pair_sequence(s):
    number_sequence = list()
    for x, y in iter(s):
        number_sequence.extend([x, y])
    number_sequence = format_number_sequence(number_sequence)
    coordinate_pair_sequence = list()
    for index in range(0, len(number_sequence), 2):
        coordinate_pair_sequence.append(','.join([number_sequence[index],
                                                  number_sequence[index + 1]]))
    return ' '.join(coordinate_pair_sequence)


def to_coordinate_pair_sequence(s):
    # [1, 2, 3, 4, ...] -> [(1, 2), (3, 4), ...]
    it = iter(s)
    return list(zip(it, it))
