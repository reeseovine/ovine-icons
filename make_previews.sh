#!/usr/bin/env bash

mkdir -p "build/composites" "build/circular" "build/preview"

# Export each icon as a circular icon made to look like the final one rendered on a device
for icon in svg/*.svg; do
	icon_name=$(echo $icon | sed -Ee 's/.*\/(.*)\.svg/\1/')
	if [ "$icon_name" = "ic_launcher" ]; then continue; fi

	# Export full PNG
	inkscape \
		--export-width=512 --export-height=512 \
		--export-area-page \
		--export-type=png \
		--export-filename="build/composites/${icon_name}.png" \
		$icon

	# Generate circular icon with drop shadow
	convert "build/composites/${icon_name}.png" "extra/circular_mask.png" -alpha off -compose copy-opacity -composite png:- | convert - \( +clone -background black -shadow 20x8+0+4 \) +swap -background none -layers merge +repage "build/circular/${icon_name}.png"
done


# Generate icon grid. This command does the following:
#   1) Take the circular icons and arrange them on an 8-wide grid, each one resized to 128px by
#      128px and with -8px spacing on each side, and make the background transparent.
#   2) Add a 16px transparent border around the grid to simulate padding.
montage $(find "build/circular/" -name '*.png' | sort) -tile 8x -geometry 128x128-8-8 -background '#00000000' png:- | convert - -bordercolor '#00000000' -border 16x16 "build/preview/grid.png"

# Get the size of the grid image
preview_size=$(identify "build/preview/grid.png" | sed -Ee 's/.* PNG ([0-9]+x[0-9]+) .*/\1/')
preview_width=$(echo $preview_size | sed -Ee 's/([0-9]+)x([0-9]+)/\1/')
preview_height=$(echo $preview_size | sed -Ee 's/([0-9]+)x([0-9]+)/\2/')

# To make the background just big enough to fill the grid background, calculate which dimension to scale to.
export_size="--export-width=${preview_width}"
if [ $(($preview_width * 1080 / 1920)) -lt $preview_height ]; then
	export_size="--export-height=${preview_height}"
fi

# Export the background at the right size
inkscape \
	$export_size \
	--export-area-page \
	--export-type=png \
	--export-filename="build/preview/background.png" \
	"extra/background.svg"

# Generate a mask with 32px rounded corners
convert -size $preview_size xc:none -draw "roundrectangle 0,0,${preview_width},${preview_height},32,32" "build/preview/mask.png"

# All together now!
convert -gravity Center "build/preview/background.png" "build/preview/grid.png" -composite -extent $preview_size -matte "build/preview/mask.png" -compose DstIn -composite "extra/preview.png"
