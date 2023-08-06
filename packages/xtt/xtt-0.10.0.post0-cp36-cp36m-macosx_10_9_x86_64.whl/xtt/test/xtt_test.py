# Copyright 2018 Xaptum, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License

from __future__ import absolute_import
from __future__ import print_function

import unittest
import xtt

class TestReturnCodes(unittest.TestCase):

    def test_error_string(self):
        string = xtt.error_string(0)
        self.assertEqual(string, "XTT - SUCCESS")

class TestCrypto(unittest.TestCase):

    def test_create_ecdsap256_key_pair(self):
        (pub, priv) = xtt.crypto.create_ecdsap256_key_pair()
        self.assertEqual(len(pub.data), 65)
        self.assertEqual(len(priv.data), 32)

if __name__ == "__main__":
    unittest.main()
