
The source of this data is from the `Kaggle project <https://www.kaggle.com/jessicali9530/honey-production>`_

`The dataset is available here <https://www.kaggle.com/jessicali9530/honey-production/data>`_. 

Download **honeyproduction.csv** data set for this tutorial and place it in the  *kunteksto/example_data* directory.

For those without an account on Kaggle, we have included a copy in the example_data directory.

The metadata (click on Data then on the Column Metadata tab) information is useful when filling in the database *model* and *record* tables. 

You can find more metadata information about this dataset in `Wrangling The Honey Production Dataset <https://www.kaggle.com/jessicali9530/wrangling-the-honey-production-dataset/data>`_. 


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


For this tutorial, you will run Kunteksto in commandline mode. 

.. code-block:: sh

    kunteksto -m all -i example_data/honeyproduction.csv


Kunteksto takes a few minutes analyzing the input file and creates a results database in the *output* directory.

The database editor opens and just like in the previous tutorial, prompts you for model metadata which you can collect from the links above.
After you click the *Save & Exit* button. The column editor will open.

.. caution::

	As you edit the data for each column, be sure to persist your changes using the **Save** button before advancing to the **Next** column. 


As before, each column is presented for you to add constraints and metadata from the information you collect from the links above or from your own personal knowledge. Remember, this is *your* model of this data. Using the best details creates the best models.

Often we must be creative when deciding which URI to use for a Defining URL. Our suggested approach when you do not have a specific, online vocabulary or ontology is to use resources such as the metadata mentioned above. 

For the *The state* column we might use https://www.kaggle.com/jessicali9530/honey-production/data#state for the Defining URL and then copy the description from that row in the Column Metadata tab. 

For additional semantics (Predicates & Objects box) it is best to use `open vocabularies <https://lov.okfn.org/dataset/lov/>`_ when possible. This gives you the ability to easily connect data across models. If you go to the link for open vocabularies and type "State" into the search box you will see a list of options to choose from. A good choice here is to use the one from Schema.org because this is a popular vocabulary for website mark up. We have an *Object* now we need a *Predicate*. Since we want to indicate that this is the meaning of this item, type *meaning of* into the search box on the open vocabularies site. Notice that rdf:type is one of the first choices and the description makes sense. If you put together the two description phrases you get; "The subject is an instance of a class" "A state or province of a country". The values in this column are instances of (a representation) of a state or province. Therefore we have a good match. 


In the Predicates & Objects enter:

.. code-block:: sh

    rdf:type http://schema.org/State

Click the *Save* button, then the *Next* button to move to the *The numcol* column. Looking at the meatdata you may choose to change the label to something more readable, like *Colonies*.   

Go through each of the column definitions and complete as many data points about each column as you can and that make sense. Feel free to use meaning names as the labels.

Remember also that numeric columns need a Units designator. Also some columns may be detected as integer or decimal and the range of values are outside the boundaries of those types. In this case be sure to change the type to *Float*.


Columns like *The year* are detected as integers. However, this is really a temporal value. In Kunteksto we cannot have a temporal datatype with just a year. So change this to *String* and in the Predicates and Objects box use  

.. code-block:: sh

    rdf:type http://www.w3.org/2001/XMLSchema#gYear


.. note::

    In `S3Model <https://datainsights.tech/S3Model/>`_ it is possible to have all of the temporal types. The `Datacentric Tools Suite <https://datainsights.tech/datacentrictools/>`_ provides facilities to create these datatypes. 

Once you complete editing of all of the columns, click the *Exit* button. The GUI will remain on the screen while the data generation process is running. The terminal where you started Kunteksto will scroll messages about the progress. 

After the processing is complete review *output/honeyproduction/honeyproduction_validation_log.csv* to see which files are invalid. 
The error message from the validator may be a bit cryptic but it's what we have to work with. Just like with the Demo tutorial, the errors are also included in the Semantic Graph via the RDF.

The output RDF will be in the Kunteksto repository in AllegroGraph which you can explore through the AllegroGraph WebView browser tool or using `Gruff <https://franz.com/agraph/gruff/>`_ which I **HIGHLY** recommend. You can also explore the XML using the `BaseX GUI <http://basex.org/basex/gui/>`_. 

There are many written and video tutorials on using these tools. Check the `AllegroGraph YouTube Channel <https://www.youtube.com/user/AllegroGraph/videos>`_ and the `BaseX Getting Started <http://docs.basex.org/wiki/Getting_Started>`_.


