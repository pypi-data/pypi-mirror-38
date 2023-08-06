crython
=======

|Join the chat at https://gitter.im/crython/Lobby|

|Build Status| |Build status| |codecov| |Code Climate| |Issue Count|

|PyPI version| |PyPI versions|

|Stories in Ready|

crython is a lightweight task (function) scheduler using
`cron <http://en.wikipedia.org/wiki/Cron>`__ expressions written in
python.

Status
~~~~~~

This module is actively maintained.

Installation
~~~~~~~~~~~~

To install crython from `pip <https://pypi.python.org/pypi/pip>`__:

.. code:: bash

       $ pip install crython

To install crython from source:

.. code:: bash

       $ git clone git@github.com:ahawker/crython.git
       $ python setup.py install

Usage
~~~~~

Crython supports seven fields (seconds, minutes, hours, day of month,
month, weekday, year).

Call a function once a minute:

.. code:: python

       import crython
       
       # Fire once a minute.
       @crython.job(second=0)
       def foo():
           print "... while heavy sack beatings are up a shocking nine hundred percent? - Kent Brockman"

Call a function every ten seconds:

.. code:: python

       # Fire every 10 seconds.
       @crython.job(second=range(0, 60, 10))
       def foo():
           print "I'm a big four-eyed lame-o and I wear the same stupid sweater every day. - Homer's Brain"

Call a function with a single cron expression:

.. code:: python

       # Fire every 10 seconds.
       @crython.job(second='*/10')
       def foo():
           print "Hail to the thee Kamp Krusty... - Kampers"

Call a function with a full cron expression:

.. code:: python

       # Fire once a week.
       @crython.job(expr='0 0 0 * * 0 *')
       def foo():
           print "Back in line, maggot! - Kearny"

Call a function with positional and/or keyword arguments:

.. code:: python

       # Fire every second.
       @job('safety gloves', second='*', name='Homer Simpson')
       def foo(item, name):
           print "Well, I don't need {0}, because I'm {1}. -- Grimey".format(item, name)

Call a function using `predefined
keywords <https://github.com/ahawker/crython#keywords>`__:

.. code:: python

       # Fire once a day.
       @crython.job(expr='@daily')
       def foo():
           print "That's where I saw the leprechaun. He tells me to burn things! - Ralph Wiggum"

.. code:: python

       # Fire once immediately after scheduler starts.
       @crython.job(expr='@reboot')
       def foo():
           print "I call the big one bitey. - Homer Simpson"

Call a function and run it within a separate thread (default behaviour
if ``ctx`` is not specified):

.. code:: python

       # Fire once a week.
       @crython.job(expr='@weekly', ctx='thread')
       def foo():
           print "No, no, dig up stupid. - Chief Wiggum"

Call a function and run it within a separate process:

.. code:: python

       # Fire every hour.
       @crython.job(expr='@hourly', ctx='multiprocess')
       def foo():
           print "Eat my shorts. - Bart Simpson"

Start the global job scheduler:

.. code:: python

       if __name__ == '__main__':
           crython.start()

Keywords
~~~~~~~~

+-----------------------+-----------------------+-----------------------+
| Entry                 | Description           | Equivalent To         |
+=======================+=======================+=======================+
| @yearly/@annually     | Run once a year at    | 0 0 0 0 1 1 \*        |
|                       | midnight in the       |                       |
|                       | morning of January 1  |                       |
+-----------------------+-----------------------+-----------------------+
| @monthly              | Run once a month at   | 0 0 0 0 1 \* \*       |
|                       | midnight in the       |                       |
|                       | morning of the first  |                       |
|                       | of the month          |                       |
+-----------------------+-----------------------+-----------------------+
| @weekly               | Run once a week at    | 0 0 0 0 \* 0 \*       |
|                       | midnight in the       |                       |
|                       | morning of Sunday     |                       |
+-----------------------+-----------------------+-----------------------+
| @daily                | Run once a day at     | 0 0 0 \* \* \* \*     |
|                       | midnight              |                       |
+-----------------------+-----------------------+-----------------------+
| @hourly               | Run once an hour at   | 0 0 \* \* \* \* \*    |
|                       | the beginning of the  |                       |
|                       | hour                  |                       |
+-----------------------+-----------------------+-----------------------+
| @minutely             | Run once a minute at  | 0 \* \* \* \* \* \*   |
|                       | the beginning of the  |                       |
|                       | minute                |                       |
+-----------------------+-----------------------+-----------------------+
| @reboot               | Run once at startup   | @reboot               |
+-----------------------+-----------------------+-----------------------+

TODO
~~~~

-  Support “L”, “W” and “#” specials.
-  Determine time delta from now -> next time expression is valid.

Contributing
~~~~~~~~~~~~

If you would like to contribute, simply fork the repository, push your
changes and send a pull request.

License
~~~~~~~

Crython is available under the `MIT
license <https://github.com/ahawker/crython/blob/master/LICENSE.md>`__.

See Other
~~~~~~~~~

There are similar python cron libraries out there. See:
`pycron <http://www.kalab.com/freeware/pycron/pycron.htm>`__,
`python-crontab <http://pypi.python.org/pypi/python-crontab/>`__,
`cronex <https://github.com/jameseric/cronex>`__.

.. |Join the chat at https://gitter.im/crython/Lobby| image:: https://badges.gitter.im/crython/Lobby.svg
   :target: https://gitter.im/crython/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Build Status| image:: https://travis-ci.org/ahawker/crython.png
   :target: https://travis-ci.org/ahawker/crython
.. |Build status| image:: https://ci.appveyor.com/api/projects/status/lrl0vof32pkl3tu9?svg=true
   :target: https://ci.appveyor.com/project/ahawker/crython
.. |codecov| image:: https://codecov.io/gh/ahawker/crython/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ahawker/crython
.. |Code Climate| image:: https://codeclimate.com/github/ahawker/crython/badges/gpa.svg
   :target: https://codeclimate.com/github/ahawker/crython
.. |Issue Count| image:: https://codeclimate.com/github/ahawker/crython/badges/issue_count.svg
   :target: https://codeclimate.com/github/ahawker/crython
.. |PyPI version| image:: https://badge.fury.io/py/crython.svg
   :target: https://badge.fury.io/py/crython
.. |PyPI versions| image:: https://img.shields.io/pypi/pyversions/crython.svg
   :target: https://pypi.python.org/pypi/crython
.. |Stories in Ready| image:: https://badge.waffle.io/ahawker/crython.svg?label=ready&title=Ready
   :target: http://waffle.io/ahawker/crython
