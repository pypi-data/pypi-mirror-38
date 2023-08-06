#
# Copyright (c) 2015, Adam Meily <meily.adam@gmail.com>
# Pypsi - https://github.com/ameily/pypsi
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import sys

# To make sure we don't break existing code, we import path_completer here since it used to be
# OS dependent (see issue #)
from pypsi.completers import path_completer

if sys.platform == 'win32':
    from pypsi.os.win32 import *  # pylint: disable=wildcard-import
elif sys.platform in ['cygwin', 'darwin'] or sys.platform.startswith('linux'):
    from pypsi.os.unix import *  # pylint: disable=wildcard-import


__all__ = [
    'find_bins_in_path',
    'is_path_prefix',
    'make_ansi_stream',
    'path_completer'
]
