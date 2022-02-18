# pycory.palette

## Planned:

> get( name, screen=None )
Returns palette JSON ({0: COLOR, 1: COLOR ... })

> customs( playdata )
Any palettes returned after setting customs will include custom colours

## To be decided

Colours format,
- rgb tuple
- rgb hex string
- decimal bgr (format used in save file)

(probably rgb tuple)

Possibly something to do with GEO colours?

## Wouldn't work very well

most of these wouldn't work because of screen specific colours (dust and pickle)

> ["name"]

> .name