# LIME Model Explainer

## Build a Development LIME Explainer Docker Image

First build your docker image by changing directory to kfserving/python and replacing `dockeruser` with your docker username in the snippet below (running this will take some time).

`docker build -t dockeruser/limeserver:latest -f lime-explainer.Dockerfile .`

Then push your docker image to your dockerhub repo (this will take some time)

`docker push dockeruser/limeserver:latest`

Once your docker image is pushed you can pull the image from `dockeruser/limeserver:latest` when deploying an inferenceservice by specifying the image in the yaml file.

## Example 

Try deploying [Lime with MNIST](https://github.com/drewbutlerbb4/kfserving/tree/master/docs/samples/explanation/aix/mnist)
