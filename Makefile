CACHE_DIR=var/cache/
LAD_DIR=var/lad/
REGION_DIR=region/
OS_ZOOMSTACK_DIR=../../../os-zoomstack-data/data/

include makerules.mk

DATA=$(REGION_DATA)

all::	$(DATA)

server:
	python3 -m http.server

makerules:	makerules.mk

makerules.mk::  $(CACHE_DIR)organisation.csv bin/makerules.py
	python3 bin/makerules.py > $@

init::
	pip3 install --upgrade -r requirements.txt

clobber::
	rm -rf $(LOCAL_DIR) $(REGION_DIR)

$(CACHE_DIR)organisation.csv:
	@mkdir -p $(CACHE_DIR)
	curl -qfs 'https://files.planning.data.gov.uk/organisation-collection/dataset/organisation.csv' > $@

# not on the platform, yet
$(CACHE_DIR)green-space.geojson:
	@mkdir -p $(CACHE_DIR)
	ln -s $(OS_ZOOMSTACK_DIR)/greenspace.geojson $@

# use zoomstack outlines
$(CACHE_DIR)urban-area.geojson:
	@mkdir -p $(CACHE_DIR)
	ln -s $(OS_ZOOMSTACK_DIR)/urban_areas.geojson $@

$(CACHE_DIR)%.geojson:
	@mkdir -p $(CACHE_DIR)
	curl -qfsL 'https://files.planning.data.gov.uk/dataset/$(notdir $@)' -o $@ 

lint::
	black .
	flake8 .
