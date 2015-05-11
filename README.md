zutilties
=========

Some helpful nodes for ZOCP networks, implemented in Python.


zmultiplier
-----------

Multiplies an input by a factor. Useful when a node outputs a float between 0.0 and 1.0 but another node needs a number between 0 and 255.
```
usage: zmultiplier.py [-h] [-f --factor F] [-i --inverse] [N]

positional arguments:
  N              the number of ports to add, all multiplied by the same factor

optional arguments:
  -h, --help     show this help message and exit
  -f --factor F  initial value of Factor
  -i --inverse   multiply (False) or divide (True) by factor
```

zcounter
--------

Counts and displays the number of signals received on its input (which can be anything) for debugging purposes.


zswitchin
---------

Virtual switchboard node that allows one of a number of inputs to be connected to a single output.
```
usage: zswitchin.py [-h] [{boolean,int,float,vec2f,vec3f,vec4f,string}] [N]

positional arguments:
  {boolean,int,float,vec2f,vec3f,vec4f,string}
                        the type of ports to use for input and output
  N                     the number of input-ports to add

optional arguments:
  -h, --help            show this help message and exit
```

zswitchout
----------

Virtual switchboard node that allows a single input to be connected to one of the nodes outputs.
```
usage: zswitchin.py [-h] [{boolean,int,float,vec2f,vec3f,vec4f,string}] [N]

positional arguments:
  {boolean,int,float,vec2f,vec3f,vec4f,string}
                        the type of ports to use for input and output
  N                     the number of output-ports to add

optional arguments:
  -h, --help            show this help message and exit
```
