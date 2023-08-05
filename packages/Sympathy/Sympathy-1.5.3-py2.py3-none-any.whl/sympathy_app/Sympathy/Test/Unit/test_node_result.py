# Copyright (c) 2013, System Engineering Software Society
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the System Engineering Software Society nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL SYSTEM ENGINEERING SOFTWARE SOCIETY BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import unittest
from sympathy.platform import node_result


class TestNodeResult(unittest.TestCase):

    def setUp(self):
        pass

    def test_node_result(self):
        result = node_result.NodeResult()
        result.stderr = 'I wrote something to stderr'

        d = result.to_dict()
        self.assertTrue(isinstance(d, dict))
        self.assertTrue('stderr' in d)
        r2 = node_result.NodeResult.from_dict(d)
        self.assertEqual(result.stderr, r2.stderr)

        exception_string = 'Not a good value'

        def bad_function():
            raise ValueError(exception_string)

        res = node_result.NodeResult()
        try:
            bad_function()
        except:
            res.store_current_exception()

        self.assertTrue(res.has_error())
        self.assertTrue(res.has_exception())
        self.assertTrue(res.exception.string.find(exception_string) >= 0)


if __name__ == '__main__':
    unittest.main()
