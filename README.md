# ovine icons 🐏

Hand-made adaptive icons for a small selection of Android apps.

![icon preview image](extra/preview.png)

## why?

I like my app icons to all be circular in the app drawer. Sometimes they don't have circular/adaptive icons or sometimes it just looks ugly or not positioned/scaled right to me. These icons are mostly meant to supplement apps that don't already have adaptive icons; not every app needs a new icon.

## notes

This is now an installable icon pack! Though I'm not an Android developer and I have no idea what I'm doing, so if you spot any issues I may need some help!

Feel free to open an issue if you want me to make an icon and I may or may not decide to.

## contributing

Feel free to submit an icon through a pull request if you'd like! I don't stick to any specific design language but I try to follow these personal rules to keep them feeling cohesive:
- SVG format vector drawing.
- Follow <a href="https://github.com/jahirfiquitiva/Blueprint/wiki/Setting-up-icon-pack-(Part-2}#naming-icons">these naming conventions</a> for the file name.
- Follow [Google's adaptive icon guidelines](https://developer.android.com/google-play/resources/icon-design-specifications) and use the file `extra/adaptive_template.svg` for scale and position. Use two layers: one with an ID of `background` and one with `foreground`.
- Use vector logo or redraw it as a vector. (NO EMBEDDED RASTER IMAGES PLS)
- If the source logo or icon looks too "busy", simplify it by reducing it to the essentials.
- No letters or text unless it's part of the logo (NOT the wordmark). (e.g. Facebook's 'f')
- No shadows.
- Gradients can be used but they should be tasteful and not too flashy.
- All colors should be sourced from the original icon, but exceptions can be made.

If an app's current icon doesn't follow these then it's probably a good candidate for this icon pack.

## to do

- [ ] Package it into an APK that you can install on your phone
- [x] Finish SVG->drawable converter
- [x] Debug gradients
- [x] Rename SVGs to drawable names
- [x] Resize all SVGs to 108x108
- [x] ~~Either~~ get rid of Xfinity Home ~~or make a whole set for all their apps~~

## license

- The icons themselves are [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- [Blueprint by jahirfiquitiva](https://github.com/jahirfiquitiva/Blueprint) is also [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- [Svg2VectorAndroid by ravibhojwani86](https://github.com/ravibhojwani86/Svg2VectorAndroid) has no license, so all rights reserved.
