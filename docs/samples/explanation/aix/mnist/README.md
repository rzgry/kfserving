# Using LIME to get explanations for MNIST classifications

To deploy the inferenceservice

`kubectl apply -f lime-explainer.yaml`

Then find the url.

`kubectl get inferenceservice`

```
NAME         URL                                                  READY   DEFAULT TRAFFIC   CANARY TRAFFIC   AGE
limeserver   http://limeserver.somecluster/v1/models/limeserver   True    100                                40m
```

Query the inferenceservice with the url and append `:explain` to signify the query is asking for an explanation.

```
python query_explain.py http://limeserver.somecluster/v1/models/limeserver:explain
```

To try a different MNIST example add an integer to the end of the query between 0-10,000. The integer chosen will be the index of the image to be chosen in the MNIST dataset.

```
python query_explain.py http://limeserver.somecluster/v1/models/limeserver:explain 100
```

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

## Stopping the Inference Service

`kubectl delete inferenceservice limeserver`

## Troubleshooting

`<504> Gateway Timeout <504>` - the explainer is probably taking too long and not sending a response back quickly enough. Either there aren't enough resources allocated or the number of samples the explainer is allowed to take needs to be reduced. To fix this go to lime-explainer.yaml and increase resources. Or to lower the number of allowed samples go to lime-explainer.yaml and add a flag to `explainer: command:` '--num_samples' (the default number of samples is 1000)


`<Response [404]>` - Make sure to add `:explain` to the end of the inferenceservice url. Otherwise try taking down the inferenceservice with `kubectl delete inferenceservice limeserver` and then putting it back up again with the `kubectl apply` command used previously.
