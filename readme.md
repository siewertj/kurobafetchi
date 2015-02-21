# Kurobafetchi

18 Feb 2015

## Introduction
Kurobafetchi is a program that allows batch downloading of images from 4chan through the command line. It was partly a foray into web scrapping with python. My goal was to make this as lightweight (ie least amount of external libraries) as possible.



## Versioning
I will be following the [Semantic Versioning](http://semver.org/) scheme laid out by mr Preston-Werner as closely as possible.


## Installing
To grab the latest build from github, make sure you have pip and setuptools installed.Then in your console of choice, type in

```bash
pip install git+https://github.com/siewertj/kurobafetchi
```

This will download to a temp folder, create an egg, and then install with setuptools. It can be uninstalled with

```bash
pip uninstall
```


## Running
The name of the script installed is 'fetchi.py'. So assuming that your Path variable is setup correctly, you can do a

```bash
fetchi.py -h
```

to see the help menu. The Path needs to be looking in '/bin' or '/usr/bin' for linux and '[PYTHON INSTALL]/Scripts' for windows, where [PYTHON INSTALL] is your python install directory (I think it's 'C:\\Python34' by default).

It is unlikely that I will add a config file unless things become more complicated so to avoid having to specify the directory every time you may want to consider adding an alias. This can be done in both Bash and Powershell (so linux and windows). By default the current working directory is where everything will get rooted.