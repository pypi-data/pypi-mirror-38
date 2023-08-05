.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_parallel_random_state.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_parallel_random_state.py:


===================================
Random state within joblib.Parallel
===================================

Randomness is affected by parallel execution differently by the different
backends.

In particular, when using multiple processes, the random sequence can be
the same in all processes. This example illustrates the problem and shows
how to work around it.



.. code-block:: python


    import numpy as np
    from joblib import Parallel, delayed


    # The followings are hacks to allow sphinx-gallery to run the example.
    import os
    import sys
    sys.path.insert(0, os.getcwd())
    main_dir = os.path.basename(sys.modules['__main__'].__file__)
    IS_RUN_WITH_SPHINX_GALLERY = main_dir != os.getcwd()








A utility function for the example



.. code-block:: python

    def print_vector(vector, backend):
        """Helper function to print the generated vector with a given backend."""
        print('\nThe different generated vectors using the {} backend are:\n {}'
              .format(backend, np.array(vector)))








Sequential behavior
##############################################################################

 ``stochastic_function`` will generate five random integers. When
 calling the function several times, we are expecting to obtain
 different vectors. For instance, we will call the function five times
 in a sequential manner, we can check that the generated vectors are all
 different.



.. code-block:: python



    def stochastic_function(max_value):
        """Randomly generate integer up to a maximum value."""
        return np.random.randint(max_value, size=5)


    n_vectors = 5
    random_vector = [stochastic_function(10) for _ in range(n_vectors)]
    print('\nThe different generated vectors in a sequential manner are:\n {}'
          .format(np.array(random_vector)))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    The different generated vectors in a sequential manner are:
     [[7 5 2 3 2]
     [8 5 1 7 3]
     [7 1 5 8 4]
     [6 3 9 5 0]
     [0 2 4 9 8]]


Parallel behavior
##############################################################################

 Joblib provides three different backend: loky (default), threading, and
 multiprocessing.



.. code-block:: python


    backend = 'loky'
    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function)(10) for _ in range(n_vectors))
    print_vector(random_vector, backend)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    The different generated vectors using the loky backend are:
     [[6 1 9 2 3]
     [7 8 5 3 8]
     [9 7 8 3 0]
     [7 4 9 0 2]
     [3 1 7 8 5]]



.. code-block:: python


    backend = 'threading'
    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function)(10) for _ in range(n_vectors))
    print_vector(random_vector, backend)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    The different generated vectors using the threading backend are:
     [[8 4 9 1 6]
     [4 7 9 2 8]
     [7 1 1 3 4]
     [0 3 3 2 1]
     [5 7 6 3 9]]


Loky and the threading backends behave exactly as in the sequential case and
do not require more care. However, this is not the case regarding the
multiprocessing backend.



.. code-block:: python


    if IS_RUN_WITH_SPHINX_GALLERY:
        # When this example is run with sphinx gallery, it breaks the pickling
        # capacity for multiprocessing backend so we have to modify the way we
        # define our functions. This has nothing to do with the example.
        from utils import stochastic_function

    backend = 'multiprocessing'
    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function)(10) for _ in range(n_vectors))
    print_vector(random_vector, backend)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    The different generated vectors using the multiprocessing backend are:
     [[7 9 5 5 9]
     [7 9 5 5 9]
     [8 2 3 9 5]
     [8 2 3 9 5]
     [2 9 6 4 6]]


Some of the generated vectors are exactly the same, which can be a
problem for the application.

Technically, the reason is that all forked Python processes share the
same exact random seed. As a results, we obtain twice the same randomly
generated vectors because we are using ``n_jobs=2``. A solution is to
set the random state within the function which is passed to
:class:`joblib.Parallel`.



.. code-block:: python



    def stochastic_function_seeded(max_value, random_state):
        rng = np.random.RandomState(random_state)
        return rng.randint(max_value, size=5)


    if IS_RUN_WITH_SPHINX_GALLERY:
        # When this example is run with sphinx gallery, it breaks the pickling
        # capacity for multiprocessing backend so we have to modify the way we
        # define our functions. This has nothing to do with the example.
        from utils import stochastic_function_seeded  # noqa: F811








``stochastic_function_seeded`` accepts as argument a random seed. We can
reset this seed by passing ``None`` at every function call. In this case, we
see that the generated vectors are all different.



.. code-block:: python


    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function_seeded)(10, None) for _ in range(n_vectors))
    print_vector(random_vector, backend)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    The different generated vectors using the multiprocessing backend are:
     [[1 5 0 2 1]
     [0 0 3 4 6]
     [5 0 9 4 6]
     [2 6 7 1 7]
     [7 6 4 6 6]]


Fixing the random state to obtain deterministic results
##############################################################################

 The pattern of ``stochastic_function_seeded`` has another advantage: it
 allows to control the random_state by passing a known seed. So for instance,
 we can replicate the same generation of vectors by passing a fixed state as
 follows.



.. code-block:: python


    random_state = np.random.randint(np.iinfo(np.int32).max, size=n_vectors)

    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function_seeded)(10, rng) for rng in random_state)
    print_vector(random_vector, backend)

    random_vector = Parallel(n_jobs=2, backend=backend)(delayed(
        stochastic_function_seeded)(10, rng) for rng in random_state)
    print_vector(random_vector, backend)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    The different generated vectors using the multiprocessing backend are:
     [[6 6 3 4 0]
     [2 3 8 6 5]
     [5 1 9 4 4]
     [3 6 4 8 7]
     [7 3 4 8 3]]

    The different generated vectors using the multiprocessing backend are:
     [[6 6 3 4 0]
     [2 3 8 6 5]
     [5 1 9 4 4]
     [3 6 4 8 7]
     [7 3 4 8 3]]


**Total running time of the script:** ( 0 minutes  0.923 seconds)


.. _sphx_glr_download_auto_examples_parallel_random_state.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: parallel_random_state.py <parallel_random_state.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: parallel_random_state.ipynb <parallel_random_state.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
