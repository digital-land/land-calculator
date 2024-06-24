A demonstration of using planning data to estimate land is potentially suitable for development.

    https://planning.data.gov.uk

# Roadmap

* <s>speed up processing</s>
  - <s>split excludes by LPA</s>
  - <s>combine shapes and have a single intersection</s>
* <s>build data nationally</s>
* <s>style polgons less bold, make more transparent</s>
* update hectares to match filters
* remove lines, slivers and sites < 37m<sup>2</sup>
* include/exclude sites in green-belt option
* sites within green-belt option
* sites within 200m of a built up area
* within 15 minutes from ONS isochrones [map](https://pbarber.github.io/uk-isochrones-map/)
* shard by LPA, not just LAD
* detailed report of size of the areas per-LPA
* popup showing LPA, area, etc for each shape
* a link to the view to https://planning.data.gov.uk/map
* estitimate number of dwellings based on [gentle density](https://www.createstreets.com/why-should-we-build-more-georgian-terraces/)
* use OS Zoomstack built up areas
* exclude OS Zoomstack surface water

# Rebuilding the data

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python [requirements](requirements.txt), [makerules](https://github.com/digital-land/makerules) and other dependencies. Requires Make v4.0 or above.

    $ make makerules
    $ make init
    $ make

# Licence

The software in this project is open source and covered by the [LICENSE](LICENSE) file.

Individual datasets copied into this repository may have specific copyright and licensing, otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
