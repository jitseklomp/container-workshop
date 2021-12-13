# Labs - pt. 2

Running single Pods is fun but let's move to a new abstraction level: Deployments

## Deployments

1. Create deployment "nginx" with image `nginx:1.18.0`, called nginx, having 2 replicas, defining port 80 as the port that this container exposes

```shell
$ kubectl create deployment --image=nginx:1.18.0 --replicas=2 --port=80 nginx \
    --dry-run=client -o yaml > deployment-nginx.yaml

$ kubectl create -f deployment-nginx.yaml
deployment.apps/nginx created
```

2. Check how the deployment rollout is going

```shell
$ kubectl rollout status deployment nginx 
deployment "nginx" successfully rolled out
```

3. Update the nginx image to nginx:1.19.8, check the rollout history and confirm that the replicas are OK

```shell
$ sed -i -e 's/1.18.0/1.19.8/g' deployment-nginx.yaml 

$ kubectl apply -f deployment-nginx.yaml 
Warning: resource deployments/nginx is missing the kubectl.kubernetes.io/last-applied-configuration annotation which is required by kubectl apply. kubectl apply should only be used on resources created declaratively by either kubectl create --save-config or kubectl apply. The missing annotation will be patched automatically.
deployment.apps/nginx configured

$ kubectl rollout status deployment nginx
Waiting for deployment "nginx" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "nginx" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "nginx" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "nginx" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "nginx" rollout to finish: 1 old replicas are pending termination...
deployment "nginx" successfully rolled out
```

> The warning from `kubectl apply` can be ignored

4. Update the nginx image to nginx:1.91 and verify that something's wrong with the rollout

```shell
$ sed -i -e 's/1.19.8/1.91.0/g' deployment-nginx.yaml 

$ kubectl apply -f deployment-nginx.yaml 
deployment.apps/nginx configured

$ kubectl rollout status deployment nginx
Waiting for deployment "nginx" rollout to finish: 1 out of 2 new replicas have been updated...
^C
```

5. Undo the latest rollout and verify that new pods have the correct (old) image

```shell
$ kubectl rollout undo deployment nginx 
deployment.apps/nginx rolled back

$ kubectl rollout status deployment nginx
deployment "nginx" successfully rolled out

$ kubectl get pod --selector=app=nginx -o yaml | grep image:
    - image: nginx:1.19.8
      image: docker.io/library/nginx:1.19.8
    - image: nginx:1.19.8
      image: docker.io/library/nginx:1.19.8
```

6. Scale the deployment to 5 replicas

```shell
$ kubectl scale deployment nginx --replicas=5
deployment.apps/nginx scaled

Or (after restoring correct image tag):
$ sed -i -e 's/replicas: 2/replicas: 5/g' deployment-nginx.yaml 
$ kubectl apply -f deployment-nginx.yaml 
deployment.apps/nginx configured
```

## Services

1. Create service "svc-httpd" for the single **Pod** `httpd-new`

```shell
$ kubectl expose pod httpd-new --name=svc-httpd
service/svc-httpd exposed
```

2. Use a temporary UBI **Pod** to `curl` 'http://svc-httpd:8080' and verify the log output of the "httpd-new" pod

```shell
$ kubectl run ubi8-curl --image=registry.access.redhat.com/ubi8-minimal --restart=Never \
    --rm -ti -- curl http://svc-httpd:8080
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<head>
[...]
    </body>
</html>
pod "ubi8-curl" deleted

$ kubectl logs httpd-new
[...]
```

3. Create service "svc-nginx" for the "nginx" deployment

```shell
$ kubectl expose deployment nginx --name=svc-nginx
service/svc-nginx exposed
```

4. Use a temporary UBI **Pod** to `curl` 'http://svc-nginx' and verify requests are balanced across application replicas

```shell
# Repeat a few times
$ kubectl run ubi8-curl --image=registry.access.redhat.com/ubi8-minimal --restart=Never \
    --rm -ti -- curl http://svc-nginx
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
</body>
</html>
pod "ubi8-curl" deleted

# Inspect logs for every nginx pod by executing `kubectl log` for every replica

# Another solution is to use `stern`. Start stern and run `curl` in a new terminal:
$ stern nginx --tail 0
+ nginx-575fc7645b-g954w › nginx
+ nginx-575fc7645b-qqdp5 › nginx
+ nginx-575fc7645b-zpksp › nginx
+ nginx-575fc7645b-f5jhs › nginx
+ nginx-575fc7645b-g86bk › nginx

# Repeat a few times
$ kubectl run ubi8-curl --image=registry.access.redhat.com/ubi8-minimal --restart=Never \
    --rm -ti -- curl http://svc-nginx

# Live log output from stern, you can see the requests are balanced across different Pods:
$ stern nginx --tail 0
+ nginx-575fc7645b-g954w › nginx
+ nginx-575fc7645b-qqdp5 › nginx
+ nginx-575fc7645b-zpksp › nginx
+ nginx-575fc7645b-f5jhs › nginx
+ nginx-575fc7645b-g86bk › nginx
nginx-575fc7645b-zpksp nginx 10.244.0.48 - - [17/Aug/2021:13:54:03 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.61.1" "-"
nginx-575fc7645b-qqdp5 nginx 10.244.0.49 - - [17/Aug/2021:13:54:10 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.61.1" "-"
nginx-575fc7645b-qqdp5 nginx 10.244.0.50 - - [17/Aug/2021:13:54:13 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.61.1" "-"
nginx-575fc7645b-g954w nginx 10.244.0.51 - - [17/Aug/2021:13:54:15 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.61.1" "-"
nginx-575fc7645b-g954w nginx 10.244.0.52 - - [17/Aug/2021:13:54:17 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.61.1" "-"
nginx-575fc7645b-f5jhs nginx 10.244.0.53 - - [17/Aug/2021:13:54:18 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.61.1" "-"
nginx-575fc7645b-qqdp5 nginx 10.244.0.54 - - [17/Aug/2021:13:54:21 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.61.1" "-"
nginx-575fc7645b-g86bk nginx 10.244.0.55 - - [17/Aug/2021:13:54:25 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.61.1" "-"
```

> Stern is available from <https://github.com/wercker/stern>
