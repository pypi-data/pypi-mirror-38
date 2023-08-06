import codecs
import functools
from typing import (Iterable,
                    Optional,
                    TextIO)


def reverse_file(file: TextIO,
                 *,
                 batch_size: Optional[int] = None,
                 lines_separator: Optional[str] = None,
                 keep_lines_separator: bool = True) -> Iterable[str]:
    encoding = file.encoding
    if lines_separator is not None:
        lines_separator = lines_separator.encode(encoding)
    yield from map(functools.partial(codecs.decode,
                                     encoding=encoding),
                   reverse_binary_stream(
                           file.buffer,
                           batch_size=batch_size,
                           lines_separator=lines_separator,
                           keep_lines_separator=keep_lines_separator))
