# 2. Webapps with Docker

Great! So you have now looked at `docker run`, played with a Docker container and also got the hang of some terminology. Armed with all this knowledge, you are now ready to get to the real stuff &#8212; deploying web applications with Docker.

## 2.1 Run a static website in a container

>**Note:** Code for this section is in this repo in the [static-site directory](https://github.com/jitseklomp/workshop-labs/tree/master/containers/static-site).

Let's start by taking baby-steps. First, we'll use Docker to run a static website in a container. The website is based on an existing image. We'll pull a Docker image from Docker Hub, run the container, and see how easy it is to set up a web server.

The image that you are going to use is a single-page website that was already created for this demo and is available on the Docker Hub as [`dockersamples/static-site`](https://hub.docker.com/r/dockersamples/static-site). You can download and run the image directly in one go using `docker run` as follows.

```console
$ docker run -d dockersamples/static-site
```

>**Note:** Thus image doesn't run without the `-d` flag. The `-d` flag enables **detached mode**, which detaches the running container from the terminal/shell and returns your prompt after the container starts.

So, what happens when you run this command?

Since the image doesn't exist on your Docker host, the Docker daemon first fetches it from the registry and then runs it as a container.
Now that the server is running, do you see the website? What port is it running on? And more importantly, how do you access the container directly from our host machine?

Actually, you probably won't be able to answer any of these questions yet! &#9786; In this case, the client didn't tell the Docker Engine to publish any of the ports, so you need to re-run the `docker run` command to add this instruction.

Let's re-run the command with some new flags to publish ports and pass your name to the container to customize the message displayed. We'll use the *-d* option again to run the container in detached mode.

First, stop the container that you have just launched. In order to do this, we need the container ID. Since we ran the container in detached mode, we don't have to launch another terminal to do this. Run `docker ps` to view the running containers.

```console
$ docker ps
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS               NAMES
a7a0e504ca3e        dockersamples/static-site   "/bin/sh -c 'cd /usr/"   28 seconds ago      Up 26 seconds       80/tcp, 443/tcp     stupefied_mahavira
```

Check out the `CONTAINER ID` or `NAME` column. You will need to use one of these values to identify the container you want to stop, and then to remove it. The example below provides the `CONTAINER ID` on our system; you should use the value that you see in your terminal.

```bash
$ docker stop a7a0e504ca3e
a7a0e504ca3e
$ docker rm   a7a0e504ca3e
a7a0e504ca3e
```

Now, let's launch a new container mode as shown below:

```bash
$ docker run -d --name static-site -e AUTHOR="you" -P dockersamples/static-site
e61d12292d69556eabe2a44c16cbd54486b2527e2ce4f95438e504afb7b02810
```

We used a few extra flags in the above command:

* `--name` allows you to specify a container name
* `-e` is how you pass environment variables to the container
* `AUTHOR` is the environment variable name and `Your Name` is the value that you can pass
* `-d` will create a container with the process detached from our terminal
* `-P` will publish all the exposed container ports to random ports on the Docker host

>**Note:** A container name is automatically generated if you do not specify one

Now you can see the ports by running the `docker port` command.

```bash
$ docker port static-site
443/tcp -> 0.0.0.0:49155
443/tcp -> :::49155
80/tcp -> 0.0.0.0:49156
80/tcp -> :::49156
```

You can now open `http://localhost:[YOUR_PORT_FOR 80/tcp]`. For our example this is `http://localhost:49156`:

```console
$ curl -s localhost:49156
<!DOCTYPE html><html>

<head>
<meta charset="utf-8">
<style type="text/css">
body {
  font-family: Helvetica, arial, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  padding-top: 10px;
[...]
```

As you can see a HTML page is returned! You can also open `http://<YOUR_DOCKER_MACHINE>:[YOUR_PORT_FOR 80/tcp]` to see your site live! For our example, this is: `http://192.168.130.200:49156`.

<img src="../images/static.png" title="static">

You can also run a second webserver at the same time, specifying a custom host port mapping to the container's webserver:

```bash
$ docker run --name static-site-2 -e AUTHOR="Your Name" -d -p 8888:80 dockersamples/static-site
```

<img src="../images/static-2.png" title="static">

To deploy this on a real server you would just need to install Docker, and run the above `docker` command.

Now that you've seen how to run a webserver inside a Docker container, how do you create your own Docker image? This is the question we'll explore in the next section.

But first, let's stop and remove the containers since you won't be using them anymore.

```console
$ docker stop static-site
static-site
$ docker rm static-site
static-site
```

Let's use a shortcut to remove the second site:

```console
$ docker rm -f static-site-2
static-site-2
```

Run `docker ps` to make sure the containers are gone.

```console
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

## 2.2 Docker Images

In this section, let's dive deeper into what Docker images are. You will build your own image and use that image to run an application locally.

Docker images are the basis of containers. In the previous example, you **pulled** the *dockersamples/static-site* image from the registry and asked the Docker client to run a container **based** on that image. To see the list of images that are available locally on your system, run the `docker images` command.

```console
$ docker images
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
dockersamples/static-site   latest              92a386b6e686        2 hours ago        190.5 MB
nginx                  latest              af4b3d7d5401        3 hours ago        190.5 MB
python                 2.7                 1c32174fd534        14 hours ago        676.8 MB
postgres               9.4                 88d845ac7a88        14 hours ago        263.6 MB
containous/traefik     latest              27b4e0c6b2fd        4 days ago          20.75 MB
node                   0.10                42426a5cba5f        6 days ago          633.7 MB
redis                  latest              4f5f397d4b7c        7 days ago          177.5 MB
mongo                  latest              467eb21035a8        7 days ago          309.7 MB
alpine                 3.3                 70c557e50ed6        8 days ago          4.794 MB
java                   7                   21f6ce84e43c        8 days ago          587.7 MB
```

Above is a list of images that I've pulled from a registry and those I've created myself (we'll shortly see how). You will have a different list of images on your machine. The `TAG` refers to a particular snapshot of the image and the `ID` is the corresponding unique identifier for that image.
For simplicity, you can think of an image akin to a git repository - images can be [committed](https://docs.docker.com/engine/reference/commandline/commit/) with changes and have multiple versions. When you do not provide a specific version number, the client defaults to `latest`.

For example you could pull a specific version of `ubuntu` image as follows:

```console
$ docker pull ubuntu:18.04
18.04: Pulling from library/ubuntu
284055322776: Pull complete 
Digest: sha256:0fedbd5bd9fb72089c7bbca476949e10593cebed9b1fb9edf5b79dbbacddd7d6
Status: Downloaded newer image for ubuntu:18.04
docker.io/library/ubuntu:18.04
```

If you do not specify the version number of the image then, as mentioned, the Docker client will default to a version named `latest`.
So for example, the `docker pull` command given below will pull an image named `ubuntu:latest`:

```bash
$ docker pull ubuntu
Using default tag: latest
latest: Pulling from library/ubuntu
7b1a6ab2e44d: Pull complete 
Digest: sha256:626ffe58f6e7566e00254b638eb7e0f3b11d4da9675088f4781a50ae288f3322
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest
```

To get a new Docker image you can either get it from a registry (such as the Docker Hub) or create your own. There are hundreds of thousands of images available on [Docker Hub](https://hub.docker.com). You can also search for images directly from the command line using `docker search`.

An important distinction with regard to images is between _base images_ and _child images_.

* **Base images** are images that have no parent images, usually images with an OS like ubuntu, alpine or debian.
* **Child images** are images that build on base images and add additional functionality.

Another key concept is the idea of _official images_ and _user images_. (Both of which can be base images or child images.)

* **Official images** are Docker sanctioned images. Docker, Inc. sponsors a dedicated team that is responsible for reviewing and publishing all Official Repositories content. This team works in collaboration with upstream software maintainers, security experts, and the broader Docker community. These are not prefixed by an organization or user name. In the list of images above, the `python`, `node`, `alpine` and `nginx` images are official (base) images. To find out more about them, check out the [Official Images Documentation](https://docs.docker.com/docker-hub/official_repos/).

* **User images** are images created and shared by users like you. They build on base images and add additional functionality. Typically these are formatted as `user/image-name`. The `user` value in the image name is your Docker Hub user or organization name.

## 2.3 Create your first image

>**Note:** The code for this section is in this repository in the [flask-app](https://github.com/jitseklomp/workshop-labs/tree/master/containers/flask-app) directory.

Now that you have a better understanding of images, it's time to create your own. Our goal here is to create an image that sandboxes a small [Flask](https://flask.palletsprojects.com) application.
We'll do this by first pulling together the components for a random cat picture generator built with Python Flask, then _dockerizing_ it by writing a _Dockerfile_. Finally, we'll build the image, and then run it.

### 2.3.1 Create a Python Flask app that displays random cat pix

For the purposes of this workshop, we've created a fun little Python Flask app that displays a random cat `.gif` every time it is loaded - because, you know, who doesn't like cats?

Start by creating a directory called `flask-app` where we'll create the following files:

* [app.py](#apppy)
* [requirements.txt](#requirementstxt)
* [templates/index.html](#templatesindexhtml)

Make sure to `cd flask-app` before you start creating the files, because you don't want to start adding a whole bunch of other random files to your container image.

#### app.py

Create the `app.py` file with the following content:

```python
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
```

#### requirements.txt

In order to install the Python modules required for our app, we need to create a file called `requirements.txt` and add the following line to that file:

```python
Flask==0.10.1
```

#### templates/index.html

Create a directory called `templates` and create an `index.html` file in that directory with the following content in it:

```html
<html>
  <head>
    <title>Cat Gif of the day</title>
    <style type="text/css">
      body {
        background: black;
        color: white;
      }
      div.container {
        max-width: 500px;
        margin: 100px auto;
        border: 20px solid white;
        padding: 10px;
        text-align: center;
      }
      h4 {
        text-transform: uppercase;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h4>Cat Gif of the day</h4>
      <img src="{{url}}" />
      <p><small>Courtesy: <a href="https://giphy.com/search/cat">GIPHY</a></small></p>
    </div>
  </body>
</html>
```

### 2.3.2 Write a Dockerfile

We want to create a Docker image with this web app. As mentioned above, all user images are based on a _base image_. Since our application is written in Python, we will build our own Python image based on [Alpine](https://hub.docker.com/_/alpine). We'll do that using a **Dockerfile**.

A [Dockerfile](https://docs.docker.com/engine/reference/builder/) is a text file that contains a list of commands that the Docker daemon calls while creating an image. The Dockerfile contains all the information that Docker needs to know to run the app &#8212; a base Docker image to run from, location of your project code, any dependencies it has, and what commands to run at start-up. It is a simple way to automate the image creation process. The best part is that the [commands](https://docs.docker.com/engine/reference/builder/) you write in a Dockerfile are *almost* identical to their equivalent Linux commands. This means you don't really have to learn new syntax to create your own Dockerfiles.

Create a file called `Dockerfile`, and add content to it as described below. We'll start by specifying our base image, using the `FROM` keyword:

```dockerfile
FROM alpine:3.15
```

The next step usually is to write the commands of copying the files and installing the dependencies. But first we will install the Python pip package to the alpine linux distribution. This will not just install the pip package but any other dependencies too, which includes the python interpreter. Add the following [RUN](https://docs.docker.com/engine/reference/builder/#run) command next:

```dockerfile
RUN apk add --update py3-pip
```

It is now time to add the files that make up the Flask Application. As our app needs Flask we will first install the Python requirements for our app to run. This will be accomplished by adding the lines:

```dockerfile
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt
```

Copy the files you have created earlier into our image by using [COPY](https://docs.docker.com/engine/reference/builder/#copy) command.

```dockerfile
COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/
```

Since our flask app is running on port `5000` we need to tell Docker to expose this port when running the container:

```dockerfile
EXPOSE 5000
```

The last step is the command for running the application which is simply `python3 ./app.py`. Use the [CMD](https://docs.docker.com/engine/reference/builder/#cmd) command to do that:

```dockerfile
CMD ["python3", "/usr/src/app/app.py"]
```

The primary purpose of `CMD` is to tell the container which command it should run by default when it is started.

Our `Dockerfile` is now ready. This is how it looks:

```dockerfile
# our base image
FROM alpine:3.15

# Install python and pip
RUN apk add --update py3-pip

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python3", "/usr/src/app/app.py"]
```

### 2.3.3 Build the image

Now that you have your `Dockerfile`, you can build your image. The `docker build` command does the heavy-lifting of creating a docker image from a `Dockerfile`.
The `docker build` command is quite simple - it takes an optional tag name with the `-t` flag, and the location of the directory containing the `Dockerfile` - the `.` indicates the current directory:

```console
$ docker build -t localhost/cat-gif .
Sending build context to Docker daemon  6.656kB
Step 1/8 : FROM alpine:3.15
3.15: Pulling from library/alpine
59bf1c3509f3: Pull complete 
Digest: sha256:21a3deaa0d32a8057914f36584b5288d2e5ecc984380bc0118285c70fa8c9300
Status: Downloaded newer image for alpine:3.15
 ---> c059bfaa849c
Step 2/8 : RUN apk add --update py3-pip
 ---> Running in 1792d8cfd7e1
fetch https://dl-cdn.alpinelinux.org/alpine/v3.15/main/x86_64/APKINDEX.tar.gz
fetch https://dl-cdn.alpinelinux.org/alpine/v3.15/community/x86_64/APKINDEX.tar.gz
(1/39) Installing libbz2 (1.0.8-r1)
(2/39) Installing expat (2.4.1-r0)
(3/39) Installing libffi (3.4.2-r1)
(4/39) Installing gdbm (1.22-r0)
(5/39) Installing xz-libs (5.2.5-r0)
(6/39) Installing libgcc (10.3.1_git20211027-r0)
(7/39) Installing libstdc++ (10.3.1_git20211027-r0)
(8/39) Installing mpdecimal (2.5.1-r1)
(9/39) Installing ncurses-terminfo-base (6.3_p20211120-r0)
(10/39) Installing ncurses-libs (6.3_p20211120-r0)
(11/39) Installing readline (8.1.1-r0)
(12/39) Installing sqlite-libs (3.36.0-r0)
(13/39) Installing python3 (3.9.7-r4)
(14/39) Installing py3-appdirs (1.4.4-r2)
(15/39) Installing py3-certifi (2020.12.5-r1)
(16/39) Installing py3-charset-normalizer (2.0.7-r0)
(17/39) Installing py3-idna (3.3-r0)
(18/39) Installing py3-urllib3 (1.26.7-r0)
(19/39) Installing py3-requests (2.26.0-r1)
(20/39) Installing py3-msgpack (1.0.2-r1)
(21/39) Installing py3-lockfile (0.12.2-r4)
(22/39) Installing py3-cachecontrol (0.12.10-r0)
(23/39) Installing py3-colorama (0.4.4-r1)
(24/39) Installing py3-contextlib2 (21.6.0-r1)
(25/39) Installing py3-distlib (0.3.3-r0)
(26/39) Installing py3-distro (1.6.0-r0)
(27/39) Installing py3-six (1.16.0-r0)
(28/39) Installing py3-webencodings (0.5.1-r4)
(29/39) Installing py3-html5lib (1.1-r1)
(30/39) Installing py3-parsing (2.4.7-r2)
(31/39) Installing py3-packaging (20.9-r1)
(32/39) Installing py3-tomli (1.2.2-r0)
(33/39) Installing py3-pep517 (0.12.0-r0)
(34/39) Installing py3-progress (1.6-r0)
(35/39) Installing py3-retrying (1.3.3-r2)
(36/39) Installing py3-ordered-set (4.0.2-r2)
(37/39) Installing py3-setuptools (52.0.0-r4)
(38/39) Installing py3-toml (0.10.2-r2)
(39/39) Installing py3-pip (20.3.4-r1)
Executing busybox-1.34.1-r3.trigger
OK: 75 MiB in 53 packages
Removing intermediate container 1792d8cfd7e1
 ---> 9ac14a836e89
Step 3/8 : COPY requirements.txt /usr/src/app/
 ---> f4ef870fdda1
Step 4/8 : RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt
 ---> Running in 11500b918d56
Collecting Flask==2.0.2
  Downloading Flask-2.0.2-py3-none-any.whl (95 kB)
Collecting Jinja2>=3.0
  Downloading Jinja2-3.0.3-py3-none-any.whl (133 kB)
Collecting Werkzeug>=2.0
  Downloading Werkzeug-2.0.2-py3-none-any.whl (288 kB)
Collecting click>=7.1.2
  Downloading click-8.0.3-py3-none-any.whl (97 kB)
Collecting itsdangerous>=2.0
  Downloading itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.0.1.tar.gz (18 kB)
Using legacy 'setup.py install' for MarkupSafe, since package 'wheel' is not installed.
Installing collected packages: MarkupSafe, Werkzeug, Jinja2, itsdangerous, click, Flask
    Running setup.py install for MarkupSafe: started
    Running setup.py install for MarkupSafe: finished with status 'done'
Successfully installed Flask-2.0.2 Jinja2-3.0.3 MarkupSafe-2.0.1 Werkzeug-2.0.2 click-8.0.3 itsdangerous-2.0.1
Removing intermediate container 11500b918d56
 ---> ea90031ecf78
Step 5/8 : COPY app.py /usr/src/app/
 ---> 6e32cf445203
Step 6/8 : COPY templates/index.html /usr/src/app/templates/
 ---> f67007047183
Step 7/8 : EXPOSE 5000
 ---> Running in 50507a267b79
Removing intermediate container 50507a267b79
 ---> e5ff90916df6
Step 8/8 : CMD ["python3", "/usr/src/app/app.py"]
 ---> Running in 11236ca7b2c8
Removing intermediate container 11236ca7b2c8
 ---> 285be30d192a
Successfully built 285be30d192a
Successfully tagged localhost/cat-gif:latest
```

If you don't have the `alpine:3.15` image, the client will first pull the image and then create your image. Therefore, your output on running the command will look different from mine. If everything went well, your image should be ready! Run `docker images` and see if your image (`localhost/cat-gif`) shows.

### 2.3.4 Run your image

The next step in this section is to run the image and see if it actually works.

```console
$ docker run -d -p 8888:5000 --name random-cat-gif localhost/cat-gif
bef1e2fe764f9ae73e07bb0307f791eb00c842dfc85498fbaeb76a3cc87af37e
```

Head over to `http://<YOUR_DOCKER_MACHINE>:8888` and your app should be live!

<img src="../images/catgif.png" title="catgif">

Hit the Refresh button in the web browser to see a few more cat images.

## 2.4 Summary

Here's a quick summary of the few basic commands we used in our Dockerfile.

* `FROM` starts the Dockerfile. It is a requirement that the Dockerfile must start with the `FROM` command. Images are created in layers, which means you can use another image as the base image for your own. The `FROM` command defines your base layer. As arguments, it takes the name of the image. Optionally, you can add the Docker Cloud username of the maintainer and image version, in the format `repository/imagename:version`.

* `RUN` is used to build up the Image you're creating. For each `RUN` command, Docker will run the command then create a new layer of the image. This way you can roll back your image to previous states easily. The syntax for a `RUN` instruction is to place the full text of the shell command after the `RUN` (e.g., `RUN mkdir /user/local/foo`). This will automatically run in a `/bin/sh` shell. You can define a different shell like this: `RUN /bin/bash -c 'mkdir /user/local/foo'`

* `COPY` copies local files into the container.

* `CMD` defines the commands that will run on the Image at start-up. Unlike a `RUN`, this does not create a new layer for the Image, but simply runs the command. There can only be one `CMD` per a Dockerfile/Image. If you need to run multiple commands, the best way to do that is to have the `CMD` run a script. `CMD` requires that you tell it where to run the command, unlike `RUN`. So example `CMD` commands would be:

  ```dockerfile
  CMD ["python", "./app.py"]
  CMD ["/bin/bash", "echo", "Hello World"]
  ```

* `EXPOSE` creates a hint for users of an image which ports provide services. It is included in the information which
 can be retrieved via `$ docker inspect <container-id>`.

  >**Note:** The `EXPOSE` command does not actually make any ports accessible to the host! Instead, this requires 
publishing ports by means of the `-p` flag when using `$ docker run`.  

If you want to learn more about Dockerfiles, check out [Best practices for writing Dockerfiles](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/).
