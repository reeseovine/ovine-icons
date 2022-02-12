#!/usr/bin/env bash

for icon in svg/*.svg; do
	icon_name=$(echo $icon | sed -Ee 's/.*\/(.*)\.svg/\1/')
	layers=($(inkscape --query-all $icon | grep layer | awk -F, '{print $1}'))

	mkdir -p "png/${icon_name}"

	for layer in "${layers[@]}"; do
		inkscape \
			--export-width=512 --export-height=512 \
			--export-area-page \
			--export-id-only \
			--export-id=$layer \
			--export-png="png/${icon_name}/${layer}.png" \
			$icon
	done
done
