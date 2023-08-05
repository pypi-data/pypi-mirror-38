# Python Linked Data API (pyLDAPI)
A very small module to add Linked Data API functionality to a Python Flask installation

[![PyPI version](https://badge.fury.io/py/pyldapi.svg)](https://badge.fury.io/py/pyldapi)

## How to use
This module contains only a small Python module which is indented to be added (imported) into a [Python Flask](http://flask.pocoo.org/) installation in order to add a series of extra functions to endpoints to the ones defined by you as a Flask user (URL routes).

An API using this module will get:

* an *alternates view* for each *Register* and *Object* that the API delivers
    - if the API declares the appropriate *model view* s for each item
* a *Register of Registers*
    - a start-up function that auto-generated a Register of Registers is run when the API is launched
* a basic, over-writeable, template for Registers' HTML & RDF


## Definitions
* **alternates view**: the *model view* that lists all other views. This API uses the definition of *alternates view* presented at <https://promsns.org/def/alt>
* **Linked Data principles**: principles of making things available over the Internet in both human and machine readable forms. codified by the World Wide Web Consortium. See <https://www.w3.org/standards/semanticweb/data>
* *model view*: a set of properties of a Linked Data object codified according to a standard or profile of a standard
* **Object**: any individual thing delivered according to *Linked Data principles*
* **Register**: a simple listing of URIs of objects, delivered according to *Linked Data principles*
* **Register of Registers**: a a *register* that lists all other *registers* that an API provides


## Further Documentation
Detailed documenatation is the subject of current work (September, 2018) so please revisit this location for it soon! Also, see the implementaitons below. The first is a small project.


## Implementations
* Register of Media Types
    * <https://w3id.org/mediatype/>
* Linked Data version of the Geocoded National Address File
    * <http://linked.data.gov.au/dataset/gnaf>


## License
This repository is licensed under GNU General Public License (GPL) v3.0. See the [LICENSE deed](LICENSE) in this repository for details.


## Contacts
Lead:  
**Nicholas Car**  
*Senior Experimental Scientist*  
CSIRO Land & Water  
<nicholas.car@csiro.au>  
<http://orcid.org/0000-0002-8742-7730>  

Senior Developer:  
**Ashley Sommer**  
*Informatics Software Engineer*  
<ashley.sommer@csiro.au>  
