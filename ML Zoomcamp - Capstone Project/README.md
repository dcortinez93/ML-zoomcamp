# Cardiovascular Disease dataset

## Problem Description

Our Health is one of the things that are relevant to all people because it influences the way you live your life. Since we don't want to get sick, we want to take care of it. However, there are multiple variables that we need to make sure that were are doing (or avoiding) to be as healthy as possible, and sometimes we can't do that. For example, avoiding high cholesterol, eating sugar, smoking and consuming  alcohol while maximizing our physical activity are common recommendations for a healthy lifestyle, but some of them are hard to avoid. As a result, we might get sick. A good example of a sickness related to those variables is cardiovascular disease. Considering all of this, a model that can predict if you are going to have a cardiovascular disease considering your gender, age, weight, height, and other variables related to your body and lifestyle could give us some insight into our lives. We might want to reconsider the way we are living it, and if we need to change it as soon as possible to avoid taking a path from which we can't return.



## Data Description
I used a dataset from Kaggle: https://www.kaggle.com/sulianova/cardiovascular-disease-dataset and added the file to this repository.

There are 3 types of input features:

    Objective: factual information;

    Examination: results of medical examination;

    Subjective: information given by the patient.

Features:

    Age | Objective Feature | age | int (days)

    Height | Objective Feature | height | int (cm) |

    Weight | Objective Feature | weight | float (kg) |

    Gender | Objective Feature | gender | categorical code |

    Systolic blood pressure | Examination Feature | ap_hi | int |

    Diastolic blood pressure | Examination Feature | ap_lo | int |

    Cholesterol | Examination Feature | cholesterol | 1: normal, 2: above normal, 3: well above normal |

    Glucose | Examination Feature | gluc | 1: normal, 2: above normal, 3: well above normal |

    Smoking | Subjective Feature | smoke | binary |

    Alcohol intake | Subjective Feature | alco | binary |

    Physical activity | Subjective Feature | active | binary |

    Presence or absence of cardiovascular disease | Target Variable | cardio | binary |
All of the dataset values were collected at the moment of medical examination.


## Data preparation, data cleaning, and EDA
Are on the file notebook.ipynb.

## Model Training
It's on the file notebook.ipynb. and train.py.

## Training the final model (Random Forest Classifier)
On train.py which creates model.bin

## Model deployment
Model is deployed with Flask in predict.py

## Testing
There are two testing files: test_service_local and test_service_cloud. Change the data in the dictionary to try different values.

## Dependency and environment management
Pipfile and Pipfile.lock. The packages use are numpy, scikit-learn==0.24.2, flask, waitress and requests
The dependencies where installed executing this line of code in cmd inside the project folder:
                  
    pipenv install numpy scikit-learn==0.24.2 flask waitress requests 

The environment can be activated using this other line of code in the same cmd:
    
    pipenv shell


## Containerization
I have two Dockerfiles : Dockerfile local and Dockerfile cloud

### Dockerfile local:

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



To run this file, first, change the name from Dockerfile local to Dockerfile, or copy the content of the first into the other file. 
Second, install and open Docker Desktop. Then, open a cmd on the project folder and execute these to lines together:

    docker build -t capstone-project -f Dockerfile .
    docker run -it --rm -p 9696:9696 cpastone-project

To test it, open another cmd, go to the project folder and execute:

    python test_service_local.py

### Dockerfile cloud:

    FROM agrigorev/zoomcamp-model:3.8.12-slim

    RUN pip install pipenv

    WORKDIR /app

    COPY ["Pipfile", "Pipfile.lock", "./"]

    RUN pipenv install --system --deploy

    COPY ["predict.py", "model.bin", "./"]

    #Doesn't expose the port  9696
    CMD waitress-serve --listen=0.0.0.0:$PORT predict:app


To use this file, first, change the name from Dockerfile cloud to Dockerfile, or copy the content of the first into the other file. This file is used for Cloud deployment, and the steps to do this are described below:

  1-First, you need to install the Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli . 

  2-Then open a cmd and go to the folder of the project. Later, type:

    heroku login

  3-After this, login into the opened horuko tab. The message "Login in...done" will appear. Then execute this command on the cmd:

    heroku container:login

  4-After this, the message "Login Succeeded" will appear and you can create an app by executing this command, where name is the name of the app,you can choose one that is not already in use (I chose "capstone-cardio").

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

Video Example:


https://user-images.githubusercontent.com/45173309/145732268-72c9e0b0-9294-48fa-952c-b16bd0b0115e.mp4



