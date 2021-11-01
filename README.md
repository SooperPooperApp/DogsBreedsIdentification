# DogsBreedsIdentification
Identification of a dog breed based on Machine Learning

This project has two parts.

TensorFlow model and “Web API” for the prediction dogs breed.

# Model:
Stored in the directory "model".

BreedsModel.ipynb – file for training model in the Jupyter Notebok.
The scipt based on the Stanford Dogs Dataset except that added 6 new breads and save model to the “breeds_model126.h5” in the current directory.
Model based on the pretained model AlexNet. Directory **"input"** in the script location must contains train dataset. 
For restriction reason of the size on the git repository, dataset stored externally in the http://134.249.147.120/DogBreeds/ImageBreeds/

TODO - Requires an approved storage in a archive

# API:

## How it works. 
The model size for the predicion about 90MB. If we trying using classic cgi script, each session will load 90MB of data. This is an overhead. 
Another case that python load tensorflow library is very long. So using python script directly is very slow.

## Decision
We wrote the light python cgi script that connect to the message broker and sent image. 
Message broker loaded earlier and load the model and tensorflow library once. It work as service permanent loaded in memory. 
It can load balancing so in ideal cases number instance it must be equals number of threads CPU. 

# Files
www/breads.html - testing prediction without client from the browser  
cgi/DocClient.py - API for the prediction. Returns result in JSON format  
service/rpc_server.py - Messsage broker using Rabbit MQ server  
service/norm_class_rate_to_JS.py - tools that convert cvs format to json  




