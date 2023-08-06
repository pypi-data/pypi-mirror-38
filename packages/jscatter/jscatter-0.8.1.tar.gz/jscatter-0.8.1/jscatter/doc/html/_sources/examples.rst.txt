.. _label_Examples:

Examples
========

These examples show how to use Jscatter. Use  *showExampleList* to get a full list.
Maybe first study the :ref:`Beginners Guide / Help`

Examples are mainly based on XmGrace for ploting as this is more convenient for
interactive inspection of data and used for the shown plots.

Matplotlib can be used by setting ``usempl=True`` in ``runExample`` and ``showExample`` (automatically set if Grace not present).
With matplotlib the plots are not optimized but still show the possibilities.

Image quality is for HTML.
Fileformats in XmGrace can jpg, png eps,pdf.... in high resolution in publication quality.

For publication use .eps or .pdf with image width 8.6 cm and 600 dpi (see ``.save`` of a plot).

The shown examples can be run by copy and pasting to a shell or by using
``js.example.runExample(17)``

.. automodule:: jscatter.examples
    :noindex:

.. autosummary::
    showExampleList
    showExample
    runExample
    runAll


In a hurry and short 
--------------------
Daily use example to show how short it can be.

Comments are shown in next examples.

.. literalinclude:: ../../examples/example_daily_use.py
    :language: python
.. image:: ../../examples/DiffusionFit_ErrPlot.jpg
    :align: left
    :height: 300px
    :alt: Picture about diffusion fit with residuals
.. image:: ../../examples/DiffusionFit.jpg
    :align: center
    :height: 300px
    :alt: Picture about diffusion fit
.. image:: ../../examples/effectiveDiffusion.jpg 
    :align: center
    :height: 300px
    :alt: diffusion fit result

How to build simple models
----------------------------
.. literalinclude:: ../../examples/example_buildsimpleModels.py
    :language: python

How to build a more complex model
---------------------------------
.. literalinclude:: ../../examples/example_buildComplexModel.py
    :language: python
.. image:: ../../examples/interactingParticles.jpeg
    :align: center
    :height: 300px
    :alt: Image of interacting particles scattering

Some Sinusoidal fits with different kinds to use data attributes
----------------------------------------------------------------
.. literalinclude:: ../../examples/example_SinusoidalFitting.py
    :language: python
.. image:: ../../examples/SinusoidalFit.png
    :align: left
    :height: 300px
    :alt: SinusoidialFit
.. image:: ../../examples/Sinusoidal3D.png
    :align: center
    :height: 300px
    :alt: Sinusoidial3D


Simple diffusion fit of not so simple diffusion case
----------------------------------------------------
Here the long part with description from the first example.

This is the diffusion of a protein in solution. This is NOT constant as for Einstein diffusion.

These simulated data are similar to data measured by Neutron Spinecho Spectroscopy, which measures on the length scale
of the protein and therefore also rotational diffusion contributes to the signal.
At low wavevectors additional the influence of the structure factor leads to an upturn,
which is neglected in the simulated data.
To include the correction :math:`D_T(q)=D_{T0} H(q)/S(q)` look at :func:`~.structurefactor.hydrodynamicFunct`.

For details see this tutorial review `Biehl et al. Softmatter 7,1299 (2011) <http://juser.fz-juelich.de/record/11985/files/FZJ-11985.pdf>`_


.. literalinclude:: ../../examples/example_simple_diffusion.py
    :language: python
    :lines: 1-42
.. image:: ../../examples/DiffusionFit.jpg
    :align: center
    :height: 300px
    :alt: Picture about diffusion fit

.. literalinclude:: ../../examples/example_simple_diffusion.py
    :language: python
    :lines: 45-
.. image:: ../../examples/effectiveDiffusion.jpg 
    :align: center
    :height: 300px
    :alt: diffusion fit result


How to smooth Xray data and make an inset in the plot
-----------------------------------------------------

.. literalinclude:: ../../examples/example_smooth_xraydata.py
    :language: python
.. image:: ../../examples/smoothedXraydata.jpg
    :align: center
    :height: 300px
    :alt: Picture about diffusion fit

Analyse SAS data
----------------
In small angle scattering a typical situation is that you want to measure a formfactor (particle shape)
or structure factor (particle interaction). For this a concentration series is measured and
we need to extrapolate to zero concentration to get the formfactor.
Afterwards we can divide the measurement by the formfactor to get the structure factor.
So we have three key parts :
    - Correction for transmission, dark and empty cell scattering to get instrument independent datasets.
    - Extrapolating concentration scaled data to get the formfactor.
    - Divide by formfactor to get structure factor

**Correction**

Brulet at al [1]_ describe the data correction for SANS, which is in principle also valid for SAXS,
if incoherent contributions are neglected.

