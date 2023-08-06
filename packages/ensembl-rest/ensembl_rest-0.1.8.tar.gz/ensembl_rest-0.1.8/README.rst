
Ensembl-REST
============

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/Ad115

A Python interface to the Ensembl REST APIs. A whole world of biological data 
at your fingertips.

The `Ensembl database <https://www.ensembl.org/index.html>`__ contains
reference biological data on almost any organism. Now it is easy to
access this data programatically through their REST API.

The full list of endpoints for the Ensembl REST API endpoints along with 
endpoint-specific documentation can be found on `their website 
<https://rest.ensembl.org/>`__.

This library also includes some utilities built on top of the APIs designed to
ease working with them, including an `AssemblyMapper 
<https://ad115.github.io/EnsemblRest/#ensembl_rest.AssemblyMapper>`__ class 
that helps in the conversion between different genome assemblies.


This project uses code from `RESTEasy <https://github.com/rapidstack/RESTEasy>`__,
which made my life much easier. Thanks!



Installation
------------

You can install from `PyPI <https://pypi.org/project/ensembl-rest/>`_::

    $ pip install ensembl_rest


Examples
========

The library exports two main classes: ``ensembl_rest.EnsemblClient`` and
``ensembl_rest.EnsemblGenomesClient`` that point respectively to the `main
REST API <http://rest.ensembl.org/>`__ and to the `Ensembl Genomes REST
API <http://rest.ensemblgenomes.org/>`__.

.. code-block:: python

    >>> import ensembl_rest
    
    >>> client = ensembl_rest.EnsemblClient()

