.. image:: pySlipQt/examples/graphics/pyslipqt_logo.png

pySlipQt
========

pySlipQt is a 'slip map' widget for PyQt5.

During my work writing geophysical applications in python I often wanted to
display a map that was very large - many hundreds of thousands of pixels in
width.  I searched around for a GUI solution that would work rather like Google
maps: tiled, layers, etc.  I couldn't find anything that didn't assume
browser+map server.  So I wrote my own PyQt5 widget.  This worked well for
cartesian self-generated maps and has been extended to handle non-cartesian
maps and tiles sourced from places like OpenStreetMap.

It's a poor thing, but solves my problem.  I'm placing it here in the hope that
someone else may find it useful.  If you find it useful, or make improvements
to it, drop me a line.

pySlipQt works on Linux, Mac and Windows.  It only works with PyQt5 and
Python 3.6+.

The widget API is documented in
`the wiki <https://github.com/rzzzwilson/pySlipQt/wiki/The-pySlipQt-API>`_.

Screenshots
===========

A few screenshots of the demonstration program *pyslipqt_demo.py*, the first
showing OpenStreetMap tiles:

.. image:: pySlipQt/examples/graphics/pyslip_demo_osm.png

Next, the pre-generated GMT tiles:

.. image:: pySlipQt/examples/graphics/pyslip_demo_gmt.png

Getting pySlipQt
================

You can clone this repository, of course, and then do this in the top directory
containing the *setup.py* program:

::

    python setup.py install

Or you could install through PyPI:

::

    pip install pySlipQt

Using pip is the recommended way to install pySlipQt as the cheese shop code
is guaranteed to work.  The code in the GitHib repository is, unfortunately,
a moving target.

Map Tiles Licensing
===================

OpenStreetMap Tiles
-------------------

© OpenStreetMap contributors

See the licence `here <http://www.openstreetmap.org/copyright>`_.

Stamen Toner Tiles
------------------

Map tiles by `Stamen Design <http://stamen.com/>`_, under
`CC BY 3.0 <http://creativecommons.org/licenses/by/3.0>`_.  Data by
`OpenStreetMap <http://openstreetmap.org>`_, under
`ODbL <http://www.openstreetmap.org/copyright>`_.

Stamen Watercolor and Transport Tiles
-------------------------------------

Map tiles by `Stamen Design <http://stamen.com/>`_, under
`CC BY 3.0 <http://creativecommons.org/licenses/by/3.0>`_.  Data by
`OpenStreetMap <http://openstreetmap.org>`_, under
`CC BY SA <http://creativecommons.org/licenses/by-sa/3.0>`_.

Tile Usage
==========

Before using any tiles provided by pySlipQt modules, make sure you are not
transgressing any usage rules applied by the tiles provider.

Heavy usage of tiles probably means you should set up your own tile cache
server and write a Tiles module that gets tiles from your own server(s).
