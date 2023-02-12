# StaccTask2023

A flask application.

Tech stack:

LookerStudio - Data display 

Flask framework - Server side 

Swagger - Api doc

Python - Language

Docker - "Deployment"




## Task description

The rise in energy prices has made consumers more aware of their consumption. However, many still find it difficult to navigate through all the power providers and various power plans. Consumers may also want to know how to make their homes more energy efficient.

To track the user's power usage, we would like to make an API call to [elvia (https://www.elvia.no/smart-forbruk/alt-om-din-strommaler/api-for-malerverdier-tilgjengelig-i-pilot-na/)]. However, this costs money, so with some magic... we pretend that we already have the user's consumption data. We only ask the user for their property type, size, and last bill. Then, we provide a "blog" based on their usage and give them some graphs. We also tell them whether they have a good or bad power provider.


I have made some modifications to the data and altered the power plans. I have also included a generated spot price for the consumption.

## How to run

Clone the repo

```console 

git clone https://github.com/Tobbelobby/StaccTask2023.git


```
Move in to the flaskApplication folder


```console

cd path/to/folder

```

Install all the dependence, but first make a virtual environment
```console 

python3 -m venv env 


```

```console

source env/bin/activate

```

```console

pip install -r requirements.txt

```

Run the application 

```console

python app.py

```

Take a look !!! 

You can find the api doc at localhost:port/api/docs/

I have also provided a Docker file. Move into the flaskApplication folder.
Build the container:

```console

docker build -t app_name .

```

Start the container, add -d for detached.  

```console

docker run -p 5000:5000 app_name

```





## Comments

There are many things to comment on. The plan was to host the site on pythonanywhere, but they were more strict than I expected. It won't run with the Swagger implementation or the data_manager.py module.

Flask is a great backend tool, but not for the frontend. So, with only HTML and vanilla CSS, it was a bit tedious. If I had more time, I could have implemented React, but I don't have much experience with JS, so that would take some time.




