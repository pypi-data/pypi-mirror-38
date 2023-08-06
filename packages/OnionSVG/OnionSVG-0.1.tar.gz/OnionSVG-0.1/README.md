# OnionSVG
Peel your SVG files with Python.

### Dependencies:
* `lxml` for reading SVG files
* `cairosvg` to render SVG. On Windows, `cairo` has to be installed manually:
an easy way to do this is to just use the appropriate `cairo.dll` provided by
[preshing/cairo-windows](https://github.com/preshing/cairo-windows/releases).