Installation Guide
==================

To install ``birdfeeder``, run the following commands in your terminal. It is **highly** reccomended that you initialize a virtual environment with ``virtualenvwrapper``:

.. code-block:: bash

   $ mkvirtualenv birdfeeder
   $ git clone https://github.com/newslynx/birdfeeder.git
   $ cd birdfeeder
   $ pip install -r requirements.txt
   $ pip install .

Tests can be run with ``nose`` in the projects root directory:

.. code-block:: bash

   $ nosetests


