========
tangoctl
========


.. image:: https://img.shields.io/pypi/v/tangoctl.svg
        :target: https://pypi.python.org/pypi/tangoctl

.. image:: https://img.shields.io/travis/tiagocoutinho/tangoctl.svg
        :target: https://travis-ci.org/tiagocoutinho/tangoctl

.. image:: https://readthedocs.org/projects/tangoctl/badge/?version=latest
        :target: https://tangoctl.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/tiagocoutinho/tangoctl/shield.svg
     :target: https://pyup.io/repos/github/tiagocoutinho/tangoctl/
     :alt: Updates


A Tango system CLI. Aimed at tango system administrators.

tangoctl aims to be to tango what systemctl is to to systemd.

* Free software: MIT license
* Documentation: https://tangoctl.readthedocs.io.


Features
--------

* server operations:
  * server info
  * tree of servers
  * list of servers
  * register/unregister servers
* device operations:
  * device info
  * tree of devices
  * list of devices
  * register/unregister devices
  * execute commands
  * command info
  * read and write attributes
  * attribute info
  * read and write properties


Special thanks to
-----------------

* PyTango_: Tango binding to python
* click_: beautiful command line interfaces
* gevent_: I/O made simple and efficient
* tabulate_: ASCII tables
* treelib_:  tree data structures


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _treelib: https://github.com/caesar0301/treelib
.. _tabulate: https://bitbucket.org/astanin/python-tabulate
.. _PyTango: https://github.com/gevent/gevent
.. _PyTango: https://github.com/tango-controls/pytango
.. _click: https://github.com/pallets/click
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
