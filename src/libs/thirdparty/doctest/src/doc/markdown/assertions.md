## Assertion macros

Most test frameworks have a large collection of assertion macros to capture all possible conditional forms (```_EQUALS```, ```_NOTEQUALS```, ```_GREATER_THAN``` etc).

**doctest** is different (but it's like [**Catch**](https://github.com/philsquared/Catch) in this regard). Because it decomposes comparison expressions most of these forms are reduced to one or two that you will use all the time. That said there is a rich set of auxiliary macros as well.

There are 3 levels of assert severity for all assertion macros:

- ```REQUIRE``` - this level will immediately quit the test case if the assert fails and will mark the test case as failed.
- ```CHECK``` - this level will mark the test case as failed if the assert fails but will continue with the test case.
- ```WARN``` - this level will only print a message if the assert fails but will not mark the test case as failed.

The ```CHECK``` level is mostly useful if you have a series of essentially orthogonal assertions and it is useful to see all the results rather than stopping at the first failure.

All asserts evaluate the expressions only once and if they fail - the values are [**stringified**](stringification.md) properly. 

## Expression decomposing asserts

These are of the form ```CHECK(expression)```  (Same for ```REQUIRE``` and ```WARN```).

```expression``` can be a binary comparison like ```a == b``` or just a single thing like ```vec.isEmpty()```.

If an exception is thrown it is caught, reported, and counted as a failure (unless the assert is of level ```WARN```).

Examples:

```c++
CHECK(flags == state::alive | state::moving);
CHECK(thisReturnsTrue());
REQUIRE(i < 42);
```

Negating asserts - ```<LEVEL>_FALSE(expression)``` - evaluates the expression and records the _logical NOT_ of the result.

These forms exist as a workaround for the fact that ```!``` prefixed expressions cannot be decomposed properly.

Example:

```c++
REQUIRE_FALSE(thisReturnsFalse());
```

## Binary and unary asserts

These asserts don't use templates to decompose the comparison expressions for the left and right parts.

These have the same guarantees as the expression decomposing ones - just less templates - [**20% faster**](benchmarks.md#cost-of-an-assertion-macro) for compile times.

```<LEVEL>``` is one of 3 possible: ```REQUIRE```/```CHECK```/```WARN```.

- ```<LEVEL>_EQ(left, right)``` - same as ```<LEVEL>(left == right)```
- ```<LEVEL>_NE(left, right)``` - same as ```<LEVEL>(left != right)```
- ```<LEVEL>_GT(left, right)``` - same as ```<LEVEL>(left >  right)```
- ```<LEVEL>_LT(left, right)``` - same as ```<LEVEL>(left <  right)```
- ```<LEVEL>_GE(left, right)``` - same as ```<LEVEL>(left >= right)```
- ```<LEVEL>_LE(left, right)``` - same as ```<LEVEL>(left <= right)```
- ```<LEVEL>_UNARY(expr)``` - same as ```<LEVEL>(expr)```
- ```<LEVEL>_UNARY_FALSE(expr)``` - same as ```<LEVEL>_FALSE(expr)```

## Fast asserts

These are the faster versions of the binary and unary asserts - by [**30-70%**](benchmarks.md#cost-of-an-assertion-macro) of compile time.

The difference is they don't evaluate the expression in a ```try/catch``` block - if the expression throws the whole test case ends.

There is also the [**```DOCTEST_CONFIG_SUPER_FAST_ASSERTS```**](configuration.md#doctest_config_super_fast_asserts) config identifier that makes them even faster by another [**35-80%**](benchmarks.md#cost-of-an-assertion-macro)!

```<LEVEL>``` is one of 3 possible: ```REQUIRE```/```CHECK```/```WARN```.

- ```FAST_<LEVEL>_EQ(left, right)``` - almost the same as ```<LEVEL>(left == right)```
- ```FAST_<LEVEL>_NE(left, right)``` - almost the same as ```<LEVEL>(left != right)```
- ```FAST_<LEVEL>_GT(left, right)``` - almost the same as ```<LEVEL>(left >  right)```
- ```FAST_<LEVEL>_LT(left, right)``` - almost the same as ```<LEVEL>(left <  right)```
- ```FAST_<LEVEL>_GE(left, right)``` - almost the same as ```<LEVEL>(left >= right)```
- ```FAST_<LEVEL>_LE(left, right)``` - almost the same as ```<LEVEL>(left <= right)```
- ```FAST_<LEVEL>_UNARY(expr)``` - almost the same as ```<LEVEL>(expr)```
- ```FAST_<LEVEL>_UNARY_FALSE(expr)``` - almost the same as ```<LEVEL>_FALSE(expr)```

## Exceptions

```<LEVEL>``` is one of 3 possible: ```REQUIRE```/```CHECK```/```WARN```.

- ```<LEVEL>_THROWS(expression)```

Expects that an exception (of any type) is thrown during evaluation of the expression.

* ```<LEVEL>_THROWS_AS(expression, exception_type)```

Expects that an exception of the _specified type_ is thrown during evaluation of the expression.

* ```<LEVEL>_NOTHROW(expression)```

Expects that no exception is thrown during evaluation of the expression.

## Floating point comparisons

When comparing floating point numbers - especially if at least one of them has been computed - great care must be taken to allow for rounding errors and inexact representations.

**doctest** provides a way to perform tolerant comparisons of floating point values through use of a wrapper class called ```doctest::Approx```. ```doctest::Approx``` can be used on either side of a comparison expression. It overloads the comparisons operators to take a tolerance into account. Here's a simple example:

```c++
REQUIRE(performComputation() == doctest::Approx(2.1));
```

By default a small epsilon value is used that covers many simple cases of rounding errors. When this is insufficient the epsilon value (the amount within which a difference either way is ignored) can be specified by calling the ```epsilon()``` method on the ```doctest::Approx``` instance. e.g.:

```c++
REQUIRE(22.0/7 == doctest::Approx(3.141).epsilon(0.01));
```

When dealing with very large or very small numbers it can be useful to specify a scale, which can be achieved by calling the ```scale()``` method on the ```doctest::Approx``` instance.

--------

- Check out the [**example**](../../examples/assertion_macros/main.cpp) which shows many of these macros
- Do not wrap assertion macros in ```try```/```catch``` - the REQUIRE macros throw exceptions to end the test case execution!

---------------

[Home](readme.md#reference)
