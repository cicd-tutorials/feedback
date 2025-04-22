# Deploy the app to a Kubernetes cluster

You need either OpenTofu or Terraform installed on your machine to use the configuration in this directory.

Install the Kubernetes provider:

```sh
tofu init
# or
terraform init
```

The configuration does not specify any authentication for the Kubernetes provider. Use environment variables to configure access to the target cluster. See provider docs ([OpenTofu](https://search.opentofu.org/provider/hashicorp/kubernetes/latest), [Terraform](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs)) for details.

Apply the configuration:

```sh
tofu apply
# or
terraform apply
```

The configuration defines the URL of the user interface as an output named `url`. Open the URL with your browser to use the application.

Use `kubectl exec` (or `kubectl logs`) to see the initial admin password:

```sh
kubectl exec -n feedback $(kubectl get pods -n feedback -o custom-columns=:.metadata.name | grep api.*) -- cat /var/feedback/initial_admin_password
```

Note that the initial admin password is only available within the pod when running the API pod for the first time.

## Use as a module

You can also use the configuration as a module by using `github.com/cicd-tutorials/feedback//iac/tf/module` as the source. For example:

```tf
module "feedback_app" {
  source = "github.com/cicd-tutorials/feedback//iac/tf/module"
}
```

If using `LoadBalancer` as the service type, define `ignore_annotations` attribute in the `kubernetes` provider block to avoid removing annotations added to the resource by the Kubernetes service. For example:

```tf
provider "kubernetes" {
  ignore_annotations = [
    "^service\\.beta\\.kubernetes\\.io\\/.*load.*balancer.*"
  ]
}
```
