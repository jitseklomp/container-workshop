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

### Cluster components

We now have a new, fully functional Kubernetes cluster. Let's investigate! What applications/processes are currently running in Kubernetes?

```console
$ kubectl get --all-namespaces all
NAMESPACE            NAME                                             READY   STATUS        RESTARTS      AGE
kube-system          pod/coredns-78fcd69978-4svdh                     1/1     Running       1 (11m ago)   24h
kube-system          pod/coredns-78fcd69978-q782b                     1/1     Running       1 (11m ago)   24h
kube-system          pod/etcd-kind-control-plane                      1/1     Running       1 (11m ago)   24h
kube-system          pod/kindnet-wgphg                                1/1     Running       1 (11m ago)   24h
kube-system          pod/kube-apiserver-kind-control-plane            1/1     Running       1 (11m ago)   24h
kube-system          pod/kube-controller-manager-kind-control-plane   1/1     Running       1 (11m ago)   24h
kube-system          pod/kube-proxy-xfnw6                             1/1     Running       1 (11m ago)   24h
kube-system          pod/kube-scheduler-kind-control-plane            1/1     Running       1 (11m ago)   24h
local-path-storage   pod/local-path-provisioner-85494db59d-fp8hg      1/1     Running       1 (11m ago)   24h

NAMESPACE     NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
default       service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP                  13s
kube-system   service/kube-dns     ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   24h

NAMESPACE     NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-system   daemonset.apps/kindnet      1         1         1       1            1           <none>                   24h
kube-system   daemonset.apps/kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   24h

NAMESPACE            NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
kube-system          deployment.apps/coredns                  2/2     2            2           24h
local-path-storage   deployment.apps/local-path-provisioner   1/1     1            1           24h

NAMESPACE            NAME                                                DESIRED   CURRENT   READY   AGE
kube-system          replicaset.apps/coredns-78fcd69978                  2         2         2       24h
local-path-storage   replicaset.apps/local-path-provisioner-85494db59d   1         1         1       24h
```

That's quite a lot of stuff for an "empty" cluster!

### Static site

What if we want to run the static-site example from before? We first need a namespace, so let's see what is available:

```console
$ kubectl get namespaces
NAME                 STATUS   AGE
default              Active   24h
kube-node-lease      Active   24h
kube-public          Active   24h
kube-system          Active   24h
local-path-storage   Active   24h
```

All these namespaces (already) contain Kubernetes system components. We do not want to interfere with those so let's create a new empty namespace:

```console
$ kubectl create namespace my-stuff
namespace/my-stuff created
```

Let's check if the namespace is created properly:

```console
$ kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   8m7s
```

That `Service` should not be there, let's try that again:

```console
$ kubectl get all --namespace my-stuff
No resources found in my-stuff namespace.
```

### Pods

Now that we have configured our Namespace we can run our application. We can use `kubectl run` to create a single Pod so let's look at some examples:

```console
$ kubectl run --help | head -n 30
Create and run a particular image in a pod.

Examples:
  # Start a nginx pod
  kubectl run nginx --image=nginx
  
  # Start a hazelcast pod and let the container expose port 5701
  kubectl run hazelcast --image=hazelcast/hazelcast --port=5701
  
  # Start a hazelcast pod and set environment variables "DNS_DOMAIN=cluster" and "POD_NAMESPACE=default" in the container
  kubectl run hazelcast --image=hazelcast/hazelcast --env="DNS_DOMAIN=cluster" --env="POD_NAMESPACE=default"
  
  # Start a hazelcast pod and set labels "app=hazelcast" and "env=prod" in the container
  kubectl run hazelcast --image=hazelcast/hazelcast --labels="app=hazelcast,env=prod"
  
  # Dry run; print the corresponding API objects without creating them
  kubectl run nginx --image=nginx --dry-run=client
  
  # Start a nginx pod, but overload the spec with a partial set of values parsed from JSON
  kubectl run nginx --image=nginx --overrides='{ "apiVersion": "v1", "spec": { ... } }'
  
  # Start a busybox pod and keep it in the foreground, don't restart it if it exits
  kubectl run -i -t busybox --image=busybox --restart=Never
  
  # Start the nginx pod using the default command, but use custom arguments (arg1 .. argN) for that command
  kubectl run nginx --image=nginx -- <arg1> <arg2> ... <argN>
  
  # Start the nginx pod using a different command and custom arguments
  kubectl run nginx --image=nginx --command -- <cmd> <arg1> ... <argN>

```

The `kubectl` tool has a _lot_ of built-in examples and documentation so when in doubt just check `--help`.

Try to create a `static` Pod using the `static-site` example from the previous lab exercise. Make sure to run the pod in the correct Namespace!

## Next steps

1. Create 2 more pods with names `static-2` and `static-3`. All of them should have the label `app=static-site`
2. List all Pods and their labels
3. Add the label `app=static-site` to pod 'static'
4. Create a **Pod** using `registry.access.redhat.com/ubi8-minimal` (using `kubectl`) that runs the command `env`. Run it and check the output.
5. Generate a **Pod** manifest using `registry.access.redhat.com/ubi8-minimal` that runs the command `env`. Set the environment variable `HELLO=WORLD`. Inspect the manifest, apply it and check the output.
6. Create a **Pod** "static-new" running the same static-site container image as before but with port `80` exposed.
7. Get the YAML describing "static" and "static-new" **Pods** and compare
8. Get "static-new" pod's ip created in previous step, use a temporary UBI **Pod** to `curl` its '/'

> Solutions: [solutions-1.md](solutions-1.md)
