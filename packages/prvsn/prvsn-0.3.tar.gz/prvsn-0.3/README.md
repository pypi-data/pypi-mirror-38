Prvsn
=================

`prvsn` is a simple provisioning tool.

It can provision linux and mac, either locally or remotely. 

[![Build](https://travis-ci.org/acoomans/prvsn.svg?branch=master)](https://travis-ci.org/acoomans/prvsn)
[![Pypi version](http://img.shields.io/pypi/v/prvsn.svg)](https://pypi.python.org/pypi/prvsn)
[![Pypi license](http://img.shields.io/pypi/l/prvsn.svg)](https://pypi.python.org/pypi/prvsn)
![Python 2](http://img.shields.io/badge/python-2-blue.svg)
![Python 3](http://img.shields.io/badge/python-3-blue.svg)

![Screenshot](documentation/screenshot.png)


## Motivation

The motivation for this tool is too keep track of configuration steps and being able to rebuild a small setup (e.g. a raspberry pi) quickly and with minimal effort.

### Goals

Easy for quickly setup a machine for hacking:

- easy to provision a single machine
- works in python
- simple way to
    - add a file, possibly a template
    - install package
    - run a command in bash
- works out of the box:
    - python 2.7 & 3 compatibility
    - no external dependencies

### Non-Goals

Large scale provisioning:

- provision thousands or more machines
- strict dependencies, complex dependency graph
- external recipes & supermarket/store support

If those are your goals, have a look at Puppet or Chef or others.


## Installation

### Install

From PyPi:

    pip install prvsn
   
From Github:

    git clone git@github.com:acoomans/prvsn.git
    cd prvsn
	python setup.py install

Or for development:

	python setup.py develop


## Usage

### Hierarchy

Configurations are called `roles` and are grouped into a `runbook`.

The file hierarchy looks like:

	runbook
	|- roles
	   |- web
	   |- ...
	   |- desktop
	      |- main.py
	      |- files


- `main.py` is the main python entry point
- `files` is to contain any files you want to use

### Tasks

A role's `main.py` can contain one or more `tasks` (also called `states` since they're mostly descriptive).

Common task options include:

- `secure`: no output will be shown on console nor logs.


#### Command Tasks

`command(interpreter, cmd)`

`bash(cmd)`:

Runs some code in bash. Hopefully this is never needed.

    bash('echo "hello"')
    
	bash('''
	    echo "hello"
	    ls
	    ps
	''')

`ruby(cmd)`

Runs some code in ruby.


### File Extension Handler Tasks

`file_handler` (mac only)

Associate an application with a file extension.

    file_handler('.txt', 'com.macromates.TextMate')

The application's identifier can be found with:

    mdls -name kMDItemCFBundleIdentifier -r /Applications/TextMate.app



#### File Tasks

`file(source, file, replacements={})`:

`source` can either be a URL or a file's path relative to the role's `files` directory.

	file('asound.conf', '/etc/asound.conf')
	
	file(
	    'http://example.com/asound.conf', 
	    '/etc/asound.conf'
	)

replacements rules can be specified, so the file acts as a template.

	file(
		'resolv.conf', 
		'/etc/resolv.conf',
		{
		    'MYIPADDRESS': '192.168.0.1'
		}
	)

### Hostname tasks

`hostname`:

    hostname('my_machine')

#### Kernel Tasks

`module(name)` (linux only):

Adds and loads a module.

	module('v4l')

#### Package Tasks

`package`:

Should automatically detect the package manager in presence. 
If multiple managers are present, it is possible to explicitly specify which to use:

    package('vim')
	
	[for package(p) in '''
	vim
	emacs
	'''.split()]

`homebrew_package` (mac only)

`cask_package` (mac only)

`mac_app_store` (mac only)

    mac_app_store('937984704')

Application identifiers can be found with:
    
    mas search app_name


`apt_package`

`yum_package`


### Command line

#### init

Creates the hierarchy for a new runbook.

    prvsn init -b path/to/runbook

#### provision

Default command if no host is specified. Provisions the machine `prvsn` runs on.

    prvsn provision -b path/to/runbook -r role1,role2

or alternatively, if running from the runbook directory:

    prvsn -r role1,role2
    
`--sudo` can be used to provision as root.

#### package

Creates an executable package with the runbook and the roles. The default package name is `package.pyz`.

    prvsn package -b path/to/runbook -r role1,role2 -o mypackage.pyz

The package can then be run individually:

    python mypackage.pyz

#### remote

Default command if a host is specified. Provision a remote host by:

1. creating a package
2. sending the package over ssh
3. running the package over ssh

example:

    prvsn remote -b path/to/runbook -r role1,role2 -n myhostname -u myuser

Additionally, ssh public key will be installed on the remote host (if no key is present, one is created). To disable this behavior, use '--no-copy-keys'.

`--sudo` can be used to provision as root (on the remote host).