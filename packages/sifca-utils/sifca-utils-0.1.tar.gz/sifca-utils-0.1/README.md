SIFCA UTILS
===========
A metapackage containing some useful scripts and utilities
for the SIFCA group.

### Installation and usage
Download and install the repository (subtitute YOURUSER by your
CERN user name)
```bash
$ git clone https://YOURUSER@gitlab.cern.ch:8443/sifca/sifca-utils.git
$ cd sifca-utils
$ python setup.py install --user
# Be sure you have your environment variables pointing to the installation
# path ($HOME/.local). You can copy-paste lines below in your .bashrc or
# do it everytime you will use the package
$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/.local/lib
$ export PYTHONPATH=$PYTHONPATH:$HOME/.local/lib
$ export PATH=$PATH:$HOME/.local/bin
# After installation, the package when be used importing it
$ python
import sifca_utils
```


### Contents
#### Modules: *plotting*
Some functions related with the plotting in ROOT. It is
defined the function *get_sifca_style* defining a _ROOT.TStyle_
of publication quality
