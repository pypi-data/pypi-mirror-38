#! /usr/bin/env python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Modifications copyright (C) 2017 Common Workflow Langauge.
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup
from sys import version_info

AVRO_VERSION = '1.8.8'

setup(
  name = 'avro-cwl',
  version = AVRO_VERSION,
  packages = ['avro',],
  package_dir = {'avro': 'src/avro'},
  scripts = ["./scripts/avro"],

  package_data={'avro': ['LICENSE', 'NOTICE']},

  # metadata for upload to PyPI
  author = 'Common Workflow Langauge',
  description = 'Avro is a serialization and RPC framework.',
  license = 'Apache License 2.0',
  keywords = 'avro serialization rpc',
  extras_require = {
    'snappy': ['python-snappy'],
  },
  zip_safe=False,
)
