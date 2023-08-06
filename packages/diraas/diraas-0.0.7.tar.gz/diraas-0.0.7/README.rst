Diraas (Make directory as a service)
====================================

Get started
-----------

Run server::

    $ pip install diraas
    $ diraas --token=abc123 --host=127.0.0.1 --port=5100 ~/lab/


Consume the API::

    HTTP GET http://127.0.0.1:5100/ls?token=abc123&targets=*.txt%20*.py
    HTTP GET http://127.0.0.1:5100/fetch?token=abc123&targets=a.txt%20b.txt