The difference is, that SAXS has typical transmission around ~0.3 for 1mm water sample in quartz cell
due to absorption, while in SANS typical values are around ~0.9 for D2O.
Larger volume fractions in the sample play a more important rule for SANS as hydrogenated ingredients
reduce the transmission significantly, while in SAXS still the water and the cell (quartz) dominate.

One finds for a sample inside of a container with thicknesses (:math:`z`)
for sample, buffer (solvent), empty cell and empty beam measurement (omitting the overall q dependence):

.. math:: I_s = \frac{1}{z_S}\big((\frac{I_S-I_{dark}}{T_S}-I_{b}T_S\big) -\big(\frac{I_{EC}-I_{dark}}{T_{EC}}-I_{b}T_{EC})\big) -
                \frac{1}{z_B}\big((\frac{I_B-I_{dark}}{T_B}-I_{b}T_B\big) -\big(\frac{I_{EC}-I_{dark}}{T_{EC}}-I_{b}T_{EC})\big)

where
 - :math:`I_s`      is the interesting species
 - :math:`I_S`      is the sample of species in solvent (buffer)
 - :math:`I_B`      is the pure solvent (describing a constant background)
 - :math:`I_{dark}` is the dark current measurement
 - :math:`I_b`      is the empty beam measurement
 - :math:`I_{EC}`   is the empty cell measurement
 - :math:`z_x`      corresponding sample thickness
 - :math:`T_x`      corresponding transmission

The recurring pattern :math:`\big((\frac{I-I_{dark}}{T}-I_{b}T\big)` shows that the the beam tail
(border of primary beam not absorbed by the beam stop) is attenuated by the corresponding sample.

For equal sample thickness :math:`z` the empty beam is included in subtraction of :math:`I_B` :

.. math:: I_s = \frac{1}{z} \big((\frac{I_S-I_{dark}}{T_S}-I_{b}T_S) - (\frac{I_B-I_{dark}}{T_B}-I_{b}T_B)\big)

