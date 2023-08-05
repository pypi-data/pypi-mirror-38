.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_parallel_memmap.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_parallel_memmap.py:


===============================
NumPy memmap in joblib.Parallel
===============================

This example illustrates some features enabled by using a memory map
(:class:`numpy.memmap`) within :class:`joblib.Parallel`. First, we show that
dumping a huge data array ahead of passing it to :class:`joblib.Parallel`
speeds up computation. Then, we show the possibility to provide write access to
original data.



Speed up processing of a large data array
#############################################################################

 We create a large data array for which the average is computed for several
 slices.



.. code-block:: python


    import numpy as np

    data = np.random.random((int(1e7),))
    window_size = int(5e5)
    slices = [slice(start, start + window_size)
              for start in range(0, data.size - window_size, int(1e5))]







The ``slow_mean`` function introduces a :func:`time.sleep` call to simulate a
more expensive computation cost for which parallel computing is beneficial.
Parallel may not be beneficial for very fast operation, due to extra overhead
(workers creations, communication, etc.).



.. code-block:: python


    import time


    def slow_mean(data, sl):
        """Simulate a time consuming processing."""
        time.sleep(0.01)
        return data[sl].mean()








First, we will evaluate the sequential computing on our problem.



.. code-block:: python


    tic = time.time()
    results = [slow_mean(data, sl) for sl in slices]
    toc = time.time()
    print('\nElapsed time computing the average of couple of slices {:.2f} s'
          .format(toc - tic))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Elapsed time computing the average of couple of slices 1.08 s


:class:`joblib.Parallel` is used to compute in parallel the average of all
slices using 2 workers.



.. code-block:: python


    from joblib import Parallel, delayed


    tic = time.time()
    results = Parallel(n_jobs=2)(delayed(slow_mean)(data, sl) for sl in slices)
    toc = time.time()
    print('\nElapsed time computing the average of couple of slices {:.2f} s'
          .format(toc - tic))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Elapsed time computing the average of couple of slices 0.82 s


Parallel processing is already faster than the sequential processing. It is
also possible to remove a bit of overhead by dumping the ``data`` array to a
memmap and pass the memmap to :class:`joblib.Parallel`.



.. code-block:: python


    import os
    from joblib import dump, load

    folder = './joblib_memmap'
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    data_filename_memmap = os.path.join(folder, 'data_memmap')
    dump(data, data_filename_memmap)
    data = load(data_filename_memmap, mmap_mode='r')

    tic = time.time()
    results = Parallel(n_jobs=2)(delayed(slow_mean)(data, sl) for sl in slices)
    toc = time.time()
    print('\nElapsed time computing the average of couple of slices {:.2f} s\n'
          .format(toc - tic))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Elapsed time computing the average of couple of slices 0.67 s


Therefore, dumping large ``data`` array ahead of calling
:class:`joblib.Parallel` can speed up the processing by removing some
overhead.


Writable memmap for shared memory :class:`joblib.Parallel`
##############################################################################

 ``slow_mean_write_output`` will compute the mean for some given slices as in
 the previous example. However, the resulting mean will be directly written on
 the output array.



.. code-block:: python



    def slow_mean_write_output(data, sl, output, idx):
        """Simulate a time consuming processing."""
        time.sleep(0.005)
        res_ = data[sl].mean()
        print("[Worker %d] Mean for slice %d is %f" % (os.getpid(), idx, res_))
        output[idx] = res_








Prepare the folder where the memmap will be dumped.



.. code-block:: python


    output_filename_memmap = os.path.join(folder, 'output_memmap')







Pre-allocate a writable shared memory map as a container for the results of
the parallel computation.



.. code-block:: python


    output = np.memmap(output_filename_memmap, dtype=data.dtype,
                       shape=len(slices), mode='w+')







``data`` is replaced by its memory mapped version. Note that the buffer as
already been dumped in the previous section.



.. code-block:: python


    data = load(data_filename_memmap, mmap_mode='r')







