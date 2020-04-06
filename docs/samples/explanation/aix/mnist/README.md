# Using AIX to get explanations for MNIST classifications

To deploy the inferenceservice

`kubectl apply -f aix-explainer.yaml`

Then find the url.

`kubectl get inferenceservice`

```
NAME         URL                                               READY   DEFAULT TRAFFIC   CANARY TRAFFIC   AGE
aixserver   http://aixserver.somecluster/v1/models/aixserver   True    100                                40m
```

Query the inferenceservice with the url and append `:explain` to signify the query is asking for an explanation.

```
python query_explain.py http://aixserver.somecluster/v1/models/aixserver:explain
```

To try a different MNIST example add an integer to the end of the query between 0-10,000. The integer chosen will be the index of the image to be chosen in the MNIST dataset.

```
python query_explain.py http://aixserver.somecluster/v1/models/aixserver:explain 100
```

## Deploying AIX explanations for another Image Classifier

This section is for users who have another Image classifier which you would like to get explanations for. Change the image from `aipipeline/aix-explainer:0.2.2` to the endpoint of your image in aix-explainer.yaml.

```
name: predictor
image: <your image endpoint>
```

Then deploy your inferenceservice.

`kubectl apply -f aix-explainer.yaml`

## Deploying a Development Explainer Image

To deploy a development image go to `aix-explainer.yaml` and change the original explainer image to the endpoint of your image.

```
name: explainer
image: <your image endpoint>
```

Then deploy your inferenceservice.

`kubectl apply -f aix-explainer.yaml`

## Stopping the Inference Service

`kubectl delete inferenceservice limeserver`

## Troubleshooting

`<504> Gateway Timeout <504>` - the explainer is probably taking to long and not sending a response back quickly enough. Either there aren't enough resources allocated or the number of samples the explainer is allowed to take needs to be reduced. To fix this go to aix-explainer.yaml and increase resources. Or to lower the number of allowed samples go to aix-explainer.yaml and add a flag to `explainer: command:` '--num_samples' (the default number of samples is 1000)

If you see `Configuration "aixserver-explainer-default" does not have any ready Revision` the container may have taken too long to download. If you run `kubectl get revision` and see your revision is stuck in `ContainerCreating` try deleting the inferenceservice and redeploying.
