"""Gridder-REST is a REST-ful interface for Gridder.
    Copyright (C) 2018  Federico Salerno <itashadd+gridder[at]gmail.com>


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>
"""
import os

from flask import Flask, send_file, make_response, request
from flask_restful import Api, Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from PIL import Image
from gridder import SUPPORTED_SHAPES
from gridder import Converter
from gridder import Drawer


# Settings and utilities

app = Flask(__name__)
api = Api(app)

output_dir = "output/"
os.makedirs(output_dir, exist_ok=True)


def build_draw_kwargs(kwargs: dict, base_image: Image.Image, sizes: tuple=None) -> dict:
    """Build the arguments dictionary necessary for drawing a grid."""
    draw_kwargs = {**kwargs, "base": base_image}

    if sizes:
        draw_kwargs.update({"im_width": sizes[0], "im_height": sizes[1]})

    return draw_kwargs


def make_output_response(draw_kwargs: dict) -> str:
    """Save the image, make the response and return it."""
    output_name = draw_kwargs["name"] if draw_kwargs["name"].endswith(".png") else draw_kwargs["name"] + ".png"
    output_path = os.path.join(output_dir, output_name)

    draw_kwargs["base"].save(output_path)

    response = make_response(send_file(output_path, as_attachment=True))

    return response


def get_response(shape_name: str, kwargs: dict):
    """Make and return a typical GET response for a request of a certain grid shape."""
    if not kwargs["bgcol"] or kwargs["bgcol"] == "transparent":
        bg_colour = (0, 0, 0, 0)
    else:
        bg_colour = kwargs["bgcol"]

    # Make base image
    base = Image.new("RGBA",
                     tuple(Converter.to_px(size) for size in (kwargs["im_width"], kwargs["im_height"])),
                     bg_colour)

    draw_kwargs = build_draw_kwargs(kwargs, base)

    Drawer.draw(shape_name, **draw_kwargs)

    return make_output_response(draw_kwargs)


def post_response(shape_name: str, kwargs: dict):
    """Make and return a typical POST response for a request of a certain grid shape."""
    if not request.files:
        return "Base file is required for POST method.", 400

    try:
        base = Image.open(request.files["base"])
    except IOError:
        return "Base file unreadable.", 415

    draw_kwargs = build_draw_kwargs(kwargs, base, base.size)

    Drawer.draw(shape_name, **draw_kwargs)

    return make_output_response(draw_kwargs)


# Requests


# noinspection PyUnresolvedReferences
# All fields are Str to allow for unit parsing via gridder's Converter.
base_args = {
    "size": fields.Str(required=True, attribute="grid_size"),
    "padding": fields.Str(required=False, missing="0"),
    "pt": fields.Str(required=False, missing=None, attribute="padding_top"),
    "pr": fields.Str(required=False, missing=None, attribute="padding_right"),
    "pb": fields.Str(required=False, missing=None, attribute="padding_bot"),
    "pl": fields.Str(required=False, missing=None, attribute="padding_left"),
    "line": fields.Str(required=False, missing="1", attribute="line_width"),
    "gridcol": fields.Str(required=False, missing="black", attribute="grid_colour"),
    "name": fields.Str(required=False, missing="grid.png"),
}

# noinspection PyUnresolvedReferences
no_file_args = {
    **base_args,
    "width": fields.Str(required=True, attribute="im_width"),
    "height": fields.Str(required=True, attribute="im_height"),
    "bgcol": fields.Str(required=False, missing="transparent"),
}


class Index(Resource):
    def get(self):
        shapes_endpoints = "".join(f" - /{shape_name}<br />" for shape_name in SUPPORTED_SHAPES)
        basic_instructions = "Choose an endpoint depending on the desired shape:<br />" \
                             "{shapes_endpoints}" \
                             "<br />" \
                             "Allowed methods:<br />" \
                             "GET: returns a new image with a grid.<br />" \
                             " - Required parameters: `width`, `height`, `size`<br />" \
                             "POST: returns the provided image with a superimposed grid.<br />" \
                             " - Required parameter: `size`<br />" \
                             " - Also required: form-data parameter: `base` containing the base image.<br />" \
                             "<br />" \
                             "Response body will contain a `grid.png` image with the output."\
            .format(shapes_endpoints=shapes_endpoints)
        output = make_response(basic_instructions, 200)
        output.headers["Content-Type"] = "text/html"
        return output


api.add_resource(Index, "/")


# Make and register a class for each supported shape.
for shape in SUPPORTED_SHAPES:
    # Make a method for each accepted HTTP verb. Only the name of the shape varies.
    @use_kwargs(no_file_args)
    def get(self, **kwargs):
        return get_response(self.__class__.__name__, kwargs)

    @use_kwargs(base_args)
    def post(self, **kwargs):
        return post_response(self.__class__.__name__, kwargs)

    grid_class = type(shape, (Resource,), {
        # Make a method for each allowed HTTP verb, with the appropriate decorator.
        "get": get,
        "post": post,
    })

    # Register each class.
    api.add_resource(grid_class, f"/{shape}")


if __name__ == "__main__":
    app.run(debug=True)
