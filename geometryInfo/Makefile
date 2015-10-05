PLUGINNAME = geometryInfo
PY_FILES = geometryInfo.py __init__.py
EXTRAS = icon.png metadata.txt
RESOURCE_FILES = resources.py

default: compile

compile: $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc4 -o $@ $<

deploy: compile
	mkdir -p $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp -vf $(RESOURCE_FILES) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)

clean:
	rm $(RESOURCE_FILES)
