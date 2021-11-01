Medical Cost Personal Datasets

Problem Description

Our Health is one of the things that are relevant to all people because it influences the way you live your life. As a result, some people can spend a lot of money on medical expenses trying to preserve their health. One way of making this less expensive is getting medical insurance. The cost of this type of insurance is determined by different factors like smoking, aging, BMI, etc... Because of that, it would be nice if you could know which one of these factors affects to a higher degree the cost of insurance and use that information to change your lifestyle to get cheaper insurance. In this project, we are going to create a model that uses patient data to predict the average medical care expenses. As I described before, this could be used by people that want to know how much will cost their insurance based on their lifestyle or by a health insurance company that wants a guide to determine how much someone should pay.

Data preparation, data cleaning, and EDA
Are on the file notebook.ipynb.

Model Training
It's on the file notebook.ipynb. and train.py.

Training the final model (ExtraTreesRegressor)
On train.py which creates model.bin

Model deployment
Model is deployed with Flask in predict.py

Dependency and environment management
Pipfile and Pipfile.lock. The packages use are numpy, scikit-learn 0.24.2, flask and waitress
The dependencies where installed executing this line of code in cmd inside the project folder:
pipenv install numpy scikit-learn==0.24.2 flask waitress 

The environment can be activated using this other line of code in the same cmd:
pipenv shell

Containerization
I have two Dockerfiles : Dockerfile local and Dockerfile cloud

*****Dockerfile local:

#Base image from dockerhub for python 3.8.12-slim
FROM agrigorev/zoomcamp-model:3.8.12-slim

#Install pipenv
RUN pip install pipenv

#Working directory named 'app'
WORKDIR /app

#Copy those files to the container
COPY ["Pipfile", "Pipfile.lock", "./"]

#Install the dependencies
RUN pipenv install --system --deploy

#Copy these files to the container
COPY ["predict.py", "model.bin", "./"]

#Expose port 9696
EXPOSE 9696

#Configure entry point
ENTRYPOINT ["waitress-serve", "--listen=0.0.0.0:9696", "predict:app"]

To run this file, first, change the name from Dockerfile local to Dockerfile, or copy the content of the first into the other file. Second, install and open Docker Desktop. Then, open a cmd on the project folder and execute these to lines together:

docker build -t midterm-project -f Dockerfile .
docker run -it --rm -p 9696:9696 midterm-project

To test it, open another cmd, go to the project folder and execute:
python test_service.py

*****Dockerfile cloud:

FROM agrigorev/zoomcamp-model:3.8.12-slim

RUN pip install pipenv
 
WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

#Uses other version of predict.py
COPY ["predict_cloud.py", "model.bin", "./"]

#Doesn't expose the port  9696
ENTRYPOINT ["waitress-serve",  "predict:app"]


To use this file, first, change the name from Dockerfile cloud to Dockerfile, or copy the content of the first into the other file. This file is used for Cloud deployment, and the steps to do this are described below:

1-First, you need to install the Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli . 

2-Then open a cmd and go to the folder of the project. Later, type:

heroku login

3-After this, login into the opened horuko tab. The message "Login in...done" will appear. Then execute this command on the cmd:

heroku container:login

4-After this, the message "Login Succeeded" will appear and you can create an app by executing this command, where name is the name of the app,you can choose one that is not already in use.

heroku create name

5-The message "name... done" will appear. After that, execute:

heroku container:push web -a name

6-This will push the container to Heroku. The message "Your image has been successfully pushed. You can now release it with the ..." will appear. Now, we need to release it by executing:

heroku container:release web -a name

7- The message "Releasing images web to name...done" will appear. After this step, the service is deployed to the cloud and we should be able to test this app. First, we need to modify this parameter on the file test_service_cloud.py
url = 'https://name.herokuapp.com/predict'
Replacing the name with the name that you used in the deployment.
Then, open a new cmd on the project folder and executing:
python test_service_cloud.py

However, I'm getting an error on consuming the app and I don't know how to solve it. So, if you have any feedback it will be appreciated. I suspect is related to predict_cloud.py. You can check the error by typing on the cmd used for the docker deployment:
heroku logs --tail -a name
