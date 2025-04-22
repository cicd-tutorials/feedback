# kind configuration

If you don't have a Kubernetes cluster available for running the application. You can use [kind](https://kind.sigs.k8s.io/) to create a local cluster suitable for development and testing.

To start the cluster, run:

```sh
kind create cluster --config ./config.yaml
```

To configure a KUBECONFIG to use with TF configuration, run:

```sh
kind export kubeconfig --kubeconfig ./kind_kubeconfig.yaml
export KUBE_CONFIG_PATH=$(pwd)/kind_kubeconfig.yaml
```

When using the created cluster with the TF configuration in this repo, use the [kind.tfvars](./kind.tfvars) files to configure the inputs. For example:

```sh
tofu apply -var-file=../kind/kind.tfvars
```

To delete the cluster, run:

```sh
kind delete cluster
```
