all: clean xml preview

clean:
	rm -rf build

layers:
	bash export_layers.sh

xml: layers
	python3 generate_icon_pack.py

preview:
	bash make_previews.sh