Fork the worker processes to perform computation concurrently



.. code-block:: python


    Parallel(n_jobs=2)(delayed(slow_mean_write_output)(data, sl, output, idx)
                       for idx, sl in enumerate(slices))







Compare the results from the output buffer with the expected results



.. code-block:: python


    print("\nExpected means computed in the parent process:\n {}"
          .format(np.array(results)))
    print("\nActual means computed by the worker processes:\n {}"
          .format(output))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Expected means computed in the parent process:
     [0.49944034 0.49911453 0.49917618 0.49957991 0.49981803 0.49984488
     0.4999535  0.49978034 0.4999072  0.49952261 0.49963678 0.49984297
     0.49978946 0.49935283 0.49954907 0.49920566 0.49936897 0.49964281
     0.49998831 0.5000339  0.50027566 0.50030891 0.50036138 0.50024663
     0.50003093 0.49989414 0.49937217 0.49946343 0.49968501 0.49993659
     0.49983988 0.49981781 0.49992288 0.50001719 0.50007076 0.50036733
     0.50049622 0.50040366 0.50033065 0.50014683 0.49955605 0.4998208
     0.49964336 0.49931954 0.49926145 0.49996879 0.50003465 0.50024348
     0.500435   0.50054241 0.50021341 0.50013659 0.49994784 0.49998328
     0.50006715 0.49997976 0.49951897 0.49970846 0.49987933 0.49983926
     0.50002081 0.50021007 0.50011726 0.50007255 0.50005647 0.50030295
     0.50035839 0.50024946 0.49993407 0.49975102 0.49995272 0.49994362
     0.50037876 0.50048861 0.5007831  0.50046208 0.50050807 0.50017532
     0.50034024 0.5004012  0.50042292 0.50029226 0.50058642 0.50055511
     0.50024335 0.50009633 0.50018244 0.499636   0.49994618 0.49980822
     0.49986107 0.49974606 0.49976604 0.49918113 0.49947031]

    Actual means computed by the worker processes:
     [0.49944034 0.49911453 0.49917618 0.49957991 0.49981803 0.49984488
     0.4999535  0.49978034 0.4999072  0.49952261 0.49963678 0.49984297
     0.49978946 0.49935283 0.49954907 0.49920566 0.49936897 0.49964281
     0.49998831 0.5000339  0.50027566 0.50030891 0.50036138 0.50024663
     0.50003093 0.49989414 0.49937217 0.49946343 0.49968501 0.49993659
     0.49983988 0.49981781 0.49992288 0.50001719 0.50007076 0.50036733
     0.50049622 0.50040366 0.50033065 0.50014683 0.49955605 0.4998208
     0.49964336 0.49931954 0.49926145 0.49996879 0.50003465 0.50024348
     0.500435   0.50054241 0.50021341 0.50013659 0.49994784 0.49998328
     0.50006715 0.49997976 0.49951897 0.49970846 0.49987933 0.49983926
     0.50002081 0.50021007 0.50011726 0.50007255 0.50005647 0.50030295
     0.50035839 0.50024946 0.49993407 0.49975102 0.49995272 0.49994362
     0.50037876 0.50048861 0.5007831  0.50046208 0.50050807 0.50017532
     0.50034024 0.5004012  0.50042292 0.50029226 0.50058642 0.50055511
     0.50024335 0.50009633 0.50018244 0.499636   0.49994618 0.49980822
     0.49986107 0.49974606 0.49976604 0.49918113 0.49947031]


Clean-up the memmap
##############################################################################

 Remove the different memmap that we created. It might fail in Windows due
 to file permissions.



.. code-block:: python


    import shutil

    try:
        shutil.rmtree(folder)
    except:  # noqa
        print('Could not clean-up automatically.')






**Total running time of the script:** ( 0 minutes  3.186 seconds)


.. _sphx_glr_download_auto_examples_parallel_memmap.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: parallel_memmap.py <parallel_memmap.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: parallel_memmap.ipynb <parallel_memmap.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
