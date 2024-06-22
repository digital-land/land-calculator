CACHE_DIR=var/cache/
LAD_DIR=var/lad/
REGION_DIR=region/

REGION_DATA=

include makerules.mk

all::	$(REGION_DATA) $(LAD_DATA)

server:
	python3 -m http.server

makerules:	makerules.mk

makerules.mk::  $(CACHE_DIR)organisation.csv bin/makerules.py
	python3 bin/makerules.py > $@

init::
	pip3 install --upgrade -r requirements.txt

clobber::
	rm -rf $(LAD_DIR) $(REGION_DIR)

$(CACHE_DIR)organisation.csv:
	#curl -qfs 'https://files.planning.data.gov.uk/organisation-collection/dataset/organisation.csv' > $@
	# until we've fixed LAD/LPA regions
	curl -qfs 'https://raw.githubusercontent.com/digital-land/organisation-collection/main/data/local-authority.csv' > $@

$(CACHE_DIR)england.geojson:
	@mkdir -p $(CACHE_DIR)
	ln -s data/england.geojson $@

# not on the platform, yet
$(CACHE_DIR)green-space.geojson:
	@mkdir -p $(CACHE_DIR)
	ln -s data/green-space.geojson $@

$(CACHE_DIR)%.geojson:
	@mkdir -p $(CACHE_DIR)
	curl -qfsL 'https://files.planning.data.gov.uk/dataset/$(notdir $@)' -o $@ 


