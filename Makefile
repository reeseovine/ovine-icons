all: clean layers preview

clean:
	rm -rf build

layers:
	bash export_layers.sh

preview:
	bash make_previews.sh
