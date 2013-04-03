.. 

admin_apps
======================

Quickstart
----------

To bootstrap the project::

    virtualenv admin_apps
    source admin_apps/bin/activate
    cd path/to/admin_apps/repository
    pip install -r requirements.pip
    pip install -e .
    cp admin_apps/settings/local.py.example admin_apps/settings/local.py
    manage.py syncdb --migrate

Documentation
-------------

Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.
