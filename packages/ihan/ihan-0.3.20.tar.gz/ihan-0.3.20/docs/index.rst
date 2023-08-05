IHAN Client
===========

This is the installation and usage guide for the `IHAN <https://www.ihan.ee/>`_ Client. This utility is used for feeding and back filling log files to the IHAN service.

Requirements
------------

Python 2.7 and Python 3.4+ are supported.

On most Ubuntu systems you should be able to install Python and virtualenv via the following:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install \
        python-pip \
        python-virtualenv

Installation
------------

.. code-block:: bash

    $ virtualenv ~/.ihan
    $ source ~/.ihan/bin/activate
    $ pip install --upgrade ihan

Logging In
----------

Make sure you have an account setup at `IHAN <http://www.ihan.ee/>`_ and you have your email address and password for your IHAN account to hand.

.. code-block:: bash

    $ source ~/.ihan/bin/activate
    $ ihan login

Enter your email address and password when prompted. If authentication is successful API credentials will be written to ``~/.ihan/config``. From this point on the ``live`` and ``backfill`` commands should work without issue.

Shipping Logs
-------------

Make sure the user account that is running has read access to the main nginx log file. If it doesn't please run the following. Replace ``your_user_name`` with your unix username (found via ``whoami``).

.. code-block:: bash

    $ sudo chown your_user_name:www-data /var/log/nginx/access.log
    $ sudo chmod u+r /var/log/nginx/access.log

.. code-block:: bash

    $ sudo apt install screen
    $ screen
    $ ihan live /var/log/nginx/access.log

Once that's running type ``CTRL-A`` and then ``CTRL-D`` to return to your regular shell.

Backfill Log Files
------------------

If the log file is not compressed, run the following:

.. code-block:: bash

    $ screen
    $ ihan backfill /var/log/nginx/access.log

If it is compressed, run the following:

.. code-block:: bash

    $ screen
    $ gunzip -c /var/log/nginx/access.log.gz | ihan backfill -

Once that's running type ``CTRL-A`` and then ``CTRL-D`` to return to your regular shell.