If you want to use a method from the REST API, say:
``GET lookup/symbol/:species/:symbol`` 
(http://rest.ensembl.org/documentation/info/symbol\_lookup) then the 
corresponding method on the class is called after the last string in the link 
to the documentation page, in this case, ``symbol_lookup``.

.. code-block:: python

    >>> help(client.symbol_lookup)


::

    Help on method symbol_lookup in module ensembl_rest.core.baseclient:
    
    symbol_lookup(*args, **kwargs) method of ensembl_rest.core.baseclient.EnsemblClient instance
        ``GET lookup/symbol/:species/:symbol``
        
        Find the species and database for a symbol in a linked external database
        - More info: https://rest.ensembl.org/documentation/info/symbol_lookup
    


We can see from the resource string ``GET lookup/symbol/:species/:symbol`` that
this method contains 2 parameters called species and symbol, so we can call the
method in the following way:

.. code-block:: python

    >>> client.symbol_lookup(species='homo sapiens',
                             symbol='TP53')
    
    # Or like this...
    >>> client.symbol_lookup('homo sapiens', 'TP53')


::

   {'source': 'ensembl_havana',
     'object_type': 'Gene',
     'logic_name': 'ensembl_havana_gene',
     'version': 14,
     'species': 'human',
     'description': 'BRCA2, DNA repair associated [Source:HGNC Symbol;Acc:HGNC:1101]',
     'display_name': 'BRCA2',
     'assembly_name': 'GRCh38',
     'biotype': 'protein_coding',
     'end': 32400266,
     'seq_region_name': '13',
     'db_type': 'core',
     'strand': 1,
     'id': 'ENSG00000139618',
     'start': 32315474}

One can pass request parameters to modify the response with the ``params`` 
keyword (the specific parameters to pass depend on the specific endpoint, 
the official endpoints documentation can be found `here 
<http://rest.ensemblgenomes.org/>`__, the parameters to be passed this way are 
the optional ones for each endpoint):

.. code-block:: python

        >>> client.symbol_lookup('human', 'BRCA2', params={'expand':True})

::


    {'source': 'ensembl_havana',
     'object_type': 'Gene',
     'logic_name': 'ensembl_havana_gene',
     'seq_region_name': '13',
     'db_type': 'core',
     'strand': 1,
     'id': 'ENSG00000139618',
     'Transcript': [{'source': 'ensembl_havana',
       'object_type': 'Transcript',
       'logic_name': 'ensembl_havana_transcript',
       'Exon': [{'object_type': 'Exon',
         'version': 4,
         'species': 'human',
         'assembly_name': 'GRCh38',
         ...
         ...
         ...
     'biotype': 'protein_coding',
     'start': 32315474}
         

In that way, you can pass the parameters for the POST endpoints, such as:

.. code-block:: python

    >>> client.symbol_post(species='human',
                           params={'symbols': ["BRCA2", 
                                               "TP53", 
                                               "BRAF" ]})

::

    {
        "BRCA2": {
            "source": "ensembl_havana",
            "object_type": "Gene",
            "logic_name": "ensembl_havana_gene",
            "version": 14,
            "species": "homo_sapiens",
            "description": "BRCA2, DNA repair associated [Source:HGNC Symbol;Acc:HGNC:1101]",
            ...
        },
        "TP53": {
            ...
        }.
        "BRAF": {
            ...
            "strand": -1,
            "id": "ENSG00000157764",
            "start": 140719327
        }
    }

Another common usage is to fetch sequences of known genes:

.. code-block:: python

    >>> client.sequence_id('ENSG00000157764')


::

    {'desc': 'chromosome:GRCh38:7:140719327:140924928:-1',
     'query': 'ENSG00000157764',
     'version': 13,
     'id': 'ENSG00000157764',
     'seq': 'TTCCCCCAATCCCCTCAGGCTCGGCTGCGCCCGGGGC...ACTGCTATAATAAAGATTGACTGCATGGAGAAGTCTTCA',
     'molecule': 'dna'}



Or to map betweeen assemblies...

.. code-block:: python

    >>> client.assembly_map(species='human',
                            asm_one='GRCh37',
                            region='X:1000000..1000100:1',
                            asm_two='GRCh38')
    
    
    # Or...
    >>> region_str = ensembl_rest.region_str(chom='X',
                                             start=1000000,
                                             end=1000100)
    
    >>> client.assembly_map(species='human',
                            asm_one='GRCh37',
                            region=region_str,
                            asm_two='GRCh38')

::

    {'mappings': [{'original': {'seq_region_name': 'X',
        'strand': 1,
        'coord_system': 'chromosome',
        'end': 1000100,
        'start': 1000000,
        'assembly': 'GRCh37'},
       'mapped': {'seq_region_name': 'X',
        'strand': 1,
        'coord_system': 'chromosome',
        'end': 1039365,
        'start': 1039265,
        'assembly': 'GRCh38'}}]}


The above problem (mapping from one assembly to another) is so frequent that 
the library provides a specialized class ``AssemblyMapper`` to efficiently
mapping large amounts of regions between assemblies. This class avoids the 
time-consuming task of making a web request every time a mapping is needed by 
fetching the mapping of the whole assembly right from the instantiation. This 
is a time-consuming operation by itself, but it pays off when one has to 
transform repeatedly betweeen assemblies.::


        >>> mapper = ensembl_rest.AssemblyMapper(from_assembly='GRCh37'
        ...                                      to_assembly='GRCh38')
        
        >>> mapper.map(chrom='1', pos=1000000)
        1064620

        
        
Meta
====

**Author**: `Ad115 <https://agargar.wordpress.com/>`_ -
`Github <https://github.com/Ad115/>`_ – a.garcia230395@gmail.com

**Project pages**: 
`Docs <https://ensemblrest.readthedocs.io>`__ - `@GitHub <https://github.com/Ad115/EnsemblRest/>`__ - `@PyPI <https://pypi.org/project/ensembl-rest/>`__

Distributed under the MIT license. See
`LICENSE <https://github.com/Ad115/EnsemblRest/blob/master/LICENSE>`_
for more information.

Contributing
============

1. Check for open issues or open a fresh issue to start a discussion
   around a feature idea or a bug.
2. Fork `the repository <https://github.com/Ad115/EnsemblRest/>`_
   on GitHub to start making your changes to a feature branch, derived
   from the **master** branch.
3. Write a test which shows that the bug was fixed or that the feature
   works as expected.
4. Send a pull request and bug the maintainer until it gets merged and
   published.
