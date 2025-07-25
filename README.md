A demonstration of using planning data to estimate land is unconstrained and potentially suitable for development.

[https://planning.data.gov.uk](https://planning.data.gov.uk)

# Roadmap

* <s>speed up processing</s>
  - <s>split excludes by LPA</s>
  - <s>combine shapes and have a single intersection</s>
* <s>build data nationally</s>
* <s>style polgons less bold, make more transparent</s>
* <s>update hectares to match filters</s>
* <s>estitimate number of dwellings based on [gentle density](https://www.createstreets.com/why-should-we-build-more-georgian-terraces/)</s>
* <s>exclude [NSIP](https://www.planning.data.gov.uk/dataset/infrastructure-project)</s>
* remove lines, slivers and other artifacts
  - <s>remove sites < 37m<sup>2</sup> in size</s>
  - remove shapes with a low [thinness ratio](https://math.stackexchange.com/questions/1336265/explanation-of-the-thinness-ratio-formula)
  - <s>remove Line, LineStrings and simplify GeometryCollections</s>
* <s>include/exclude sites in green-belt option</s>
* <s>sites within green-belt option</s>
* move from large GeoJSON files to <a href="https://martinfleischmann.net/how-to-create-a-vector-based-web-map-hosted-on-github/">vector tiles</a>
* sites within 200m of a built up area
* split golf course from green-space
* within 15 minutes from ONS isochrones [map](https://pbarber.github.io/uk-isochrones-map/)
* within 800m of a main-line railway station
* shard by LPA, not just LAD (National parks span regions)
* detailed report of size of the areas per-LPA
* popup showing LPA, area, etc for each shape
* update URL for current options
* a link to the current view to https://planning.data.gov.uk/map
* use OS Zoomstack rather than ONS built up areas
* exclude OS Zoomstack surface water
* exclude OS Zoomstack foreshore
* exclude OS Zoomstack railways (buffered)
* exclude OS Zoomstack rivers (buffered)
* exclude OS Zoomstack schools (sites of type "Education")
* exclude OS Zoomstack hospitals and clinics (sites of type "Medical Care")
* exclude agricultural land with a high [ALC grade](https://www.gov.uk/government/publications/agricultural-land-assess-proposals-for-development/guide-to-assessing-development-proposals-on-agricultural-land)
* stacked bar chart of land use in selected areas
* [Indicies of Multiple Deprevation](https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019) Barriers to Housing and Services Domain (2019) (statistical cut-off)

<a href="https://www.flickr.com/photos/psd/53780793882/in/dateposted-ff/" title="Estimating land availability"><img src="https://live.staticflickr.com/65535/53780793882_5ac8d56fa2_c.jpg" width="400" alt="Estimating land availability"/></a>

# Grid approach

The approach of subtracting geometries take time to process and creates issues with invalid polygons. Processing the country as a matrix of 1 hectare grids could avoid geometry issues, speed up processing, reduce the size of the data, and simplify how the browser shows switching options.

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
