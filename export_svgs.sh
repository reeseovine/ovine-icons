#!/usr/bin/env bash

generate_sizes(){
	icon_name=$(echo $1 | sed -Ee 's/.*\/(.*)\.svg/\1/')
	inkscape \
		--export-type=png \
		--export-filename="./png/${icon_name}.png" \
		--export-area-page \
		--export-width=1024 --export-height=1024 \
		$1
}
export -f generate_sizes

find ./svg/ -name \*.svg -exec bash -c 'generate_sizes "$0"' {} \;
