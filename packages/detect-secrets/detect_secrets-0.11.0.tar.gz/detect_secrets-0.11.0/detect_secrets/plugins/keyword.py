"""
This code was extracted in part from
https://github.com/PyCQA/bandit. Using similar heuristic logic,
we adapted it to fit our plugin infrastructure, to create an organized,
concerted effort in detecting all type of secrets in code.

Copyright (c) 2014 Hewlett-Packard Development Company, L.P.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from __future__ import absolute_import

from .base import BasePlugin
from detect_secrets.core.potential_secret import PotentialSecret
from detect_secrets.plugins.core.constants import WHITELIST_REGEX


BLACKLIST = (
    # NOTE all values here should be lowercase,
    # otherwise _secret_generator can fail to match them
    'pass =',
    'password',
    'passwd',
    'pwd',
    'secret',
    'secrete',
    'token',
)


class KeywordDetector(BasePlugin):
    """This checks if blacklisted keywords
    are present in the analyzed string.
    """

    secret_type = 'Password'

    def analyze_string(self, string, line_num, filename):
        output = {}

        if WHITELIST_REGEX.search(string):
            return output

        for identifier in self.secret_generator(string):
            secret = PotentialSecret(
                self.secret_type,
                filename,
                identifier,
                line_num,
            )
            output[secret] = secret

        return output

    def _secret_generator(self, lowercase_string):
        for line in BLACKLIST:
            if line in lowercase_string:
                yield line

    def secret_generator(self, string):
        return self._secret_generator(string.lower())
