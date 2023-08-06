"""
Python code packer for AWS Lambda, trading cold start latency for size.
Mostly useful for inline code in CloudFormation templates.
"""

import base64
import bz2
import functools
import lzma
import re
import zlib
from typing import Optional

__all__ = ["pack"]

ALGORITHMS = [
    (functools.partial(bz2.compress, compresslevel=9), bz2.decompress),
    (functools.partial(zlib.compress, level=9), zlib.decompress),
    (
        functools.partial(
            lzma.compress, format=lzma.FORMAT_ALONE, preset=lzma.PRESET_EXTREME | 9
        ),
        lzma.decompress,
    ),
]

PACK_TEMPLATE = (
    "import {imports},{module};"
    + "exec({module}.{decompressor}(base64.b85decode('{encoded}')))"
)


def pack(source: str, *, include_cfnresponse: Optional[bool] = None):
    if include_cfnresponse is None:
        # if CloudFormation detects an import of `cfnresponse`, it'll add that
        # module to your Lambda environment automatically.
        # this regex roughly matches CloudFormation's detection logic.
        include_cfnresponse = bool(
            re.search(r"^\s*import\s+cfnresponse", source, re.MULTILINE)
        )
    attempts = [("import cfnresponse\n" if include_cfnresponse else "") + source]
    imports = (["cfnresponse"] if include_cfnresponse else []) + ["base64"]
    for compressor, decompressor in ALGORITHMS:
        compressed = compressor(source.encode("utf-8"))
        packed = PACK_TEMPLATE.format(
            imports=",".join(imports),
            module=decompressor.__module__,
            decompressor=decompressor.__name__,
            encoded=base64.b85encode(compressed).decode("utf-8"),
        )
        attempts.append(packed)
    return sorted(attempts, key=len)[0]
