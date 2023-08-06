PySPH: a Python-based SPH framework
------------------------------------

|Travis Status|  |Shippable Status|  |Appveyor Status|  |Codeship Status|

**PySPH has moved here:** https://github.com/pypr/pysph

PySPH is an open source framework for Smoothed Particle Hydrodynamics
(SPH) simulations. It is implemented in
`Python <http://www.python.org>`_ and the performance critical parts
are implemented in `Cython <http://www.cython.org>`_ and PyOpenCL_.

PySPH allows users to write their high-level code in pure Python. This Python
code is automatically converted to high-performance Cython or OpenCL which is
compiled and executed. PySPH can also be configured to work seamlessly with
OpenMP, OpenCL, and MPI.

The latest documentation for PySPH is available at
`pysph.readthedocs.org <http://pysph.readthedocs.org>`_.

.. |Travis Status| image:: https://travis-ci.org/pypr/pysph.svg?branch=master
    :target: https://travis-ci.org/pypr/pysph
.. |Shippable Status| image:: https://api.shippable.com/projects/59272c73b2b3a60800b215d7/badge?branch=master
   :target: https://app.shippable.com/github/pypr/pysph
.. |Codeship Status| image:: https://app.codeship.com/projects/37370120-23ab-0135-b8f4-5ed227e7b019/status?branch=master
   :target: https://codeship.com/projects/222098
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/q7ujoef1xbguk4wx
   :target: https://ci.appveyor.com/project/prabhuramachandran/pysph-00bq8

Here are `videos
<https://www.youtube.com/playlist?list=PLH8Y2KepC2_VPLrcTiWGaYYh88gGVAuVr>`_
of some example problems solved using PySPH.


.. _PyOpenCL: https://documen.tician.de/pyopencl/

Features
--------

- Flexibility to define arbitrary SPH equations operating on particles
  in pure Python.
- Define your own multi-step integrators in pure Python.
- High-performance: our performance is comparable to hand-written
  solvers implemented in FORTRAN.
- Seamless multi-core support with OpenMP.
- Seamless GPU support with PyOpenCL_.
- Seamless parallel support using
  `Zoltan <http://www.cs.sandia.gov/zoltan/>`_.

SPH formulations
-----------------

PySPH ships with a variety of standard SPH formulations along with
basic examples.  Some of the formulations available are:

-  `Weakly Compressible SPH
   (WCSPH) <http://www.tandfonline.com/doi/abs/10.1080/00221686.2010.9641250>`_
   for free-surface flows (Gesteira et al. 2010, Journal of Hydraulic
   Research, 48, pp. 6--27)
-  `Transport Velocity
   Formulation <http://dx.doi.org/10.1016/j.jcp.2013.01.043>`_ for
   incompressilbe fluids (Adami et al. 2013, JCP, 241, pp. 292--307)
-  `SPH for elastic
   dynamics <http://dx.doi.org/10.1016/S0045-7825(01)00254-7>`_ (Gray
   et al. 2001, CMAME, Vol. 190, pp 6641--6662)
-  `Compressible SPH <http://dx.doi.org/10.1016/j.jcp.2013.08.060>`_
   (Puri et al. 2014, JCP, Vol. 256, pp 308--333)

Installation
-------------

Up-to-date details on how to install PySPH on Linux/OS X and Windows are
available from
`here <http://pysph.readthedocs.org/en/latest/installation.html>`_.

If you wish to see a working build/test script please see our `shippable.yml
<https://github.com/pypr/pysph/blob/master/shippable.yml>`_. For
Windows platforms see the `appveyor.yml
<https://github.com/pypr/pysph/blob/master/appveyor.yml>`_.

Running the examples
--------------------

You can verify the installation by exploring some examples. A fairly
quick running example (taking about 20 seconds) would be the
following::

    $ pysph run elliptical_drop

This requires that Mayavi be installed. The saved output data can be
viewed by running::

    $ pysph view elliptical_drop_output/

A more interesting example would be a 2D dam-break example (this takes about 30
minutes in total to run)::

    $ pysph run dam_break_2d

The solution can be viewed live by running (on another shell)::

    $ pysph view

The generated output can also be viewed and the newly generated output files
can be refreshed on the viewer UI.

A 3D version of the dam-break problem is also available, and may be run
as::

    $ pysph run dam_break_3d

This runs the 3D dam-break problem which is also a SPHERIC benchmark
`Test 2 <https://wiki.manchester.ac.uk/spheric/index.php/Test2>`_

.. figure:: https://github.com/pypr/pysph/raw/master/docs/Images/db3d.png
   :width: 550px
   :alt: Three-dimensional dam-break example

PySPH is more than a tool for wave-body interactions:::

    $ pysph run cavity

This runs the driven cavity problem using the transport velocity formulation of
Adami et al. The output directory ``cavity_output`` will also contain
streamlines and other post-processed results after the simulation completes.
For example the streamlines look like the following image:

.. figure:: https://github.com/pypr/pysph/raw/master/docs/Images/ldc-streamlines.png
   :width: 550px
   :alt: Lid-driven-cavity example

If you want to use PySPH for elastic dynamics, you can try some of the
examples from the ``pysph.examples.solid_mech`` package::

    $ pysph run solid_mech.rings

Which runs the problem of the collision of two elastic rings:

.. figure:: https://github.com/pypr/pysph/raw/master/docs/Images/rings-collision.png
   :width: 550px
   :alt: Collision of two steel rings

The auto-generated code for the example resides in the directory
``~/.pysph/source``. A note of caution however, it's not for the faint
hearted.

There are many more examples, they can be listed by simply running::

    $ pysph run


Credits
--------

PySPH is primarily developed at the `Department of Aerospace
Engineering, IIT Bombay <http://www.aero.iitb.ac.in>`_. We are grateful
to IIT Bombay for their support.  Our primary goal is to build a
powerful SPH based tool for both application and research. We hope that
this makes it easy to perform reproducible computational research.

To see the list of contributors the see `github contributors page
<https://github.com/pypr/pysph/graphs/contributors>`_


Some earlier developers not listed on the above are:

- Pankaj Pandey (stress solver and improved load balancing, 2011)
- Chandrashekhar Kaushik (original parallel and serial implementation in 2009)


Support
-------

If you have any questions or are running into any difficulties with PySPH,
please email or post your questions on the pysph-users mailing list here:
https://groups.google.com/d/forum/pysph-users

Please also take a look at the `PySPH issue tracker
<https://github.com/pypr/pysph/issues>`_.
