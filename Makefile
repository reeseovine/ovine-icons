all: clean layers preview

clean:
	rm -rf png/ previews/circular previews/composites previews/background.png

layers:
	bash export_layers.sh

preview:
	bash make_previews.sh
