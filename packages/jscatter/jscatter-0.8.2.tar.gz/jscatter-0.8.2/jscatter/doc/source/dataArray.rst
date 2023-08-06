dataArray
=========

.. currentmodule:: jscatter.dataarray

.. include:: ../../dataarray.py
    :start-after: **dataArray**
    :end-before:  **dataList**

Class
-----
.. autosummary::
    dataArray

- dataArray creating by js.dA('filename.dat') or from numpy arrays.
- Array columns can be accessed as automatic generated attributes like *.X,.Y,.eY* (see protectedNames).
  or by incexing as *data[0] -> .X *
- Corrsponding column indices are set by :py:meth:`dataArray.setColumnIndex` (default X,Y,eY = 0,1,2).
- .Y are used as function values at coordinates [.X,.Z,.W] in fitting.
- Attributes can be set like:  data.aName= 1.2345


Attributes
----------
.. autosummary::
        protectedNames

.. autosummary::

        dataArray.showattr
        dataArray.attr
        dataArray.getfromcomment
        dataArray.extract_comm
        dataArray.resumeAttrTxt
        dataArray.setattr
        dataArray.setColumnIndex
        dataArray.name
        dataArray.array
        dataArray.argmax
        dataArray.argmin

Fitting
-------
.. autosummary::

        dataArray.fit
        dataArray.modelValues
        dataArray.setLimit
        dataArray.hasLimit
        dataArray.setConstrain
        dataArray.hasConstrain
        dataArray.makeErrPlot
        dataArray.makeNewErrPlot
        dataArray.killErrPlot
        dataArray.detachErrPlot
        dataArray.showlastErrPlot
        dataArray.savelastErrPlot

Housekeeping
------------
.. autosummary::

        dataArray.savetxt
        dataArray.isort
        dataArray.where
        dataArray.prune
        dataArray.merge
        dataArray.concatenate
        dataArray.interpolate
        dataArray.interpAll
        dataArray.interp
        dataArray.polyfit
        dataArray.addZeroColumns
        dataArray.addColumn
        dataArray.nakedCopy

Convenience
-----------
.. autosummary::
    
        zeros
        ones
        fromFunction

-----

.. autodata:: jscatter.dataarray.protectedNames

.. autoclass:: jscatter.dataarray.dataArray
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

.. automethod:: jscatter.dataarray.zeros
.. automethod:: jscatter.dataarray.ones
.. automethod:: jscatter.dataarray.fromFunction

