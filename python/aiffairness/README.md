# AIF Model Fairness

## Build a Development AIF Model Explainer Docker Image

First build your docker image by changing directory to kfserving/python and replacing dockeruser with your docker username in the snippet below (running this will take some time).

docker build -t dockeruser/aifserver:latest -f aiffairness.Dockerfile .

Then push your docker image to your dockerhub repo (this will take some time)

docker push dockeruser/aifserver:latest

Once your docker image is pushed you can pull the image from dockeruser/aifserver:latest when deploying an inferenceservice by specifying the image in the yaml file.
