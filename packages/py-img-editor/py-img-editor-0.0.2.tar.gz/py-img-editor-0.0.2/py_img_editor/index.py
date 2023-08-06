#!/usr/bin/python3
from io import BytesIO
from PIL import Image

import cgi
import os

import cgitb
cgitb.enable()


print("Content-type: text/html\r\n\r\n")
print("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Image Processing</title>
  
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
</head>
<body>""")

print("<h1 class='text-center mt-5 border-bottom border-primary col-md-6 mx-auto'>Image Processing with Pillow</h1>")

form = cgi.FieldStorage()
img = form.getvalue("image")
action = form.getvalue("action")

if not img:
    if os.path.exists('temp.png'):
        img = Image.open('temp.png')
    else:
        img = None
        print("<h3 class='text-danger text-center'>No input file</h3>")
else:
    img = Image.open(BytesIO(img))

if img is not None:
    if action == 'thumbnail':
        img.thumbnail((400, 400))
    elif action == 'rotate':
        img = img.rotate(90)
    elif action == 'crop':
        box = (150, 200, 600, 600)
        img = img.crop(box)
    elif action == 'flip':
        # PIL.Image.FLIP_LEFT_RIGHT,
        # PIL.Image.FLIP_TOP_BOTTOM,
        # PIL.Image.ROTATE_90,
        # PIL.Image.ROTATE_180,
        # PIL.Image.ROTATE_270,
        # PIL.Image.TRANSPOSE.
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif action == 'greyscale':
        img = img.convert('L')
    else:
        pass
    img.save('temp.png')
    print('<br><br><h3 class="text-center"><img src="temp.png" alt="image goes here"></h3>')

    print('<div class="row"><div class="col-md-6 mx-auto"><ul>')
    # The file format of the source file.
    print('<li>Image format:', img.format, "</li>")  # Output: JPEG

    # The pixel format used by the image. Typical values are “1”, “L”, “RGB”, or “CMYK.”
    print("<li>Image mode:", img.mode, "</li>")  # Output: RGB

    # Image size, in pixels. The size is given as a 2-tuple (width, height).
    print("<li>Image size:", img.size, "</li>")  # Output: (1200, 776)

    # Colour palette table, if any.
    print("<li>Image color palette:", img.palette, "</li>")  # Output: None
    print("</ul></div></div>")


"""
transpose() function. It takes one of the following options: PIL.Image.FLIP_LEFT_RIGHT, PIL.Image.FLIP_TOP_BOTTOM, PIL.Image.ROTATE_90, PIL.Image.ROTATE_180, PIL.Image.ROTATE_270 or PIL.Image.TRANSPOSE.

image = Image.open('unsplash_01.jpg')

image_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
image_flip.save('image_flip.jpg')

greyscale_image = image.convert('L')
    """

print("""
<div class="row">
  <div class="col-md-6 mx-auto">
      <form method='post' action='' enctype='multipart/form-data'>
      
        <div class="form-group">
            <label for="image">Upload image file for processing:</label>
            <input type="file" id="image" name="image" class="form-control" value=%s>
        </div>
        
        <button type="submit" class="btn btn-primary mb-2" value="rotate" name="action">Rotate</button>
        <button type="submit" class="btn btn-primary mb-2" value="crop" name="action">Crop</button>
        <button type="submit" class="btn btn-primary mb-2" value="thumbnail" name="action">Thumbnail</button>
        <button type="submit" class="btn btn-primary mb-2" value="flip" name="action">Flip</button>
        <button type="submit" class="btn btn-primary mb-2" value="greyscale" name="action">Greyscale</button>
      </form>
  </div>
</div>""" % 'temp.png')

print("</body></html>")
