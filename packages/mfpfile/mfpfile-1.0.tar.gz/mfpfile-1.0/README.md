# mfpfile

mfpfile is a module for reading of data files recorded with MFP devices (something like [this](https://www.asylumresearch.com/Products/MFP3DInfinity/MFP3DInfinity.shtml), I think). I am sorry for the lack of comments and documentation. This project is in a very early stage. Instead, you can have a look at the jupyter notebook in the `examples` folder.

# Install

Navigate via command line to the top level directory of this project, and type:
```
$ python setup.py install
```
You should be good to go, and be able to
```
from mfpfile import MFPFile
```
anywhere on your system. To create an `MFPFile` object from file, do:
```
mfp = MFPFile('path/to/file.ibw')
```

# License 

The MIT License (MIT)
Copyright (c) 2018 Ilyas Kuhlemann (ilyasp.ku@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.