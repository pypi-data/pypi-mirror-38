
.. _advtutor:

==================
Advanced Tutorials
==================

Below are additional tutorials to perform after the **Getting Started** :ref:`tutor`.


It is suggested that you install one or more of the following databases for these tutorials.

`AllegroGraph <https://franz.com/agraph/downloads/?ui=new>`_ database for creating your semantic graph.

`BaseX <http://basex.org>`_ database for storing your XML documents.

`MarkLogic 9 <>` database can store all three types of content; XML, RDF and JSON and has many additional features.  


If you are not familiar with semantic graph databases please see the following links:

  - `AllegroGraph Documentation <https://allegrograph.com/support/documentation/current/agraph-introduction.html>`_ 
  - `MarkLogic Getting Started w/Semantics <https://docs.marklogic.com/guide/getting-started/semantics>`_ 


Prerequisites
=============

MarkLogic 9
-----------
See the `Installation instructions <https://docs.marklogic.com/guide/installation/intro>`_ for details.

BaseX
-----
BaseX requires Java 8 for your platform.

Please `download the ZIP file <http://basex.org/download/>`_ and extract it into your home directory. 

Start the server using the `Client/Server instructions <http://docs.basex.org/wiki/Startup>`_. You will use the client in later parts of the tutorial.  


AllegroGraph
------------

`Download and Install the server for your platform based on these instructions <https://franz.com/agraph/downloads/?ui=new>`_ . 

When asked for the superuser username and password use these:

.. code-block:: sh

    user: admin
    password: admin

If you use another username or password, you must edit the entries in kunteksto.conf using a text editor. See below for editing kunteksto.conf. 

When the server is installed and running, install the `Gruff GUI client <https://franz.com/agraph/gruff/download/index.clp?ui=new>`_ for AllegroGraph. You will use this later in the tutorials.


.. caution::

    Only edit the configuration file with a text editor. Do not use a word processing application such as MS Word or LibreOffice. There are many great text editors from which to choose.  Some favorites, in no particular order, are:

        - `Atom <https://atom.io/>`_
        - `VS Code <https://code.visualstudio.com/>`_
        - `Sublime <https://www.sublimetext.com/>`_



Configuration
-------------

Using a text editor, edit the *status* entries in kunteksto.conf for [BASEX] and [ALLEGROGRAPH]. Change them from INACTIVE to ACTIVE. When completed they should look like this:

For BaseX:

.. sourcecode:: text

    [BASEX]
    status: ACTIVE
    host: localhost
    port: 1984
    dbname: Kunteksto
    user: admin
    password: admin


For AllegroGraph:

.. sourcecode:: text

    [ALLEGROGRAPH]
    status: ACTIVE
    host: localhost
    port: 10035
    repo: Kunteksto
    user: admin
    password: admin



For MarkLogic:

.. sourcecode:: text

    [MARKLOGIC]
    status: ACTIVE
    loadxml: True
    loadrdf: True
    loadjson: True
    hostip: 192.168.25.120
    hostname: localhost.localdomain
    port: 8020
    dbname: Kunteksto
    forests: 2  
    user: admin
    password: admin


Most users will run MarkLogic on another networked machine or using VirtualBox with a CentOS installation. Use the IP Address 
of that machine or VirtualBox for the *hostip* value. 

The *port* is the location that Kunteksto will use to create your REST API for the DB. 

For the tutorials just leave the number of forests at 2. 

The host name can be found by going to http://<hostip>:8001/default.xqy then look in the box in the lower-right labeled **Hosts**. 
You probably only have one and it is labeled *Default* use this value.  


Unless you are using MarkLogic for JSON persistence you will likely want to turn off JSON generation.

.. sourcecode:: text

	; Default data formats to create. Values are True or False.
	; These can be changed in the UI before generating data. 
	xml: True
	rdf: True
	json: False





Database Checks
---------------
From the kunteksto directory run

.. code-block:: sh

    python utils/db_setup.py


.. warning::

    This python script tests the database connections and installs the S3Model ontology and 3.1.0 Reference Model RDF. 

    **It clears any previously stored data in the databases and reinstalls the required files.** 

During execution, the script displays several lines of output to the terminal. 
If you are using AllegroGraph and BaseX then look for *AllegroGraph connections are okay.* and *BaseX connections are okay.* or any lines that start with **ERROR:**.

The MarkLogic checks will display several lines of information as well. As long as the script ends with the message 
*Database Setup is finished.*  then everything went ok. 


.. caution::

    If you see the *okay* output lines and no **ERROR:** lines, then all went well. 
    Otherwise, you must troubleshoot these issues before continuing. 



Viewing the AllegroGraph RDF Repository
---------------------------------------

You can view the Kunteksto repository by using `this link <http://127.0.0.1:10035/#/repositories/Kunteksto>`_ in a browser. 
Right click and open it in a new tab. Then under **Explore the Repository** click the *View Triples* link. 
These triples are the S3Model ontology and the S3Model 3.1.0 RDF. These triples connect all of your RDF into a graph, 
even when they do not have other semantics linking them. 

You may also use the Gruff GUI Client to explore the respoitory at any time. See the `Franz, Inc. Learning Center <https://franz.com/agraph/gruff/learning-center.lhtml>`_ for more information.


Using Your Data in MarkLogic
----------------------------

The `MarkLogic Developer Network <https://developer.marklogic.com/>`_ is extensive. They provide an enormous amount of 
high quality training as well a number of open source tools to assit with data exploration and application design. 

Now you have high quality data in a knowledge graph. `BI Tools and MarkLogic NoSQL <https://www.youtube.com/watch?v=ndmHYcQU2d4>`_ 
demonstrates in less than 7 minutes how to use external tools to use your data. 

**The Tutorials begin here.**

.. _honeytutor:

US Honey Production
===================


.. include:: honey.rst



.. _tradetutor:

Global Commodity Trade Statistics
=================================


.. include:: trade.rst
