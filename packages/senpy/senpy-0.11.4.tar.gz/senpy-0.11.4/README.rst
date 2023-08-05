.. image:: img/header.png
   :width: 100%
   :target: http://demos.gsi.dit.upm.es/senpy

.. image:: https://travis-ci.org/gsi-upm/senpy.svg?branch=master
   :target: https://travis-ci.org/gsi-upm/senpy

Senpy lets you create sentiment analysis web services easily, fast and using a well known API.
As a bonus, senpy services use semantic vocabularies (e.g. `NIF <http://persistence.uni-leipzig.org/nlp2rdf/>`_, `Marl <http://www.gsi.dit.upm.es/ontologies/marl>`_, `Onyx <http://www.gsi.dit.upm.es/ontologies/onyx>`_) and formats (turtle, JSON-LD, xml-rdf).

Have you ever wanted to turn your sentiment analysis algorithms into a service?
With senpy, now you can.
It provides all the tools so you just have to worry about improving your algorithms:

`See it in action. <http://senpy.cluster.gsi.dit.upm.es/>`_

Installation
------------
The stable version can be installed in three ways.

Through PIP
***********

.. code:: bash

   pip install -U --user senpy

   
Alternatively, you can use the development version:
 
.. code:: bash

   git clone http://github.com/gsi-upm/senpy
   cd senpy
   pip install --user .

If you want to install senpy globally, use sudo instead of the ``--user`` flag.

Docker Image
************
Build the image or use the pre-built one: ``docker run -ti -p 5000:5000 gsiupm/senpy --default-plugins``.

To add custom plugins, add a volume and tell senpy where to find the plugins: ``docker run -ti -p 5000:5000 -v <PATH OF PLUGINS>:/plugins gsiupm/senpy --default-plugins -f /plugins``


Developing
----------

Developing/debugging
********************
This command will run the senpy container using the latest image available, mounting your current folder so you get your latest code:

.. code:: bash


    # Python 3.5
    make dev
    # Python 2.7
    make dev-2.7

Building a docker image
***********************

.. code:: bash


    # Python 3.5
    make build-3.5
    # Python 2.7
    make build-2.7

Testing
*******

.. code:: bash


    make test

Running
*******
This command will run the senpy server listening on localhost:5000

.. code:: bash


    # Python 3.5
    make run-3.5
    # Python 2.7
    make run-2.7

Usage
-----

However, the easiest and recommended way is to just use the command-line tool to load your plugins and launch the server.

.. code:: bash


   senpy

or, alternatively:

.. code:: bash


    python -m senpy


This will create a server with any modules found in the current path.
For more options, see the `--help` page.

Alternatively, you can use the modules included in senpy to build your own application.

Deploying on Heroku
-------------------
Use a free heroku instance to share your service with the world.
Just use the example Procfile in this repository, or build your own.


`DEMO on heroku <http://senpy.herokuapp.com>`_


For more information, check out the `documentation <http://senpy.readthedocs.org>`_.
------------------------------------------------------------------------------------


Acknowledgement
---------------
This development has been partially funded by the European Union through the MixedEmotions Project (project number H2020 655632), as part of the `RIA ICT 15 Big data and Open Data Innovation and take-up` programme.


.. image:: img/me.png
    :target: http://mixedemotions-project.eu
    :height: 100px
    :alt: MixedEmotions Logo

.. image:: img/eu-flag.jpg
    :height: 100px
    :target: http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/index.html
