CACHE_DIR=var/cache/

DATASETS=\
    $(CACHE_DIR)england.geojson\
    $(CACHE_DIR)ancient-woodland.geojson\
    $(CACHE_DIR)area-of-outstanding-natural-beauty.geojson\
    $(CACHE_DIR)heritage-coast.geojson\
    $(CACHE_DIR)park-and-garden.geojson\
    $(CACHE_DIR)local-nature-reserve.geojson\
    $(CACHE_DIR)national-nature-reserve.geojson\
    $(CACHE_DIR)national-park.geojson\
    $(CACHE_DIR)ramsar.geojson\
    $(CACHE_DIR)site-of-special-scientific-interest.geojson\
    $(CACHE_DIR)special-area-of-conservation.geojson\
    $(CACHE_DIR)special-protection-area.geojson\
    $(CACHE_DIR)flood-risk-zone.geojson\
    $(CACHE_DIR)battlefield.geojson\
    $(CACHE_DIR)conservation-area.geojson\
    $(CACHE_DIR)scheduled-monument.geojson\
    $(CACHE_DIR)world-heritage-site.geojson\
    $(CACHE_DIR)world-heritage-site-buffer-zone.geojson\
    $(CACHE_DIR)built-up-area.geojson\
    $(CACHE_DIR)region.geojson\
    $(CACHE_DIR)green-space.geojson\
    $(CACHE_DIR)green-belt.geojson

all:	$(DATASETS) #docs/index.html

$(CACHE_DIR)england.geojson:
	@mkdir -p $(CACHE_DIR)
	cp data/england.geojson $@

$(CACHE_DIR)green-space.geojson:
	@mkdir -p $(CACHE_DIR)
	cp data/green-space.geojson $@

$(CACHE_DIR)%.geojson:
	@mkdir -p $(CACHE_DIR)
	curl -qfsL 'https://files.planning.data.gov.uk/dataset/$(notdir $@)' -o $@ 

server:
	python3 -m http.server

init::
	pip3 install --upgrade -r requirements.txt
