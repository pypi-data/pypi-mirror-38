Ancient Lives Toolkit (altk)
=======================

The Ancient Lives Toolkit provides an interface for aggregating crowdsourced labels in euclidean space, e.g. annotations on 2-d images. While the toolkit was designed for Ancient Lives, it can be used to aggregate 2d information more generally.

Updating Documentation
----------------------
.. code-block:: bash

	cd docs

	# .. modify index.rst 

	make html 


Deploying Changes
----------------------
.. code-block:: bash

	python setup.py sdist
	twine upload dist/