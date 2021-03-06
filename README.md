# PsyParse

PsyParse provides code to deal with parsing log files generated by
[PsychoPy](www.psychopy.org). You may find PsyParse useful for doing
things like generating CSV dataframes from the default sequential
logfiles generated by [PsychoPy](www.psychopy.org).

## Author

**Travis Nesland** :: <tnesland@gmail.com>

## Version

**0.11** :: Project currently in alpha release and should be considered exerimental

## Requirements

* [git](http://git-scm.com/)
* [python](http://www.python.org/)

## Installation

Assuming you have met the above requirements:

```shell
cd <some directory>
git clone https://github.com/tnez/PsyParse.git
cd PsyParse
sudo python setup.py install
```

To check that the installation worked, open a terminal and try the
following::

```shell
ipython
```

Wait for ipython to load...

```python
import psyparse
psyparse.available_classes()
```

If the installation worked, you should see a list of available
classes.

## Usage

[Sample Use Case](http://tnez.github.io/PsyParse/examples/sample_usage.pdf)
