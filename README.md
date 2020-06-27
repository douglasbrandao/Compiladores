# CK Compiler

CK Compiler is an instructions generator to Assembly language, developed to complete the Compiler discipline taught by Ed'Wilson Ferreira at Federal Institute of Mato Grosso.

## The CK Language

```python
run # code started
integer n = 1;
integer j; # declare variables
input(j); # read strings or variables
while(n < j){ # loop
  if(2 >= 3){ # conditional
      display("teste\n"); # show strings or variables
  }
}
exit # code finished
```

## Requirements

* Python 3

## Let's get started

Clone the repository

```bash
git clone https://github.com/douglasbrandao/ck-compiler.git
```

Go to the repository folder

```bash
cd ck-compiler
```

How to execute

```bash
python3 main.py [code] [args]
```

> Some examples codes were made available in Examples folder

To see all the arguments and how to use just add *-h* argument

```bash
python3 main.py -h
```

## Author

Douglas Frota Brandão - [douglasbrandao](https://github.com/douglasbrandao "Douglas Brandão")
