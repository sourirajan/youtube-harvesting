## Youtube data harvest

Youtube data harvest is a python based applications that facilitates user to review youtube channel and load into database for further analysis. 

## Features

- View channel details including playlists, videos and comments
- Load channel into PostgreSQL for further analysis
- Pre-defined analysis options
- Search and view youtube videos

## Tech
- Built on python, streamlit and postgresql database. 
- Uses youtube data library to fetch data from youtube

## Modules

The application uses the following python modules

| Module | Purpose |
| ------ | ------ |
| streamlit | Build interactive web application |
| pandas | Handling transformation of data |
| time | Handle ISO 8601 duration format |
| os | Access environment variables |
| plotly | Build visualizations |
| streamlit_player | Video player to display youtube videos |
| psycopg2 | Postgres driver to connect to database |
| requests | Client to perform HTTP request |

## Environment Variables

The application requires the following enviornment variables to be set

| Module | Purpose |
| ------ | ------ |
| api_key | Youtube data API key |
| pg_host | Postgresql Host name |
| pg_port | Postgresql Port number |
| pg_dbname | Postgresql Database that contains application tables |
| pg_user | Username to connect to database |
| pg_password | User password |

## Installation

From the application directory, install the following dependencies.

```sh
pip install pandas
pip install streamlit
pip install streamlit_player
pip install requests
pip install psycopg2
node app
```

After setting the environment variables and installing dependencies, run the application using the following command:

```sh
python -m streamlit run home.py
```
