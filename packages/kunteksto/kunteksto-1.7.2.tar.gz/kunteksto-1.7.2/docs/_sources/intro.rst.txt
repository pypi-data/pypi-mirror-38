=============================
Introduction and Installation
=============================

Purpose
=======

**Kunteksto** (ˈkänˌteksto) [#f1]_ is a tool to translate simple CSV formatted data files into computable, 
semantically enhanced knowledge representations. As a foundation for **crowdsourced**, *automated knowledge base construction*; 
it provides a path for existing data sets to be used in conjunction with the emerging *graph data, model first* approach in analysis, 
general artificial intelligence (AGI), and decision support systems. This approach opens the door for the change to a *data-centric* 
world as opposed to the *application-centric* one we have now. This new approach enables automatic interoperability avoiding the data 
quality issues created through data migration, cleaning and massaging. See :ref:`mlai`  

The importance of how this simplifies query and analysis capabilities and improves data quality is discussed in foundational 
`S3Model <https://datainsights.tech/S3Model>`_ documentation and references. However, detailed understanding of S3Model is not 
required to understand and use the power of Kunteksto. Additional information on the datacentric movement can be found below [#f2]_

Target Audience
---------------
Kunteksto design is based on the ability for *domain experts* from any field, with very little programming ability to quickly 
annotate data extracts to improve the usability of the data.  Data engineers and data scientists can also benefit from Kunteksto 
in the same ways as domain experts. It just takes a bit more research to discover the semantics that the original domain experts 
usually have at hand.

.. _install:

Installation
============

Cross-Platform on Anaconda
--------------------------

Anaconda is the **preferred environment** for a tool like Kunteksto because it integrates easily with systems for domain experts, data engineers, and data scientists.

- `Download and install <https://www.continuum.io/downloads>`_ Anaconda Python 3.7+ for your platform.
- More detailed Anaconda instructions are `here <https://docs.continuum.io/anaconda/install/>`_  if you prefer.

.. note::
    Anaconda now offers to install the `VS Code editor <https://code.visualstudio.com/download>`_. Unless you already have a preferred text editor,
    this is a good choice.


- Open a terminal window and create a conda environment. On Windows it is best to open an *Anaconda Prompt* terminal from the Anaconda menu: 

.. code-block:: sh

    conda create -p kunteksto python=3 pycurl ujson

- Change to the directory

.. code-block:: sh
    
    cd kunteksto

.. _activate: Activate


- Activate the environment according to the instructions shown by Anaconda in the terminal window.

**Windows**

.. code-block:: sh

    activate <path/to/directory> 

**or Linux/MacOSX**

.. code-block:: sh

    source activate <path/to/directory> 

- Windows users **may** need to manually install the pycurl library using this command:

.. code-block:: sh

    conda install pycurl

trying will not damage anything but it may fail or just report that pycurl is the current version.

- install Kunteksto

.. code-block:: sh

    pip install kunteksto

These quick steps create a virtual environment in the subdirectory *kunteksto*. Once the environment is created, conda displays how to activate the environment. When activated then Kunteksto is installed in the subdirectory along with the environment. 

The last step is to do the :ref:`tutor`


Update to a New Version
=======================

When you want to upgrade to a new version of Kunteksto you can use the line below in your terminal where you have activated the virtual environment. 

.. code-block:: sh

    pip install  kunteksto --upgrade --no-cache-dir


Be certain that you remove any project based catalog files from the *kunteksto/catalogs* directory. For example the *Demo_catalog.xml* file.
 

What are all the files for?
===========================

Depending on how and where you installed Kunteksto you will see a varying number of files and subdirectories. Many of them may be part of the Anaconda environment, so we do not cover those.

Referenced from the *kunteksto* directory created at install time:

Files
-----

- README.md
    A brief explanation of Kunteksto's purpose and links to background information.

- LICENSE.txt
    A copy of the copyright notice and license.

- kunteksto.conf
    This file is the required configuration file for Kunteksto.

Directories
-----------

- example_data
    This directory contains information and sample data files for the tutorials. There is also an example of the completed Demo database, model, and data in the archive Demo_with_semantics.zip. 

- output
    The default location of all generated output from Kunteksto. This directory can be changed either via the configuration file or the command line. 

- catalogs
    This directory is where Kunteksto places XML catalog files used in the data validation process.

- s3model
    Support files required for operation.

    - s3model.owl - the core S3Model ontology.
    - s3model_3_1_0.xsd - the reference model schema version 3.1.0
    - s3model_3_1_0.rdf - the extracted semantics from the reference model schema version 3.1.0
    - s3model_3_1_0.xsl - a stylesheet providing visualization in a browser of the reference model schema version 3.1.0
    - dm-description.xsl - a stylesheet that provides for visualization in a browser of any S3Model data model. 
        Just place it in the same directory with the dm-{uuid}.xsd file and open the schema in a browser. 


.. rubric:: Footnotes

.. [#f1] S3Model is called the Esperanto of information management. Kunteksto is the Esperanto translation of the word *Context*. See `Wikipedia <https://simple.wikipedia.org/wiki/Esperanto>`_ for more information about the Esperanto language.

.. [#f2] 
    -  `The Estes Park Group <http://estesparkgroup.org/>`_ 
    -  `The Data-centric Manifesto <http://datacentricmanifesto.org/>`_  
    -  `Data-centric companies will devour competitors <https://goo.gl/xDcpZM>`_ 
    -  `The Data-Centric Revolution: Gaining Traction <https://goo.gl/zdRLm9>`_ 
    -  `The limits of deep learning <https://blog.keras.io/the-limitations-of-deep-learning.html>`_ 
    -  `The future of deep learning <https://blog.keras.io/the-future-of-deep-learning.html>`_