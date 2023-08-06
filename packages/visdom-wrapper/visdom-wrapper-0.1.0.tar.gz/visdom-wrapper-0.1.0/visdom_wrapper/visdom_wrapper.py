# Copyright 2018 Queequeg92.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from visdom import Visdom


class VizWrapper(object):
    _viz = Visdom(port=8097, server="http://localhost")
    _wins = {}

    def __init__(self, name):
        self._name = name
        self._win = None

    def __enter__(self):
        self._check_connection()

        if self._name in self._wins:
            self._win = self._wins[self.name]
        return self

    def update_wins(self, win):
        self._wins[self.name] = win

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_val}')
            print(f'exc_traceback: {exc_tb}')

    def _check_connection(self):
        assert self.viz.check_connection(), \
            'No connection could be formed quickly'

    @property
    def viz(self):
        return self._viz

    @viz.setter
    def viz(self, value):
        if not isinstance(value, Visdom):
            raise ValueError('viz must be an object of class Visdom')
        self._viz = value

    @property
    def name(self):
        return self._name

    @property
    def win(self):
        return self._win