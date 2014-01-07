# The MIT License (MIT)
#
# Copyright (c) 2013  Daniel Watkins <daniel@daniel-watkins.co.uk>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the Software), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Fix incorrect pylint import errors of nose.tools.

pylint cannot detect the PEP-8'd assertion functions that nose provides
in nose.tools, which leads to errors about missing imports.  This
pylint plugin fixes that.

Installation Instructions:

1) Put this file somewhere on your PYTHONPATH.
2) Load it using either the --load-plugins command-line option, or
   adding it to the load-plugins setting in your pylintrc.
"""

from logilab.astng import MANAGER
from logilab.astng.builder import ASTNGBuilder

from nose import tools


function_template = """
def {}(*args, **kwargs):
    pass
"""


def nose_transform(module):
    funcs = ''.join(function_template.format(func_name)
                    for func_name in tools.__all__)
    fake = ASTNGBuilder(MANAGER).string_build(funcs)

    for func_name in tools.__all__:
        if func_name not in module.locals:
            module.locals[func_name] = fake[func_name]


def transform(module):
    if module.name == 'nose.tools':
        nose_transform(module)

from logilab.astng import MANAGER
MANAGER.register_transformer(transform)


def register(linter):
    pass
