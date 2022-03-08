#!/usr/bin/env python3

import csv
from typing import NamedTuple
from pathlib import Path
from subprocess import run
from os import listdir


#########
# Setup #
#########

app_path = Path("./app/src/main")

class Icon(NamedTuple):
	drawable: str
	package: str
	activity: str

	def __repr__(self) -> str:
		return "│ {0:30} │ {1:50} │ {2:70} │".format(self.drawable, self.package, self.activity)

class IconList:
	def __init__(self, icons=[]):
		self.icons = icons

	def __repr__(self) -> str:
		top     = '╭─'+('─'*30)+'─┬─'+('─'*50)+'─┬─'+('─'*70)+'─╮'
		header  = '│ {0:30} │ {1:50} │ {2:70} │'.format('Drawable', 'Package ID', 'Activity ID')
		divider = '├─'+('─'*30)+'─┼─'+('─'*50)+'─┼─'+('─'*70)+'─┤'
		bottom  = '╰─'+('─'*30)+'─┴─'+('─'*50)+'─┴─'+('─'*70)+'─╯'
		return "\n".join([top, header, divider, *[str(row) for row in self.icons], bottom])

	def query(self, column: str, value: str):
		results = []
		for row in self.icons:
			if getattr(row, column) == value:
				results.append(row)
		return IconList(results)

	def get_unique_entries(self, column: str) -> list:
		names = []
		for row in self.icons:
			if getattr(row, column) not in names:
				names.append(getattr(row, column))
		return names

def get_drawable_names() -> list:
	return filter(lambda name: name != "ic_launcher", listdir('build/layers'))



#################
# File handling #
#################

# Open `icon_data.tsv` and turn it into a usable format
def get_from_tsv_file():
	icons = []
	with open('icon_data.tsv') as icon_data:
		r = csv.reader(icon_data, delimiter="\t")
		for (drawable, package, activity) in r:
			icons.append(Icon(drawable, package, activity))
	return IconList(icons)
	# return IconList(map(Icon._make, csv.reader(open('icon_data.tsv', 'rb'), delimiter="\t")))

def write_file(filename: str, data: str) -> None:
	with open(filename, 'w') as f:
		f.write(data)
		print(f'Successfully wrote {filename}')



##################
# XML generators #
##################

# Generate appfilter.xml
def xmlgen_appfilter(icons: IconList) -> None:
	xml = '<?xml version="1.0" encoding="UTF-8"?>\n<resources>\n'
	for row in icons.icons:
		xml += f'\t<item component="ComponentInfo{{{row.package}/{row.activity}}}" drawable="{row.drawable}" />\n'
	xml += '</resources>\n'
	write_file(app_path / 'assets' / 'appfilter.xml', xml)
	write_file(app_path / 'res' / 'xml' / 'appfilter.xml', xml)

# Generate appmap.xml
def xmlgen_appmap(icons: IconList) -> None:
	xml = '<?xml version="1.0" encoding="UTF-8"?>\n<appmap>\n'
	for row in icons.icons:
		xml += f'\t<item class="{row.package}/{row.activity}" name="{row.drawable}" />\n'
	xml += '</appmap>\n'
	write_file(app_path / 'res' / 'xml' / 'appmap.xml', xml)

# Generate drawable.xml
def xmlgen_drawable(icons: IconList) -> None:
	xml = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n\t<version>1</version>\n\t<category title="All" />\n'
	for name in get_drawable_names():
		xml += f'\t<item drawable="{name}" />\n'
	xml += '</resources>\n'
	write_file(app_path / 'assets' / 'drawable.xml', xml)

# Generate icon_pack.xml
def xmlgen_iconpack(icons: IconList) -> None:
	xml = '<?xml version="1.0" encoding="utf-8"?><!--suppress CheckTagEmptyBody -->\n<resources xmlns:tools="http://schemas.android.com/tools" tools:ignore="ExtraTranslation">\n\t<!-- Make sure to put at least 8 icons -->\n\t<string-array name="icons_preview">\n'
	for name in get_drawable_names():
		xml += f'\t\t<item>{name}</item>\n'
	xml += '\t</string-array>\n\n\t<!-- These sections below are for your "Previews" section -->\n\t<!-- Make sure the filters names are the same as the other arrays -->\n\t<string-array name="icon_filters">\n\t\t<item>all</item>\n\t</string-array>\n\n\t<string-array name="all">\n'
	for name in get_drawable_names():
		xml += f'\t\t<item>{name}</item>\n'
	xml += '\t</string-array>\n</resources>\n'
	write_file(app_path / 'res' / 'values' / 'icon_pack.xml', xml)

# Generate drawable/*_[background,foreground].xml
def xmlgen_drawable_layers(icons: IconList) -> None:
	run(['java', '-jar', 'Svg2VectorAndroid-1.0.1.jar', 'build/layers/'])
	run(['rm', '-r', 'build/vectordrawables'])
	run(['mv', 'build/layers/ProcessedSVG', 'build/vectordrawables'])
	for name in get_drawable_names():
		for layer in ['background', 'foreground']:
			with open(Path(__file__).parent / 'build' / 'vectordrawables' / name / f'{layer}_svg.xml') as f:
				write_file(app_path / 'res' / 'drawable' / f'{name}_{layer}.xml', f.read())

# Generate drawable-anydpi-v26/*.xml
def xmlgen_drawable_combined(icons: IconList) -> None:
	for name in get_drawable_names():
		xml = '<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
		xml += f'\t<background android:drawable="@drawable/{name}_background" />\n'
		xml += f'\t<foreground android:drawable="@drawable/{name}_foreground" />\n'
		xml += '</adaptive-icon>\n'
		write_file(app_path / 'res' / 'drawable-anydpi-v26' / f'{name}.xml', xml)



########
# Main #
########

def main():
	icons = get_from_tsv_file()
	xmlgen_appfilter(icons)
	xmlgen_appmap(icons)
	xmlgen_drawable(icons)
	xmlgen_iconpack(icons)
	xmlgen_drawable_layers(icons)
	xmlgen_drawable_combined(icons)
	print('All done!')

if __name__ == '__main__':
	main()
