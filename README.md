# APPROOV DYNAMIC MODULE FOR NGINX PLUS

The Approov dynamic module for NGINX Plus will show how simple is to integrate the [Approov Token](https://www.approov.io/docs/latest/approov-usage-documentation/#approov-tokens) check to protect the access to an API backend, without requiring any changes to its code, by leveraging the NGINX Plus support for dynamic modules in order to include the Approov Token check functionality, that only requires minimal changes to the actual NGINX Plus configuration.

If you landed in this repo without any prior knowledge about [Approov](https://approov.io/), then take a look at our overall architecture:

![Approov Architecture](/docs/assets/img/approov-overall-architecture.png)

Now if you are serious or just curious about API and Mobile App security, then we invite you to keep tabs on our [Blog](https://blog.approov.io), that its regularly updated with educational content on this topics.


## APPROOV TOKEN QUICK START

Please follow this [guide](/docs/APPROOV_QUICK_START.md) for a quick start on integrating Approov in your current NGINX Plus instance.

## APPROOV TOKEN BINDING QUICK START

The [Approov Token Binding](https://approov.io/docs/latest/approov-usage-documentation/#token-binding) is an advanced feature of Approov that lets you to bind another header in the request with the Approov Token itself. For example the Authorization header.

Please follow this [guide](/docs/APPROOV_TOKEN_BINDING_QUICK_START.md) for a quick start on integrating the Approov Token Binding in your current NGINX Plus instance.

## APPROOV DEMO

The [Approov demo](/docs/APPROOV_DEMO.md) has the goal of showing to bot experienced and inexperienced NGINX Plus users how Approov can be integrated in a new NGINX Plus instance. The [Approov Token Binding](https://approov.io/docs/latest/approov-usage-documentation/#token-binding) advanced feature is also included in the demo.
