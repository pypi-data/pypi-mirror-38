
.. warning::

	This dataset contains more than 8 million rows of data. If you are using the free version of AllegroGraphDB then processing this file will exceed the 5 million triples limit many times over. The file will still process and all of the XML files will be generated. However, most of the triples will not be stored in AllegroGraph.

	
The original data set is provided at `UNdata Comtrade <http://data.un.org/DataMartInfo.aspx#ComTrade>`_ site.

The best source (easiest download) of this data is the `Kaggle Competition <https://www.kaggle.com/unitednations/global-commodity-trade-statistics>`_


`Download the dataset <https://www.kaggle.com/unitednations/global-commodity-trade-statistics/data>`_ Extract the CSV data and place it the *kunteksto/example_data* directory.

The metadata (click on Data then on the Column Metadata tab) information may be useful in filling in the database *model* and *record* tables. However, it is somewhat incomplete. You can find more metadata information about this dataset in the `UNdata Glossary <https://comtrade.un.org/db/mr/rfGlossaryList.aspx#>`_. There is also a `knowledgebase <https://unstats.un.org/unsd/tradekb/Knowledgebase/901>`_ that describes how the data was collected and some hints on how to use it. Asyou can see, the metadata is not very organized nor is it computable. S3Model and related datacentric tools allow you to solve this issue with any data of interest. 

After you have downloaded the dataset from Kaggle or even a subset from the UNdata site; you are ready to proceed with the tutorial.


Following the same step by step procedures outlined in the *Getting Started* section.


- Navigate to the directory where you installed Kunteksto.

- Be certain the virtual environment is active.

.. caution::

    If you closed and reopened a new window, then you need to activate the environment again. Also, be sure that you are in the *kunteksto* directory. 


    **Windows**

    .. code-block:: sh

        activate <path/to/directory> 

    **or Linux/MacOSX**

    .. code-block:: sh

        source activate <path/to/directory> 


For this tutorial, you start Kunteksto in commandline mode. 

.. code-block:: sh

    kunteksto -m all -i example_data/commodity_trade_statistics_data.csv


Kunteksto takes a few minutes analyzing the input file and creates a results database in the *output* directory.

The database editor opens and just like in the previous tutorial, prompts you for model metadata which you can collect from the links above.

.. caution::

	As you edit the data for each column, be sure to persist your changes using the **Save** button before advancing to the **Next** column. 


As before, each column is presented for you to add constraints and metadata from the information you collect from the links above or from your own personal knowledge. Remember, this is *your* model of this data. Using the best details creates the best models.

Be sure to check the datatype detected of columns as well as value constraints. For example the "The year" column is detected as an integer column. Obviously this is not valid. For temporals, Kunteksto only offers data, time and datetime options. Using the Datacentric Tool Suite would allow you to create this properly as a *Year* datatype column. So, using Kunteksto you must choose the most appropriate which in this case is more likely to be *String*.

Often we must be creative when deciding which URI to use for a Defining URL. Our suggested approach when you do not have a specific, online vocabulary or ontology is to use resources such as the glossary mentioned above. For the *The Year* column we might use https://comtrade.un.org/db/mr/rfGlossaryList.aspx#Year for the Defining URL and then copy the description from that row in the table. 

In the Predicates & Objects we can use

.. code-block:: sh

	skos:exactMatch http://www.w3.org/2001/XMLSchema#gYear

Go through each of the column definitions and complete as many data points about each column as you can and that make sense.
For example, changing the *The weight kg* column from String to Decimal will help detect missing or invalid values. Then add the 'kg' for the units.


The output RDF will be in the Kunteksto repository in AllegroGraph which you can explore through the AllegroGraph WebView browser tool or using `Gruff <https://franz.com/agraph/gruff/>`_ which I **HIGHLY** recommend. You can also explore the XML using the `BaseX GUI <http://basex.org/basex/gui/>`_. 

There are many written and video tutorials on using these tools. Check the `AllegroGraph YouTube Channel <https://www.youtube.com/user/AllegroGraph/videos>`_ and the `BaseX Getting Started <http://docs.basex.org/wiki/Getting_Started>`_.


