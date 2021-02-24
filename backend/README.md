# I Reporter
## Description
Corruption is a huge bane to Africa’s development. African countries must develop novel and localised solutions that will curb this menace, hence the introduction to ireport.It is an application that enables users to fight corruption through filing redflags/flag reports. The users setup an account, naviagate to create their reports and check regularly to keep tabs on their reports




## Setup and Installation

To get the project .......

##### Cloning the repository:

```bash
https://github.com/OwinoLucas/I-Reporter.git
```

##### Navigate into the folder and install requirements

```bash
cd IReporter pip install -r requirements.txt
```

##### Install and activate Virtual

```bash
- python3 -m virtualenv venv - source venv/bin/activate
```

##### Install Dependencies

```bash
pip install -r requirements.txt
```

##### Setup Database

SetUp your database User,Password, Host then make migrate

```bash
python manage.py makemigrations 
```

Now Migrate

```bash
python manage.py migrate
```

##### Run the application

```bash
python manage.py runserver
```

##### Testing the application

```bash
python manage.py test
```

Open the application on your browser `127.0.0.1:8000`.
## Tech Stack
* Python 3.6
* Django 3.0.7
* Django Rest Framework 3.11.0
* psycopg2 2.8.5
* django-cors-headers 3.4.0
## License
Copyright (c) [2020] [Lucas Otieno,Manasseh Bundi,Patricia Kuria,Moses Babu,Victor Mongare & Daniel]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.