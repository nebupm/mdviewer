# Docker and Kubernetes

Containers at scale is resolved by K8s.
Eventhough, It can be done manually, but k8s will give scheduling, scaling, healing and updating containers at scale automatically.

Each node with worloads, will have a container runtime and a k8s agent. All this will be controlled by the control plane.
K8s is always looking for a desired vs actual state of the cluster. If there are changes, then it will be addressed automatically.
This is done all automatically.

If your app is running your app of K8s, then the migration of your app acroos cloud or on and off the cloud is seamless.
So, if your app is developed using K8s, then it can be deployed first on premise and then moved to cloudA and if you dont like cloudA and want to move to cloudB, it is seamless to move it across the cloud platform.

Stateless data vs Stateful data in the apps.
Stateless data is data that does not depend on the previous state of the application. It can be easily replicated and scaled across multiple instances. Examples include web servers, API servers, and microservices.
- It doesnt need to remember the data across nodes. Webserver is one such example. 

Stateful data, on the other hand, is data that depends on the previous state of the application. It requires persistent storage and cannot be easily replicated or scaled across multiple instances. Examples include databases, message queues, and file storage systems.
- It has to remember stuff. for example DB. If data in the DB is stored by node1 and if the node1 fails after sometime, then data should be available on node2 as well.
  
