TimedDict
=========

Requirements
-------------

* Python -- one of the following:

  - CPython_ : >= 3.3
  - PyPy_ : Latest version

.. _CPython: https://www.python.org/
.. _PyPy: https://pypy.org/

Installation
------------

Package is uploaded on `PyPI <https://pypi.org/project/TimedDict>`_.

You can install it with pip::

    $ python3 -m pip install TimedDict


Backwards compatibility
-----------------------

Backwards compatibility is only guaranteed between minor versions above the stable version (1.0)
Therefore it's advised to to pin the module on a version ether the specific version like:
TimedDict==X.X.X

or get the latest minor version:
TimedDict~=X.X.X

See more examples of how to pin version in `PEP-440 <https://www.python.org/dev/peps/pep-0440/#compatible-release>`_.


Documentation
-------------

For support, please refer to `StackOverflow <https://stackoverflow.com/>`_.

Example
-------

The following example showcases

.. code:: python

    import time
    from TimedDict import timeddict

    events_window = timeddict.TimedDict()

    now = time.time()

    # Assign values like a normal dict like:
    events_window[now] = 'value_1'
    events_window[now + 1] = 'value_2'

    # ...or like:
    events_window.update({now + 2: {'values': {'value_3', 'value_4'}}})

    print('Raw data:')
    print(events_window)

    # NOTE:
    # As the TimedDict has a thread running purging old elements, it's important to ether
    # use the protect() or pause() followed by a resume() when iterating.

    # Automatic by the use of context manager, protect() approach
    with events_window.protect():
        print('\n- protect()')
        for event in events_window:
            print(event)

    # Manual setting, pause() and resume() approach
    events_window.pause()
    print('\n- pause() followed by resume()')

    for event in events_window:
        print(event)

    events_window.resume()

    # TTL example
    print('\nLength of the TimedDict: {}'.format(len(events_window)))
    print(events_window)
    time.sleep(1.1)
    print(events_window)
    time.sleep(1)
    print(events_window)
    time.sleep(1)
    print(events_window)

    # Gracefully stop the purge thread
    events_window.stop()

This example will print:

.. code:: python

    Raw data:
    {1534608053.6948583: 'value_1', 1534608054.6948583: 'value_2', 1534608055.6948583: {'values': {'value_4', 'value_3'}}}

    - protect()
    1534608053.6948583
    1534608054.6948583
    1534608055.6948583

    - pause() followed by resume()
    1534608053.6948583
    1534608054.6948583
    1534608055.6948583

    Length of the TimedDict: 3
    {1534608053.6948583: 'value_1', 1534608054.6948583: 'value_2', 1534608055.6948583: {'values': {'value_4', 'value_3'}}}
    {1534608054.6948583: 'value_2', 1534608055.6948583: {'values': {'value_4', 'value_3'}}}
    {1534608055.6948583: {'values': {'value_4', 'value_3'}}}
    {}

License
-------

TimedDict is released under the MIT License. See LICENSE for more information.