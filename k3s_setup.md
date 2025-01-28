# Kubernetes Cluster Setup with K3S

This file provides step-by-step instructions to set up a Kubernetes cluster using K3S with a master node and multiple worker nodes.

## Prerequisites

- **Master Node Requirements**: Ubuntu OS with 2 CPU cores (VM can be used).
- **Worker Nodes**: Raspberry Pi devices or equivalent.

## Steps

### 1. Set Up Static IP for Master and Nodes

For each master and node:

1. **SSH into each node**:
   ```bash
   ssh user@<node-ip>
   ```
2. **Get the default gateway IP**:
   ```bash
   ip route | grep default
   ```
   Save the default gateway IP.
3. **Configure static IP**:
   - Run the following command:
     ```bash
     sudo nmtui
     ```
   - Select **Edit a connection**.
   - Edit the wired connection:
     - Set IPv4 configuration to `Manual`.
     - Add a static IP address (e.g., `192.168.0.xxx`, different for each node).
     - Set DNS servers to `8.8.8.8` and `1.1.1.1`.
   - Save and exit the network manager.

### 2. Set Up the Master Node

1. **Prepare the environment**:

   - Use Ubuntu OS with 2 CPU cores.
   - Edit the GRUB configuration:
     ```bash
     sudo nano /etc/default/grub
     ```
     Add the following line:
     ```
     GRUB_CMDLINE_LINUX="cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory"
     ```
   - Apply changes:
     ```bash
     sudo update-grub
     sudo reboot
     ```

2. **Install K3S**:

   ```bash
   curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" sh -s
   ```

3. **Verify K3S installation**:

   ```bash
   systemctl status k3s
   ```

4. **Retrieve cluster information**:

   ```bash
   kubectl cluster-info
   ```

5. **Save the token for nodes**:
   ```bash
   sudo cat /var/lib/rancher/k3s/server/node-token > ~/.kube/node_token
   cat ~/.kube/node_token
   ```
   Save the token for later use.

### 3. Set Up Worker Nodes

1. **SSH into each worker node**:

   ```bash
   ssh pi@<node-ip>
   ```

2. **Install K3S on each worker node**:
   Replace `<master-token>` with the token from the master node and `<master-ip-address>` with the master node's IP address.

   ```bash
   curl -sfL https://get.k3s.io | K3S_TOKEN="<master-token>" K3S_URL="https://<master-ip-address>:6443" K3S_NODE_NAME="<node-name>" sh -s
   ```

3. **Verify K3S agent**:

   ```bash
   sudo systemctl status k3s-agent
   ```

4. **Check the cluster from the master node**:
   ```bash
   sudo kubectl get nodes
   ```

## Notes

- Ensure all nodes have unique static IPs within the same subnet.
- The token retrieved from the master node is required for connecting worker nodes.
- Use `kubectl` commands on the master node to monitor and manage the cluster.

By following these steps, you can successfully set up a Kubernetes cluster using K3S.

# Weather Application Deployment with Master Node Configuration

This README provides step-by-step instructions for deploying a weather application and configuring the Kubernetes cluster to schedule specific workloads on the master node while preventing others from running there.

## Prerequisites

- Kubernetes cluster up and running.
- `kubectl` installed and configured.
- YAML configuration files for the backend, logger, notifications, predictions, and ingress services.

## Steps

### 1. Deploy the Weather Application

Apply all configuration files to deploy the components of the weather application.

```bash
kubectl apply -f ./kube_file/weather_backend.yml
kubectl apply -f ./kube_file/weather_logger.yml
kubectl apply -f ./kube_file/weather_predict.yml
kubectl apply -f ./kube_file/weather_notification.yml
kubectl apply -f ./kube_file/ingress.yml
```

### 2. Label the Master Node

Label the master node to identify it as `masterNode`.

```bash
kubectl label node masterNode node-role.kubernetes.io/master=true
```

### 3. Patch `ingress-nginx-controller` to Add a NodeSelector

Update the `ingress-nginx-controller` Deployment to include a `nodeSelector` in the Pod template spec. This ensures the Pods are scheduled only on the master node.

```bash
kubectl patch deployment ingress-nginx-controller -n ingress-nginx \
--type='json' \
-p='[{"op": "add", "path": "/spec/template/spec/nodeSelector", "value": {"node-role.kubernetes.io/master": "true"}}]'
```

### 4. Taint the Master Node

Add a taint to the master node to prevent other Pods from being scheduled on it unless they explicitly tolerate the taint.

```bash
kubectl taint nodes masterNode dedicated=master:NoSchedule
```

### 5. Patch `ingress-nginx-controller` to Add a Toleration

Update the `ingress-nginx-controller` Deployment to include a toleration, allowing it to bypass the taint and be scheduled on the master node.

```bash
kubectl patch deployment ingress-nginx-controller -n ingress-nginx \
--type='json' \
-p='[{"op": "add", "path": "/spec/template/spec/tolerations", "value": [{"key": "dedicated", "operator": "Equal", "value": "master", "effect": "NoSchedule"}]}]'
```

## Summary of Configuration

### Applied Configuration Files:

- **Backend Service**: `weather_backend.yml`
- **Logger Service**: `weather_logger.yml`
- **Notification Service**: `weather_notification.yml`
- **Prediction Service**: `weather_predict.yml`
- **Ingress Configuration**: `ingress.yml`

### Master Node Configuration:

1. **Node Label**: Added label `node-role.kubernetes.io/master=true` to `masterNode`.
2. **NodeSelector**: Ensured `ingress-nginx-controller` Pods are scheduled on `masterNode` using a NodeSelector.
3. **Taint**: Prevented scheduling of other Pods on `masterNode` with the taint `dedicated=master:NoSchedule`.
4. **Toleration**: Allowed `ingress-nginx-controller` Pods to bypass the taint with a toleration.
   
## Notes

- Ensure the `masterNode` name is correctly replaced in the commands above.
- Verify the changes using `kubectl describe node masterNode` and `kubectl describe deployment ingress-nginx-controller -n ingress-nginx`.

By following these steps, you ensure the weather application's ingress controller runs exclusively on the master node while maintaining control over Pod scheduling.
