from setuptools import setup
setup(
    description="More Collections! Some useful data structures for dealing with Data",
    license="MPL 2.0",
    author="Kyle Lahnakoski",
    author_email="kyle@lahnakoski.com",
    long_description_content_type="text/markdown",
    include_package_data=True,
    classifiers=["Development Status :: 4 - Beta","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules","License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"],
    install_requires=["mo-dots>=2.20.18318","mo-future","mo-kwargs>=2.26.18331","mo-logs>=2.26.18331"],
    version="2.26.18331",
    url="https://github.com/klahnakoski/mo-collections",
    packages=["mo_collections"],
    long_description="More Collections\r\n================\r\n\r\nSome useful data structures for collections of data\r\n\r\n\r\n### Class `Index`\r\n\r\nProvide indexing for a list. Inner properties can be used for keys, and keys can be tuples of properties.  \r\n\r\n### Class `UniqueIndex`\r\n\r\nSame as Index, but includes checks and optimization to ensure members' keys are unique.\r\n\r\n### Class `Queue`\r\n\r\nA `Queue` is a list, with `add()` and `pop()`. It ensures members in the queue are not duplicated by not adding the ones already found in the queue.\r\n\r\n### Class `Matrix`\r\n\r\nA multidimensional grid of values that can be used like a `Mapping` from a-tuple-of-coordinates to the value at that coordinate. Plus a few other convenience methods.\r\n\r\nThis is a naive implementation. The hope it is a simple facade to a faster implementation.\r\n\r\n### Class `Relation`\r\n\r\nStore the many-to-many relations between two domains     ",
    name="mo-collections"
)