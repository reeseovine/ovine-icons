#!/usr/bin/env bash

mkdir -p previews/{composites,circular}
for icon in svg/*.svg; do
	icon_name=$(echo $icon | sed -Ee 's/.*\/(.*)\.svg/\1/')

	# Export full PNG
	inkscape \
		--export-width=512 --export-height=512 \
		--export-area-page \
		--export-png="previews/composites/${icon_name}.png" \
		$icon

	# Generate circular icon with drop shadow
	convert "previews/composites/${icon_name}.png" "previews/circular_mask.png" -alpha off -compose copy-opacity -composite png:- | convert - \( +clone -background black -shadow 20x8+0+4 \) +swap -background none -layers merge +repage "previews/circular/${icon_name}.png"
done


# Export the background drawing I made
inkscape \
	--export-width=928 \
	--export-area-page \
	--export-png="previews/background.png" \
	previews/background.svg

# Generate full preview. Does the following steps:
#   1) Take the circular icons and arrange them on an 8-wide grid, each one resized to 128px by
#      128px and with -8px spacing on each side, and give the whole thing a transparent background.
#   2) Add a 16px transparent border around the grid to simulate padding.
#   3) Place this on top of the background image I made and crop it to 928px by 256px.
montage $(find previews/circular/ -name '*.png' | sort) -tile 8x -geometry 128x128-8-8 -background '#00000000' png:- | convert - -bordercolor '#00000000' -border 16x16 png:- | convert previews/background.png - -composite -extent 928x256 preview.png
