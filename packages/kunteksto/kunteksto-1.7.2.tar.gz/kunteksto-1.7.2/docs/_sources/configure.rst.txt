=============
Configuration
=============

.. warning::

    Only edit the configuration file with a text editor. Do not use a word processing application such as MS Word or LibreOffice. There are many great opensource and free text editors from which to choose.  Some favorites, in no particular order, are:

    - `Atom <https://atom.io/>`_
    - `VS Code <https://code.visualstudio.com/>`_
    - `Sublime <https://www.sublimetext.com/>`_

The initial kunteksto.conf file should be okay for most uses and indeed for this initial tutorial. You are encouraged to make backup copies, under different names, of the configuration file for different use cases/projects. The active configuration, however, is always the one named **kunteksto.conf**. Kunteksto ships with a copy of the original config file named *default.conf* as well as a config file for the advanced tutorials named *advanced_tutorials.conf*. You can always go back to the initial settings by making a copy of the *default.conf* file and naming it *kunteksto.conf*.

.. _config:

Config File Details
===================
Here we cover the details of the configuration options. 


.. sourcecode:: text

    [KUNTEKSTO]
    
    ; analyzelevel can be either Simple or Full.
    analyzelevel: Full

    ; allowed delimiter (field separator) types are one of these:  , ; : | $ 
    ; The default delimiter is defined here.
    delim: ;

    ; A default output directory may be defined here. It can be overridden on the command line.
    ; The 'output' directory is relative to the installation directory of Kunteksto. 
    ; Typically it is only used for the Demo and Tutorials.
    outdir: output

These three items are also available on the command line. A command line entry overrides these defaults.


.. sourcecode:: text


    ; Default data formats to create. Values are True or False.
    xml: True
    rdf: True
    json: True

These values determine what data file format(s) are generated.  If a file format is set to *True* and no repository is configured for that format; then the files are written to the filesystem under the defined *outdir*.  


.. sourcecode:: text


    [NAMESPACES]
    ; any additional namespaces must be defined here with their abbreviations. The format is shown below. Note the space after the colon.
    ; {abbrev}: {namespace URI}

    dul: http://www.ontologydesignpatterns.org/ont/dul/DUL.owl# 

When defining the semantics for your models, you should use appropriate ontologies from various public sources such as `Linked Open Vocabularies <http://lov.okfn.org/dataset/lov>`_  `Biontology <https://www.bioontology.org/>`_ or some of the many others, as well as your local ontologies. You must define an abbreviation for each ontology namespace here. The one above shows the example from the Tutorial/Demo of defining the *dul* abbreviation for the `Ontology Design Patterns <http://ontologydesignpatterns.org/wiki/Main_Page>`_ ontology.  

.. sourcecode:: text


    ; Below are where repository setup definitions for each of the three types of data generation are expressed.
    ; If a type is to be generated, but no repository is defined for the type. Then the data is generated 
    ; and written to the filesystem in a subdirectory of the output directory.  


    ; A default repository where we can write the output XML instead of to the filesystem.
    ; The config processes only the first one with an ACTIVE status. 

    [BASEX]
    status: INACTIVE
    host: localhost
    port: 1984
    dbname: S3M_test
    user: admin
    pw: admin

    ; Not Yet Implemented
    [EXISTDB]
    status: INACTIVE


    ; A default repository where we can write the output RDF instead of to the filesystem.
    ; The config processes only the first one with an ACTIVE status. 
     

    [ALLEGROGRAPH]
    status: INACTIVE
    host: localhost
    port: 10035
    repo: S3M_test
    user: admin
    pw: admin

    ; Not Yet Implemented
    [STARDOG]
    status: INACTIVE

    ; Not Yet Implemented
    [BLAZEGRAPH]
    status: INACTIVE

    ; Not Yet Implemented
    [GRAPHDB]
    status: INACTIVE


    ; A default repository where we can write the output JSON instead of to the filesystem.
    ; The config processes only the first one with an ACTIVE status. 

    [MONGODB]
    status: INACTIVE
    host: localhost
    port: 27017
    dbname: S3M_test
    ; default MongoDB has no authentication requirements.
    user: admin
    pw: admin

    ; Not Yet Implemented
    [COUCHDB]
    status: INACTIVE

There is currently one repository supported for each filetype. We plan to support the others in the future. 


**There are no options editable by the user in the SYSTEM section.**

.. sourcecode:: text


    [SYSTEM]
    version: 1.7.1  
    rmversion: 3.1.0

The *version* is the current version of Kunteksto.
The *rmversion* is the version of the S3Model Reference Model that is used for generated data models and RDF. 
