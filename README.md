**Crawler**

    An Application to crawl and generate sitemap based on user input.

**Installation guide**

python version: 3.8

1) Clone the repository

2) Setup a virtual environment

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

   For Linux or macOs users

       uwsgi --ini uwsgi.ini

   For Windows users

       set FLASK_APP=app.py
       flask run
