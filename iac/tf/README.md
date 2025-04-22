# Deploy the app to a Kubernetes cluster

You need either OpenTofu or Terraform installed on your machine to use the configuration in this directory.

Install the Kubernetes provider:

```sh
tofu init
# or
terraform init
```

The configuration does not specify any authentication for the Kubernetes provider. Use environment variables to configure access to the target cluster. See provider docs ([OpenTofu](), [Terraform](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs)) for details.

Apply the configuration:

```sh
tofu apply
# or
terraform apply
```

The configuration defines the URL of the user interface as an output named `url`. Open the URL with your browser to use the application.
