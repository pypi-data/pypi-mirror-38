# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Synthtool synthesizes libraries from disparate sources."""

from synthtool.transforms import move, replace
from synthtool import log
from synthtool import update_check

copy = move

__all__ = ["copy", "move", "replace"]

# check for updates, if needed.
update_check.check_for_updates("gcp-synthtool", print=log.critical)
