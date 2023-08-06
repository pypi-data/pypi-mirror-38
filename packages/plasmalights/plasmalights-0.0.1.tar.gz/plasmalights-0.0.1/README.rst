Plasma Arcade Lights
====================

|Build Status| |Coverage Status| |PyPi Package| |Python Versions|

https://shop.pimoroni.com/products/plasma

Eight super-bright RGB LED indicators, ideal for adding visual
notifications to your Raspberry Pi on their own or on a pHAT stacking
header.

Installing
----------

Full install (recommended):
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We've created an easy installation script that will install all
pre-requisites and get your Plasma Arcade Button Lights up and running
with minimal efforts. To run it, fire up Terminal which you'll find in
Menu -> Accessories -> Terminal on your Raspberry Pi desktop, as
illustrated below:

.. figure:: http://get.pimoroni.com/resources/github-repo-terminal.png
   :alt: Finding the terminal

In the new terminal window type the command exactly as it appears below
(check for typos) and follow the on-screen instructions:

.. code:: bash

    curl https://get.pimoroni.com/plasma | bash

If you choose to download examples you'll find them in
``/home/pi/Pimoroni/plasma/``.

Manual install:
~~~~~~~~~~~~~~~

Library install for Python 3:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

on Raspbian:

.. code:: bash

    sudo apt-get install python3-plasmalights

other environments:

.. code:: bash

    sudo pip3 install plasmalights

Library install for Python 2:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

on Raspbian:

.. code:: bash

    sudo apt-get install python-plasmalights

other environments:

.. code:: bash

    sudo pip2 install plasmalights

Using Plasma
~~~~~~~~~~~~

Plasma installs two programs onto your Raspberry Pi. ``plasma`` itself
and a tool called ``plasmactl`` you can use to install and switch
lighting effects. Plasma runs as a service on your system.

``plasmactl`` commands:

-  ``plasmactl 255 0 0`` - Set Plasma lights to R, G, B colour. Red in
   this case.
-  ``plasmactl <pattern>`` - Set Plasma lights to pattern image
-  ``plasmactl fps <fps>`` - Change plasma effect framerate (default is
   30, lower FPS = less CPU)
-  ``plasmactl --list`` - List all available patterns
-  ``sudo plasmactl --install <pattern>`` - Install a new pattern, where
   ``<pattern>`` is the filename of a 24bit PNG image file

Development:
~~~~~~~~~~~~

If you want to contribute, or like living on the edge of your seat by
having the latest code, you should clone this repository, ``cd`` to the
library directory, and run:

.. code:: bash

    sudo python3 setup.py install

(or ``sudo python setup.py install`` whichever your primary Python
environment may be)

Documentation & Support
-----------------------

-  Guides and tutorials - https://learn.pimoroni.com/plasma
-  Function reference - http://docs.pimoroni.com/plasma/
-  Get help - http://forums.pimoroni.com/c/support

.. |Build Status| image:: https://travis-ci.com/pimoroni/plasma.svg?branch=master
   :target: https://travis-ci.com/pimoroni/plasma
.. |Coverage Status| image:: https://coveralls.io/repos/github/pimoroni/plasma/badge.svg?branch=master
   :target: https://coveralls.io/github/pimoroni/plasma?branch=master
.. |PyPi Package| image:: https://img.shields.io/pypi/v/plasmalights.svg
   :target: https://pypi.python.org/pypi/plasmalights
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/plasmalights.svg
   :target: https://pypi.python.org/pypi/plasmalights
