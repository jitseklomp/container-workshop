from flask import Flask, render_template
import random

app = Flask(__name__)

# list of cat images
images = [
    "http://i.giphy.com/media/ICOgUNjpvO0PC/giphy.webp",
    "https://i.giphy.com/media/13CoXDiaCcCoyk/giphy.webp",
    "https://i.giphy.com/media/5i7umUqAOYYEw/giphy.webp",
    "https://i.giphy.com/media/JIX9t2j0ZTN9S/giphy.webp",
    "https://i.giphy.com/media/l4KibK3JwaVo0CjDO/giphy.webp",
    "https://i.giphy.com/media/gwjociZExlDqAJWXgO/giphy.webp",
    "https://i.giphy.com/media/gEz3mtYvGgtpigTG1P/giphy.webp",
    "https://i.giphy.com/media/jAkYjgioY9HUc24Y2y/giphy.webp",
    "https://i.giphy.com/media/bU6GKBpWaJ4tO/giphy.webp",
    "https://i.giphy.com/media/MpSgICvhxS2kw/giphy.webp"
    ]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
