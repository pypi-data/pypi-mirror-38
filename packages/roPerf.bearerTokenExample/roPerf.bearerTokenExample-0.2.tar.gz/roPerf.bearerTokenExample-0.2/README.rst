=========================
roPerf.bearerTokenExample
=========================

.. contents::
   :depth: 3
..

Bearer Token Example Web Services

Support
=======

| For support, criticism, comments and questions; please contact the
  author/maintainer
| `Mohsen Banan <http://mohsen.1.banan.byname.net>`__ at:
  http://mohsen.1.banan.byname.net/contact

Documentation
=============

Part of ByStar Digital Ecosystem http://www.by-star.net.

This module’s primary documentation is in
http://www.by-star.net/PLPC/180051

Example Usage
=============

::

    from  roPerf import bearerTokenExample

TODO List
=========

-  In documentation, refer to plpc-180056 (mmwsIcm BCP) and plpc-180057
   (Testing Framework)

-  Convert ./bin/roPerf-bearerTokenExample.sh to a python ICM aware of
   pkgBases

-  Get Port number from
   ./roPerf/bearerTokenExample-config/svcInfo/portNu

-  Get ./roPerf/bearerTokenExample-config/pkgInfo/fp/icmsPkgVarBaseDir/
   and build and run in there

-  Reflect the recuirements.txt of generated code in ./setup.py
   dependncies. so that it is not needed.

-  Deal with automation of java swagger code generator – perhaps a dummy
   pkg, ...

-  Understand BCP for flask productization

-  Make this be a starting point for other services

-  Attach the controller to mmwsIcm.bearer token.

-  Create a scenario tester for bearerTokenExample.

-  Test pure out of the box “just runs” experience.
