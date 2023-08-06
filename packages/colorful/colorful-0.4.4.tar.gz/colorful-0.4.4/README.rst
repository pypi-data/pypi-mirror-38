colorful
========

Terminal string styling done right, in Python :tada:

Here's a tease
--------------

.. figure:: examples/basic_example.png
   :alt: colorful example

   colorful example

.. code:: python

    import colorful

    # create a colored string using clever method translation
    print(colorful.bold_white('Hello World'))
    # create a colored string using `str.format()`
    print('{c.bold}{c.lightCoral_on_white}Hello World{c.reset}'.format(c=colorful))

    # use true colors
    colorful.use_true_colors()

    # extend default color palette
    colorful.update_palette({'mint': '#c5e8c8'})
    print(colorful.mint_on_snow('Wow, this is actually mint'))

    # choose a predefined style
    colorful.use_style('solarized')
    # print the official solarized colors
    print(colorful.yellow('yellow'), colorful.orange('orange'),
        colorful.red('red'), colorful.magenta('magenta'),
        colorful.violet('violet'), colorful.blue('blue'),
        colorful.cyan('cyan'), colorful.green('green'))

    # choose specific color mode for one block
    with colorful.with_8bit_ansi_colors() as c:
        print(c.bold_green('colorful is awesome!'))

    # create and choose your own color palette
    MY_COMPANY_PALETTE = {
        'companyOrange': '#f4b942',
        'companyBaige': '#e8dcc5'
    }
    with colorful.with_palette(my_company_palette) as c:
        print(c.companyOrange_on_companyBaige('Thanks for choosing our product!'))

Key Features
------------

-  expressive and consistent API
-  support for different color modes (8bit ANSI, 256 ANSI, true colors)
-  support for predefined awesome styles (solarized, ...)
-  support for custom color palettes
-  support for different platforms (using colorama on windows)
-  context managers for clean color mode, color palette or style switch
-  no dependencies

Usage
-----

**colorful** supports all major Python versions: *2.7*, *3.2*, *3.3*,
*3.4*, *3.5* and *3.6*. We recommend to use the latest version released
on `PyPI <https://pypi.python.org/pypi/colorful>`__:

.. code:: bash

    pip install colorful

*Note: on a Windows system it will install ``colorama`` as a dependency
to ensure proper ANSI support.*

**colorful** does not require any special setup in order to be used:

.. code:: python

    import colorful

    print(colorful.italic_coral_on_beige('Hello World'))
    print('{c.italic_coral_on_beige}Hello World{c.reset}'.format(c=colorful))

Color modes
~~~~~~~~~~~

These days terminals not only support the ancient 8 bit ANSI colors but
often they support up to 16 Million colors with *`true
color <https://en.wikipedia.org/wiki/Color_depth#True_color_.2824-bit.29>`__*.
And if they don't support *true color* they might support the *`256 ANSI
color
palette <https://en.wikipedia.org/wiki/ANSI_escape_code#Colors>`__* at
least.

**colorful** supports the following color modes:

-  no colors / disable (``colorful.NO_COLORS``)
-  8 colors -> 8 bit ANSI colors (``colorful.ANSI_8BIT_COLORS``)
-  256 colors -> 256 ANSI color palette (24bit
   ``colorful.ANSI_256_COLORS``)
-  16'777'215 colors -> true color (``colorful.TRUE_COLORS``)

By default *colorful* tries to auto detect the best supported color mode
by your terminal. Consult
```colorful.terminal`` <https://github.com/timofurrer/colorful/blob/master/colorful/terminal.py>`__
for more details.

However, sometimes it makes sense to specify what color mode should be
used. **colorful** provides multiple ways to do so:

**(1) specify color mode globally via Python API**

.. code:: python

    colorful.disable()
    colorful.use_8bit_ansi_colors()
    colorful.use_256_ansi_colors()
    colorful.use_true_colors()

If you change the color mode during runtime it takes affect immediately
and globally.

**(2) enforce color mode globally via environment variable**

