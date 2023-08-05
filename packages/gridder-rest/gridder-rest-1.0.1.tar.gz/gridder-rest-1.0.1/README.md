# Gridder-REST
A REST-ful API for [Gridder](https://pypi.org/project/gridder/).
Generate grids or tiles over existing images or as stand-alone images.

## Usage
### Server
Set up a server and run `main.py` to be able to receive requests.

Be sure to create a directory named `output` at the same level as the main script.

**NOTE:** Gridder-REST stores the uploaded images and the prepared images before 
sending them back to the user, but no clean up occurs. It is the responsibility 
of the server to clean up the directory of all the png files created by 
Gridder-REST.

### Client
Send a request containing, at a minimum, the `size` parameter, to one of the
available endpoints (see below) depending on the desired shape of the grid.

See below for a list of allowed and required parameters.

## Methods
Requests can be made with two possible methods:

### GET
GET requests create brand-new images. In addition to the `size` parameter,
`width` and `height` parameters are required to determine the size of the output.

### POST
POST requests draw grids over pre-existing images. In addition to the `size`
parameter, the base image to draw on must be provided in the form-data under the
`base` key.

## Endpoints
Requests with the allowed methods and parameters must be sent to one of the
following endpoints.

All endpoints accept GET and POST methods, with the exception of the
`/` index endpoint, which only accepts GET.

### `/`
Provides basic usage instructions.

### `/square`
A square grid. The `size` parameter equals the side of the square.

### `/vline`
A grid of vertical lines. The `size` parameter equals the distance between 
the lines.

### `/hline`
A grid of horizontal lines. The `size` parameter equals the distance between 
the lines.

### `/vhex`
A grid of hexagonal tiles arranged vertically (with top and bottom being flat). 
The `size` parameter equals the height of each hex.

### `/hhex`
A grid of hexagonal tiles arranged horizontally (with left and right being flat). 
The `size` parameter equals the width of each hex.

## Parameters
All parameters are optional except for `size` and, for GET method, 
`width` and `height`.

Where applicable, measures can be entered in centimetres, millimetres or inches by
appending `cm`, `mm` or `in` to the amount.

#### `size`
Determines the size of the grid. For details, refer to specific endpoints.

#### `height`, `width`
Height and width of the output image. Only allowed with GET method.

#### `bgcol`
Colour of the background of the image. Can be a colour name or hexadecimal colour
value like `#000000`. Only allowed with GET method.

#### `gridcol`
Colour of the line used to draw the grid.

#### `padding`, `pt`, `pr`, `pb`, `pl`
Padding around the grid, before the image bounds.

Options for specific padding on the top `pt`, right `pr`, bottom `pb` and left `pl`
margins are available and, if present, have priority over the generic `padding`
option.

#### `line`
Line width of the lines used to draw the grid.

#### `name`
Name of the output file. If an extension other than png is entered, it is used as
part of the file name: the output will always be in png format.

## Response codes
#### 200 OK
Everything went as expected and appropriate output was produced.

#### 400 Bad Request
A POST request was made without correctly including the base file.

#### 415 Unsupported Media Type
A POST request was made using a base file in a format unreadable by the backend.
Convert the file to a more common format and retry.

#### 422 Unprocessable Entity
One or more required parameter are missing or were provided in unreadable form.

#### 500 Server Error
Something went wrong with the backend. Please contact the author providing details
on what you tried so the problem may be fixed, if it's due to a bug.
