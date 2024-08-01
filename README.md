# Crawler

Crawler is a Flask-based web application that crawls a given website and generates an XML sitemap. The application allows users to input an URL, initiates the crawling process, and provides the sitemap for download. The system does not follow any external links and only crawls within the specified domain.

# Installation guide

    Dependency: python 3.8

1) Clone the repository

    Clone using https as follows

        https://github.com/Harshith-J-L/crawler.git

2) Setup a virtual environment(Optional)

    Navigate to the project and create a virtual environment as follows

        cd path/to/your/project
        
        python3 -m venv myapp
    
    Activate the virtual environment by running the following command

    For Linux or macOS users

       source myapp/bin/activate

    For Windows Users

       myapp\Scripts\activate

2) Install the dependencies using requirements.txt file

        pip install -r requirements.txt

3) Run the application as follows

   For Linux or macOS users

       uwsgi --ini uwsgi.ini

   For Windows users

       set FLASK_APP=app.py
       flask run

# How to use ?

    After successful installation, the application will be running at http://localhost:5000.

    The user can either use an API or an interface to input the URL to start the crawling

    Use API as follows

        http://localhost:5000/v1/crawl?url=https://www.example.com
    
    To input through an interface, open any browser and enter http://localhost:5000
