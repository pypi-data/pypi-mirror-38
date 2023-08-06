konst
==========


.. image:: https://travis-ci.com/yehonatanz/konst.svg?branch=master
    :target: https://travis-ci.com/yehonatanz/konst

.. image:: https://codecov.io/gh/yehonatanz/konst/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/yehonatanz/konst
  
.. image:: https://api.codeclimate.com/v1/badges/23274b375351ba37b8b2/maintainability
   :target: https://codeclimate.com/github/yehonatanz/konst/maintainability
   :alt: Maintainability


Effortless, meaningless, DRY constants

.. code-block:: python
    
    from konst.string import RED
    from konst.symbol import FLOWER
    
    assert RED == 'RED'
    assert FLOWER.name == 'FLOWER'
