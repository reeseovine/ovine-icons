#!/usr/bin/env bash

for icon in svg/*.svg; do
	icon_name=$(echo $icon | sed -Ee 's/.*\/(.*)\.svg/\1/')
	mkdir -p "build/layers/${icon_name}"

	layers=(foreground background)
	for layer in "${layers[@]}"; do
		inkscape \
			--export-width=108 --export-height=108 \
			--export-area-page \
			--export-id-only \
			--export-id="$layer" \
			--export-plain-svg="build/layers/${icon_name}/${layer}.svg" \
			"$icon"
	done
done
