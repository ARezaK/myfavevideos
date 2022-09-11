# -*- coding: utf-8 -*-
#!/bin/python

import os
import random
from flask import Flask, Response, request, abort, render_template_string, send_from_directory
from PIL import Image
from io import StringIO

app = Flask(__name__)

dir_path = os.path.dirname(os.path.abspath(__file__))
print(dir_path)

file_format = 'jpeg'

WIDTH = 400
HEIGHT = 200

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<title></title>
<meta charset="utf-8" />
<style>
body {
margin: 0;
background-color: #333;
}
.image {
display: inline-block;
margin: 3em 14px;
background-color: #444;
box-shadow: 0 0 10px rgba(0,0,0,0.3);
}
img {
display: block;
}

.video {
  background-image: url('https://img.youtube.com/vi/nZcejtAwxz4/maxresdefault.jpg');
  height: 500px;
  width: 600px;
  margin-bottom: 50px;
}

/* Hide Play button + controls on iOS */
video::-webkit-media-controls {
    display:none !important;
}
</style>

</head>
<body>

{% for video in videos %}
<video width="420" height="500" controls loop preload="metadata">
  <source src="{{video.src}}#t=0.1" type="video/mp4">
</video>
    <a href="delete/{{video.src}}">delete</a>
{% endfor %}

{% for image in images %}
    <a class="image" href="{{ image.src }}" >
        <img src="{{ image.src }}" />
        {{image.src}}
    </a>
     <a href="delete/{{image.src}}">delete</a>
{% endfor %}

<script>
var figure = $(".video").hover( hoverVideo, hideVideo );

function hoverVideo(e) {  
    $('video', this).get(0).play(); 
}

function hideVideo(e) {
    $('video', this).get(0).pause(); 
}
</script>

</body>
'''


@app.route('/<path:filename>')
def image(filename):
    # print(filename)
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = StringIO()
        im.save(io, format='gif')
        return Response(io.getvalue(), mimetype='image/gif')

    except IOError:
        print("IOError: %s" % filename)
        abort(404)

    return send_from_directory('.', filename)


@app.route('/')
def index():
    videos = []
    images = []
    for root, dirs, files in os.walk('.'):
        f_ = [os.path.join(root,name) for name in files]
        random.shuffle(f_)
        for filename in f_:
            # load the images
            if filename.endswith('.png'):
                images.append({'src': filename})
            if filename.endswith('.mp4'):
                videos.append({
                    'image_src': filename.replace('#', '%23').replace('mp4', '%s' % file_format),
                    'src': filename.replace('#', '%23')
                })

    return render_template_string(TEMPLATE, **{
        'images': images,
        'videos': videos
    })


@app.route('/delete/<path:filename>')
def delete(filename):
    print("delete %s" % filename)
    os.remove(filename)
    os.remove(filename.replace('#', '%23').replace('mp4', '%s' % file_format))
    return "deleted"


@app.route('/upload', methods=['POST'])
def upload():
    print(request.files)
    file = request.files['file']
    # if files is .jpg or .png save in pictures folder
    if file.filename.endswith('.jpg') or file.filename.endswith('.png'):
        # save in pictures folder
        file.save(os.path.join(dir_path + "/pictures", file.filename))
    # if files is .mp4 save in videos folder
    if file.filename.endswith('.mp4'):
        # save in videos folder
        file.save(os.path.join(dir_path + "/videos", file.filename))
    return "uploaded"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
