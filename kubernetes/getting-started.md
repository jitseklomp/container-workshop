# Getting started with Kubernetes

## Creating a Kubernetes cluster

As setting up a Kubernetes cluster is _way_ beyond the scope of this workshop we will use `kind` (see [https://kind.sigs.k8s.io/](seehttps://kind.sigs.k8s.io/)) to run a local cluster for us *in Docker*. kind was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

### Create a new kind cluster

```shell
$ kind create cluster
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.22.0) 🖼
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Thanks for using kind! 😊
```

## Core concepts

Use the following `kubectl` subcommands: `create`, `get`, `run`, `apply`. Check if tab auto-completion works!

### Exercises

1. Create a **Namespace** called `my-namespace`
2. Generate a YAML manifest file for **Pod** "httpd" running container image `registry.access.redhat.com/ubi8/httpd-24:1-143`
3. Create the "httpd" **Pod** in Kubernetes using the generated YAML
4. Get the YAML for the running "httpd" Pod and compare with generated manifest
5. Create 2 more pods with names `httpd-1` and `httpd-2`. All of them should have the label `app=httpd`
6. List all Pods and their labels
7. Add the label `app=httpd` to pod 'httpd'
8. Create a **Pod** using `registry.access.redhat.com/ubi8-minimal` (using `kubectl`) that runs the command `env`. Run it and check the output.
9. Generate a **Pod** manifest using `registry.access.redhat.com/ubi8-minimal` that runs the command `env`. Set the environment variable `HELLO=WORLD`. Inspect the manifest, apply it and check the output.
10. Create a **Pod** "httpd-new" running the same httpd container image as before but with port `8080` exposed.
11. Get the YAML describing "httpd" and "httpd-new" **Pods** and compare
12. Edit the exported YAML manifest for "httpd-new" to use image tag `1-152` and apply. Check that the Pod is recreated.
13. Get "httpd-new" pod's ip created in previous step, use a temporary UBI **Pod** to `curl` its '/'
14. Advanced:
    1. Create a Pod with `httpd` (`registry.access.redhat.com/ubi8/httpd-24`) container exposed at port 8080. 
    2. Add a `busybox` init container which downloads a page using `wget -O /work-dir/index.html http://example.com`. 
    3. Make a volume of type `emptyDir` and mount it in both containers. For the `httpd` container, mount it on "/var/www/html" and for the initcontainer, mount it on `/work-dir`. 
    4. Fetch the webpage using a UBI pod and `curl`

> We did not get in to `initContainers` and `volumes` during the workshop, see if you can figure out what happens in the below manifest
