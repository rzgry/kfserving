# Using LIME to get explanations for MNIST classifications

To deploy the inferenceservice

`kubectl apply -f lime-explainer.yaml`

Then find the url

`kubectl get inferenceservice`

```
NAME         URL                                                                                             READY   DEFAULT TRAFFIC   CANARY TRAFFIC   AGE
limeserver   http://limeserver.drewbutlerbb4-cluster.sjc03.containers.appdomain.cloud/v1/models/limeserver   True    100                                40m
```

Query the inferenceservice with the url

`python query_explain.py http://limeserver.drewbutlerbb4-cluster.sjc03.containers.appdomain.cloud/v1/models/limeserver`

To try a different MNIST example add a number to the end of the query

`python query_explain.py http://limeserver.drewbutlerbb4-cluster.sjc03.containers.appdomain.cloud/v1/models/limeserver 100`

## Deploying LIME explanations for another Image Classifier

This section is for users who have another Image classifier which you would like to get explanations for. Change the image from `ibmandrewbutler/lime-server:predictor` to the endpoint of your image in lime-explainer.yaml.

```
name: predictor
image: <your image endpoint>
```

Then deploy your inferenceservice.

`kubectl apply -f lime-explainer.yaml`

## Deploying a Development Explainer Image

To deploy a development image go to `lime-explainer.yaml` and change the original explainer image to the endpoint of your image.

```
name: explainer
image: <your image endpoint>
```

Then deploy your inferenceservice.

`kubectl apply -f lime-explainer.yaml`

## Troubleshooting

`<504> Gateway Timeout <504>` - the explainer is probably taking to long and not sending a response back quickly enough. Either there aren't enough resources allocated or the number of samples the explainer is allowed to take needs to be reduced. To fix this go to lime-explainer.yaml and increase resources. Or to lower the number of allowed samples go to lime-explainer.yaml and add a flag to `explainer: command:` '--num_samples' (the default number of samples is 1000)
