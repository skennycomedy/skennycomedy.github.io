---
layout: default
title: Sigma
permalink: /sigma/
---

# THE SIGMA COGNITIVE ARCHITECTURE
Sigma is a cognitive architecture (AGI) that is grounded in a graphical architecture. This guide will walk you through setting up and running Sigma. You can then proceed to the in-depth tutorial. It requires some familiarity with Lisp and Quicklisp, but there are links to additional information to help guide you if you're new to Lisp.

[Developed at the University of Southern California](http://cogarch.ict.usc.edu)  
Current release: Sigma38  

## Overview ##

* If you're new to lisp, there is a lisp tutorial [here](https://gigamonkeys.com/book/)  
* A full Sigma tutorial is available [here](/tutorial)  
* Sigma reference sheet can be found [here](/referencesheet)  
* For help contact: sigma@ict.usc.edu

---
### Where to get Sigma ###

You can download Sigma using the following command--it requires you to have [git](http://git-scm.com/) installed on your machine.

```lisp
$ git clone https://github.com/skenny24/sigma.git
```
This will copy a directory *sigma* onto your local machine, under ```sigma/src``` you will see the Sigma source files.  

Sigma is written in Common Lisp and uses a REPL (Read-Eval-Print Loop) which is a programming interface that has continuous interaction with the language--the commands you see throughout this document and in the tutorial illustrate this interaction. This version of Sigma requires [LispWorks](http://www.lispworks.com/) for use of its GUI, but can be run in other implementations for use of the core functionality (it has been tested with CLISP). If you're looking for an open source common lisp implementation options are available [here](http://www.jonathanfischer.net/modern-common-lisp-on-windows/) and [here](http://common-lisp.net/project/lispbox/).

---
### Install Quicklisp ###

Sigma is loaded using the [Quicklisp library manager](https://www.quicklisp.org/beta/). If you don't have quicklisp installed please follow the directions on the Quicklisp site for installation, you will then need to load the ```quicklisp.lisp``` file and run the following command to install:
```
CL-USER> (quicklisp-quickstart:install)
```
This will create a directory called ```quicklisp``` in your home directory. To ensure quicklisp is loaded each time you start your lisp system you should run the following command:
```lisp
CL-USER> (ql:add-to-init-file)
```
This will append code to your initialization file which checks and loads Quicklisp each time you start LispWorks (or whatever Lisp system you're using). In LispWorks, commands will be added to your ```.lispworks``` initialization file

---
### Load Sigma ###

Using LispWorks (or one of the open source options) you can fire up a REPL and add the sigma source directory to the ASDF source registry system (using your own path) like so:
```lisp
CL-USER> (pushnew #p"/home/USER/sigma/src/" asdf:*central-registry*)
```
Sigma requires the cl-store library for serializing and deserializing Common Lisp objects, load the library:

```lisp
CL-USER> (ql:quickload :cl-store)
```
Once cl-store is loaded, you can then load the sigma package:

```lisp
CL-USER> (ql:quickload :sigma)
```
You can use```in-package``` to make sigma the current package and call functions without the ```sigma:``` qualifier:
```lisp
CL-USER> (in-package :sigma)
```

---
### Permanently Add Sigma to your Initialization file ###
The commands above can be added to your initialization file so that you need not run them every time you start your Lisp system. For example in *Lispworks* you can add these lines to the end of your *.lispworks* file:
```
(pushnew #p"/home/USER/sigma/src/" asdf:*central-registry*)
(ql:quickload :cl-store)
(ql:quickload :sigma)
```
Then every time you start up lispworks Sigma will be loaded and you can simply run ```(in-package :sigma)```

Additional commands can also be added to set your default package to sigma every time you launch LispWorks. A sample LispWorks initalization file can be found [here](https://github.com/skenny24/sigma/blob/master/src/sigma-init.lisp)

IMPORTANT NOTE: to compile new files within the sigma package the package directive should be added at the beginning of the source file before compiling
```lisp
(in-package :sigma)
```

---
Once you've completed the setup instructions above you're ready to run through the [full Sigma tutorial](/tutorial)  

---

### Older Releases are Available [here](https://bitbucket.org/sigma-development/sigma-archive/src)  ###

Download the archive, releases < Sigma38 require the following steps

* Under *SigmaXX/src* you will see the ```sigma.lisp```
* [LispWorks](http://www.lispworks.com/) is required for use of graphical features, but Sigma can be run in other implementations for use of the core functionality (tested with CLISP)
* load/compile the file *sigma.lisp*. This will also compile the additional files that sigma requires & if Lispworks' CAPI library is detected the graphical features will be loaded as well. 
* The variable *sigma-home* by default assumes that you have downloaded sigma into your $HOME directory. If you have downloaded Sigma to another location you will need to adjust that variable (line 52 of *sigma.lisp*)
* other GUI-based git tools available: [SourceTree](https://www.atlassian.com/software/sourcetree/overview) 

*This material is based on research supported by the Army, the Office of Naval Research, and the Air Force Office of Scientific Research.
