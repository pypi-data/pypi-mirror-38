# AIMMS Pygments Style

Enable a style in Pygments Python package for highlighting AIMMS code. Notably, this can be coupled with a proper AIMMS lexer, and Sphinx Python documentation generator. 

Install
-----------

`python -m pip install --index-url https://test.pypi.org/simple/ aimms-pygments-style`

Verify it is working
---------------------

Please run the following in the Python Interpreter:

``` python
    >>> from pygments.styles import get_all_styles
    >>> list(get_all_styles())
```

And verify that you have a new Pygments style named `aimmslexer`

Modifying style rules
-------------------

To modify it, please take a look at the file [aimmslexer.py](https://gitlab.com/ArthurdHerbemont/aimms-pygments-style/tree/master/style) and [Pygments Style documentation](http://pygments.org/docs/styles/)