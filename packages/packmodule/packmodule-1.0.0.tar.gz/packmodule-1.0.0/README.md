# packmodule

A code packer for Python modules. Designed for use with AWS CloudFormation, which allows
embedding Python code up to 4096 bytes in size directly into a template.

## Usage

Call `packmodule.pack` with a string of your module's source code. The function returns
your code packed with the best performing of zlib, bz2, lzma, and the identity function.
The behavior of your code should not change other than some extra modules being imported.