.. code:: bash

    COLORFUL_DISABLE=1 python eggs.py  # this process will not use ANY coloring
    COLORFUL_FORCE_8BIT_COLORS=1 python eggs.py  # this process will use 8 bit ANSI colors by default
    COLORFUL_FORCE_256_COLORS=1 python eggs.py  # this process will use 256 ANSI colors by default
    COLORFUL_FORCE_TRUE_COLORS=1 python eggs.py  # this process will use true colors by default

**(3) specify color mode locally via Python API (contextmanager)**

.. code:: python

    with colorful.with_8bit_ansi_colors() as c:
        print(c.italic_coral_on_beige('Hello world'))

    with colorful.with_256_ansi_colors() as c:
        print(c.italic_coral_on_beige('Hello world'))

    with colorful.with_true_colors() as c:
        print(c.italic_coral_on_beige('Hello world'))

Color palette
~~~~~~~~~~~~~

**colorful**'s Python API is based on *color names* like in
``colorful.bold_white_on_black('Hello')``. During runtime these *color
names* are translated into proper `ANSI escape
code <https://en.wikipedia.org/wiki/ANSI_escape_code>`__ sequences
supported by the *color mode* in use. However, all *color names* are
registered in a **color palette** which is basically a mapping between
the *color names* and it's corresponding RGB value. Very much like this:

.. code:: python

    color_palette_example = {
        'black': '#000000',
        'white': '#FFFFFF',
    }

*Note: Depending on the color mode which is used the RGB value will be
reduced to fit in the value domain of the color mode.*

The default color palette is the `X11
rgb.txt <https://en.wikipedia.org/wiki/X11_color_names>`__ palette -
it's shipped with *colorful*, thus, you don't have to provide your own.

**colorful** supports to update or replace the default color palette
with custom colors. The colors have to be specified as RGB hex or
channel values:

.. code:: python

    # corporate identity colors
    ci_colors = {
        'mint': '#c5e8c8',  # RGB hex value
        'darkRed': '#c11b55',  # RGB hex value
        'lightBlue': (15, 138, 191)  # RGB channel triplet
    }

    # replace the default palette with my custom one
    colorful.use_palette(ci_colors)
    # update the default palette with my custom one
    colorful.update_palette(ci_colors)

    # we can use these colors
    print(colorful.italic_mint_on_darkRed('My company'))

Styles
~~~~~~

**colorful** supports some famous color palettes using what's called
*styles* in colorful:

.. code:: python

    colorful.use_style('solarized')

    # print the official solarized colors
    print(colorful.yellow('yellow'), colorful.orange('orange'),
        colorful.red('red'), colorful.magenta('magenta'),
        colorful.violet('violet'), colorful.blue('blue'),
        colorful.cyan('cyan'), colorful.green('green'))

The following styles are already supported:

* solarized
* monokai

*Note: if you know some awesome color palettes which could be a new
style in colorful, please contribute it!*

Temporarily change colorful settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**colorful** provides a hand full of convenient context managers to
change the colorful settings temporarily:

**(1) change color mode**

Use 8 bit colors:

.. code:: python

    with colorful.with_8bit_ansi_colors() as c:
        print(c.red('I am red'))

Use 256 colors:

.. code:: python

    with colorful.with_256_ansi_colors() as c:
        print(c.red('I am red'))

Use true colors:

.. code:: python

    with colorful.with_true_colors() as c:
        print(c.red('I am red'))

**(2) change color palette**

.. code:: python

    # replace the entire color palette
    with colorful.with_palette(my_palette) as c:
        print(c.customRed('I am custom red'))

    # update the color palette
    with colorful.with_updated_palette(my_palette) as c:
        print(c.customRed('I am custom red'))

**(3) change style**

.. code:: python

    with colorful.with_style('solarized') as c:
        print(c.red('I am solarized red'))

--------------

\*

.. raw:: html

   <p align="center">

This project is published under `MIT <LICENSE>`__.A `Timo
Furrer <https://tuxtimo.me>`__ project.- :tada: -

.. raw:: html

   </p>

-
