# pycory.decode

## Planned:

>> geo( data )

Data can be base64 encoded string OR list
Returns geo class of the data

>> paint( data, palette=None )

Data can be base64 encoded string OR list
Returns paint class of the data
If palette is specified, Paint.to_palette is run with it

>> Geo( list )

[x, y] returns a list of the two values for that position

>> Paint( list )

[x, y] returns the value (1 - 15) or colour.

> to_palette( palette )

goes through paint data and sets colour

> from_palette( palette )

does to_palette but the other way around

> current - int

uses consts decode.PALETTE decode.COLOUR
whether its paletted or colours

>> Both Paint & Geo

> for loop?

either do what enumerate is planned to do OR just go through each of the value left to right top to bottom

> .enumerate()

function to loop through with the x, y and value position (left to right top to bottom), e.g:

```py
for x, y, value in paint.enumerate:
```

> encode( )

returns encoded version of paint/geo

## To be decided:

Geo palette?