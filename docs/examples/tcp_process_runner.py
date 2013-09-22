# Licensed to Tomaz Muraus under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# Tomaz muraus licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys

from glob import glob
from os.path import splitext, basename, join as pjoin
from distutils.core import Command
from unittest import TextTestRunner, TestLoader

TEST_PATHS = ['tests']


class TestCommand(Command):
    description = 'run test suite'
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        self._run_mock_api_server()
        status = self._run_tests()
        sys.exit(status)

    def _run_tests(self):
        testfiles = []
        for test_path in TEST_PATHS:
            test_files = glob(pjoin(self._dir, test_path, 'test_*.py'))
            for t in test_files:
                module_path = '.'.join([test_path.replace('/', '.'),
                                        splitext(basename(t))[0]])
                testfiles.append(module_path)

        tests = TestLoader().loadTestsFromNames(testfiles)

        t = TextTestRunner(verbosity=2)
        res = t.run(tests)
        return not res.wasSuccessful()

    def _run_mock_api_server(self):
        from test_utils.process_runners import TCPProcessRunner

        script = pjoin(os.path.dirname(__file__), 'tests/mock_http_server.py')

        for port in [8881, 8882, 8883]:
            args = [script, '--port=%s' % (port)]
            log_path = 'mock_api_server_%s.log' % (port)
            wait_for_address = ('127.0.0.1', port)
            server = TCPProcessRunner(args=args,
                                      wait_for_address=wait_for_address,
                                      log_path=log_path)
            server.setUp()