- The simple case

   If the transmissions are nearly equal as for e.g. protein samples with low concentration (:math:`T_S \approx T_B`)
   we only need to subtract the transmission and dark current corrected buffer measurement from the sample.

   .. math:: I_s = \frac{1}{z} \big((\frac{I_S-I_{dark}}{T_S}) - (\frac{I_B-I_{dark}}{T_B}\big)

- Higher accuracy for large volume fractions

   For larger volume fractions :math:`\Phi` the transmission might be different and we have to take into account that
   only :math:`1-\Phi` of solvent contributes to :math:`I_S`.
   We may incorporate this in the sense of an optical density changing the effective thickness
   :math:`\frac{1}{z_B}\rightarrow\frac{1-\Phi}{z_B}` resulting in different thicknesses :math:`z_S \neq z_B`

.. [1] Improvement of data treatment in small-angle neutron scattering
       Brûlet et al Journal of Applied Crystallography 40, 165-177 (2007)

**Extrapolation and dividing**

We asume that the above correction was correctly applied and we have a transmission corrected
sample and buffer (background) measurement. This is what you typically get from SANS instruments
as e.g KWS1-3 from MLZ Garching or D11-D33 at ILL, Grenoble.

The key part is ``dataff=datas.extrapolate(molarity=0)[0]`` to extrapolate to zero molarity.

.. literalinclude:: ../../examples/example_analyseSASData.py
    :language: python
.. image:: ../../examples/SAS_sf_extraction.png
    :align: center
    :height: 300px
    :alt: SAS_sf_extraction


How to fit SANS data including the resolution for different detector distances
------------------------------------------------------------------------------
First this example shows the influence of smearing, then how to do a fit including
 smearing a la Pedersen in 2 versions.

.. literalinclude:: ../../examples/example_SANSsmearing.py
    :language: python
.. image:: ../../examples/SANSsmearing.jpg
    :align: center
    :height: 300px
    :alt: Picture about SANS smearing

Smearing and desmearing of SAX and SANS data
------------------------------------------------------------
.. literalinclude:: ../../examples/example_SASdesmearing.py
    :language: python
.. image:: ../../examples/SASdesmearing.png
    :align: center
    :height: 300px
    :alt: Picture about smearing/desmearing


A long example for diffusion and how to analyze step by step
------------------------------------------------------------
This is a long example to show possibilities.

A main feature of the fit is that we can change from a constant fit parameters to a parameter
dependent one by simply changing A to [A].


.. literalinclude:: ../../examples/example_fit_diffusion.py
    :language: python

Sedimentation of two particle sizes and resulting scattering: a Simulation
--------------------------------------------------------------------------
.. literalinclude:: ../../examples/example_Sedimentation.py
    :language: python
    :lines: 1-32
.. image:: ../../examples/Sedimentation.jpg
    :align: center
    :height: 300px
    :alt: Picture about diffusion fit

.. literalinclude:: ../../examples/example_Sedimentation.py
    :language: python
    :lines: 33-
.. image:: ../../examples/bimodalScattering.jpg
    :align: center
    :height: 300px

Create a stacked chart of some curves
-------------------------------------
.. literalinclude:: ../../examples/example_grace_stackeddata.py
    :language: python
    :lines: 1-32
.. image:: ../../examples/stackedGaussians.jpeg
    :align: center
    :height: 300px
    :alt: Picture about diffusion fit

A comparison of different dynamic models in frequency domain
------------------------------------------------------------
.. literalinclude:: ../../examples/example_dynamics.py
    :language: python
.. image:: ../../examples/DynamicModels.png
    :align: center
    :height: 300px
    :alt: Picture about diffusion fit

Protein incoherent scattering in frequency domain
------------------------------------------------------------
.. literalinclude:: ../../examples/example_inelasticNeutronScattering.py
    :language: python
.. image:: ../../examples/inelasticNeutronScattering.png
    :align: center
    :height: 300px
    :alt: Picture about diffusion fit
.. image:: ../../examples/Ribonuclease_inelasticNeutronScattering.png
    :align: center
    :height: 300px
    :alt: Picture about diffusion fit

Fitting a multiShellcylinder in various ways
------------------------------------------------------------
.. literalinclude:: ../../examples/example_fit_multicylinder.py
    :language: python
    :lines: 1-73

Hydrodynamic function
------------------------------------------------------------
.. literalinclude:: ../../examples/example_HydrodynamicFunction.py
    :language: python
    :lines: 1-42
.. image:: ../../examples/HydrodynamicFunction.png
    :align: center
    :height: 300px
    :alt: Picture HydrodynamicFunction

Multilamellar Vesicles
----------------------
.. literalinclude:: ../../examples/example_multilamellarVesicle.py
    :language: python
    :lines: 1-180
.. image:: ../../examples/multilamellar1.png
    :align: center
    :height: 300px
    :alt: Picture multilamellar1
.. image:: ../../examples/multilamellar2.png
    :align: center
    :height: 300px
    :alt: Picture multilamellar2
.. image:: ../../examples/multilamellar3.png
    :align: center
    :height: 300px
    :alt: Picture multilamellar3
.. image:: ../../examples/multilamellar5.png
    :align: center
    :height: 300px
    :alt: Picture multilamellar5

2D oriented scattering
-----------------------

**Formfactors of oriented particles or particle complexes**

.. literalinclude:: ../../examples/example_2D_orientedScattering.py
    :language: python
    :lines: 1-109
.. image:: ../../examples/2D_5coreshell.png
    :align: left
    :height: 300px
    :alt: 2D scattering coreshell
.. image:: ../../examples/2D_5spheres.png
    :align: center
    :height: 300px
    :alt: 2D scattering

**Oriented crystal structure factors in 2D**

.. literalinclude:: ../../examples/example_2D_structurefactors.py
    :language: python
    :lines: 5-
.. image:: ../../examples/smallCubeAsymetric.png
    :align: center
    :height: 300px
    :alt: 2D scattering coreshell
.. image:: ../../examples/smallCube10degreeRotation.png
    :align: center
    :height: 300px
    :alt: 2D scattering



A nano cube build of different lattices
---------------------------------------
.. include:: ../../examples/example_comparisonLattices.py
    :start-after: """
    :end-before:  END

.. literalinclude:: ../../examples/example_comparisonLattices.py
    :language: python
    :lines: 23-69
.. image:: ../../examples/LatticeComparison.png
    :align: center
    :height: 300px
    :alt: LatticeComparison

.. include:: ../../examples/example_comparisonLattices.py
    :start-after: #start2
    :end-before:  #end2
.. literalinclude:: ../../examples/example_comparisonLattices.py
    :language: python
    :lines: 83-113
.. image:: ../../examples/LatticeComparison2.png
    :align: center
    :height: 300px
    :alt: LatticeComparison2


.. include:: ../../examples/example_comparisonLattices.py
    :start-after: #start3
    :end-before:  #end3
.. literalinclude:: ../../examples/example_comparisonLattices.py
    :language: python
    :lines: 128-
.. image:: ../../examples/LatticeComparison3.png
    :align: center
    :height: 300px
    :alt: LatticeComparison3

Using cloudscattering as fit model
----------------------------------
At the end a complex shaped object: A cube decorated with spheres of different scattering length.


.. literalinclude:: ../../examples/example_cloudscattering.py
    :lines: 1-
.. image:: ../../examples/cubeWithSpheres.png
    :align: center
    :height: 300px
    :alt: cubeWithSpheres


.. automodule:: jscatter.examples
    :members:
