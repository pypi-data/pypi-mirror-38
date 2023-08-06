Documentation
=============

poolbox (Pdf tOOLBOX) : manipulate PDF over the web.
poolbox is actually a web wrapper around various PDF libraries.


Installation
------------

Dependencies
____________

poolbox depends on wkhtmltopdf, poppler and pdftk.

On debian-based distribs :

    $ sudo apt-get install wkhtmltopdf poppler-utils pdftk


Production-ready
________________

Installation using pip :

    $ pip install poolbox

Done.


Developement
____________

Create and activate a virtual env :

    $ virtualenv myvenv
    
    $ cd myvenv
    
    $ . bin/activate


Clone this repository :

    $ git clone git@gitlab.com:atreal/poolbox.git

    $ cd poolbox


Install egg and depencies :

    $ python setup.py develop


You're good to go. 


Run the services
----------------

Run pyramid in waitress :

    $ pserve poolbox.ini


Web Services are available localy on :

    http://localhost:6544/WS_NAME

Developement
____________

Run pyramid in waitress, with auto reload when file are modified :

    $ pserve poolbox.ini --reload


You can allow global access by switching host address to 0.0.0.0 from poolbox.ini.


Services
--------

TODO : list services and associated functionalities.


OpenAPI
-------

OpenAPI JSON is available at : 

    http://localhost:6544/__api__


Tests
-----

To run the tests, you have to install the egg in dev mode :

    $ python setup.py develop


Then launch the app : 

    $ pserve poolbox.ini


In another terminal, run the tests :

    $ cd tests

    $ python test_pdf_toolbox.py
