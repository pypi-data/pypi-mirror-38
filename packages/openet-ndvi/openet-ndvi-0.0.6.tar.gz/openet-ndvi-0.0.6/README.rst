======================
OpenET - NDVI ET Model
======================

|version| |build|

This repository provides an Earth Engine Python API based implementation of a simple model for computing evapotranspiration (ET) as a linear function of NDVI.

Model Structure
===============



Examples
========

Computing an ET fraction image using the Landsat C1 TOA helper method

.. code-block:: console

    import openet.ndvi as ndvi_et

    landat_img = ee.Image('LANDSAT/LC08/C01/T1_RT_TOA/LC08_044033_20170716')
    etf_img = ndvi_et.Image().from_landsat_c1_toa(landat_img).etf

The Image class can also be initialized directly from an NDVI image (the band must be called "ndvi").

.. code-block:: console

    import openet.ndvi as ndvi_et

    ndvi_img = ee.Image('LANDSAT/LC08/C01/T1_RT_TOA/LC08_044033_20170716')\
        .normalizedDifference(['B4', 'B5'])
    etf_img = ndvi_et.Image(input_img).etf

Notebooks
---------

Detailed Jupyter notebook examples can be found in the examples folder.

Installation
============

The OpenET NDVI based ET python module can be installed via pip:

.. code-block:: console

    pip install openet-ndvi

Dependencies
============

Modules needed to run the model:

 * `earthengine-api <https://github.com/google/earthengine-api>`__
 * `openet <https://github.com/Open-ET/openet-core-beta>`__

OpenET Namespace Package
========================

Each OpenET model should be stored in the "openet" folder (namespace).  The benefit of the namespace package is that each ET model can be tracked in separate repositories but called as a "dot" submodule of the main openet module,

.. code-block:: console

    import openet.ndvi as ndvi

.. |build| image:: https://travis-ci.org/Open-ET/openet-ndvi-beta.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.org/Open-ET/openet-ndvi-beta
.. |version| image:: https://badge.fury.io/py/openet-ndvi.svg
   :alt: Latest version on PyPI
   :target: https://badge.fury.io/py/openet-ndvi
