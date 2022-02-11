#!/usr/bin/env bash

mkdir -p previews/{composites,circular}
for icon in svg/*.svg; do
	icon_name=$(echo $icon | sed -Ee 's/.*\/(.*)\.svg/\1/')

	# Export full PNG
	inkscape \
		--export-width=512 --export-height=512 \
		--export-area-page \
		--export-png="./previews/composites/${icon_name}.png" \
		$icon

	# Generate circular icon with drop shadow
	convert "./previews/composites/${icon_name}.png" circular_mask.png -alpha off -compose copy-opacity -composite png:- | convert - \( +clone -background black -shadow 20x8+0+3 \) +swap -background none -layers merge +repage "./previews/circular/${icon_name}.png"
done
