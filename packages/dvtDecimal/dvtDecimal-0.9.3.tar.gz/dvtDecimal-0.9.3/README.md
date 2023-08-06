This package provides a way to access repeating decimals in the
decimal representation of rational numbers.

### class object

``` python3
>>> from dvtDecimal import *

```



Once package importation completed, you have to create a rational
number using:

* one of its fraction representation


``` python3
>>> f = dvtDecimal(-604, 260)

```

for the fraction whose numerator is -604 and denominator is 260.


* its usual decimal representation

``` python3
>>> f = dvtDecimal(2.5)

```

* the repeating decimals as a string

``` python3
>>> f = dvtDecimal('00765')

```

thus creating a number (w/o irregular part) between 0 and 1.
In the example, 0.007650076500765... and so on.


### object methods

Once you created the object for example, you can access to those
methods and variables:


``` python3
>>> f.dispResults()
For fraction: -604 / 260
    integer   part : -2
    irregular part : 0.3
    periodic  part : [2, 3, 0, 7, 6, 9]
    mixed fraction : [-2, 21, 65]
Operation in Python gives : -2.3230769230769233
>>> f.initValues
[-604, 260]
>>> f.simpValues
[-151, 65]
>>> f.isDecimal()
False
>>> f.dotWrite(20)
-2.32307692307692307692
>>> f.intPart
-2
>>> f.irrPart
0.3
>>> f.repPart
[2, 3, 0, 7, 6, 9]
>>> f.repPartC
230769
>>> f.periodLen
6
>>> f.gcd
4
>>> f.mixedF
[-2, 21, 65]
>>> f.sign
-1

```

Entering via repeating decimals string allows:

``` python3
>>> f = dvtDecimal('0123456789')
>>> f = dvtDecimal(*f.simpValues)
>>> f.simpValues
[13717421, 1111111111]

```


dvtDecimal also supports minimal operations (+,-,*,/) in between
elements of the class but also with integers:


``` python3
>>> f = dvtDecimal(1, 5)
>>> g = dvtDecimal(10, 3)
>>> h = f + g
>>> h.mixedF
[3, 8, 15]
>>> i = f / g
>>> i.mixedF
[0, 3, 50]

```

``` python3
>>> f = dvtDecimal(1, 5)
>>> g = 5
>>> h = f * g
>>> h.isDecimal()
True

```


``` python3
>>> f = dvtDecimal(1, 5)
>>> g = dvtDecimal(7, 5)
>>> h = f - g
>>> h.simpValues
[-6, 5]

```

### further...

More operations!


### about

dvtDecimal is rather an attempt to publish on the `PyPi` packages
index than a fully completed python project, I do not recommend
dvtDecimal usage for professionnal use. You have to consider this
package as an experiment.
