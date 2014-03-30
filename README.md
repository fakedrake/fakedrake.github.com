# DrNinjaBatman's (aka FakeDrake's) pelican blog

To setup this blog just

	git clone git@github.com:fakedrake/fakedrake.github.com
	git checkout sources
	virtualenv --no-site-packages .
	. bin/activate
	pip install -r requirements.txt

Then just throw markdown (or rst, I prefer markdown) documents in the
`content/` directory and run

	make html serve

This will run serve and you can check what your article looks like in
your browser. To actually publish an article:

	make github
