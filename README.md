# Energy Clustering
Tornado web services and scikit-learn algorithms for energy data clustering.

## Quick start

Clone the repository and access the energyclustering folder.

```git clone https://github.com/matheper/energyclustering.git```

```cd energyclustering```

You must to have installed Python 3 to run energyclustering.

You also need PostgreSQL and Redis.

If you have `docker` and `docker-compose` installed,
this prerequisites can be installed with `docker-compose up`.

Whether you use your own database, you need to properly configure the `settings.py`.

Create a virtualenv:

```python3 -m venv env```

Activate the virtual environment:

```source env/bin/activate```

Install the Python prerequisites using pip:

```pip install -r requirements.txt```


Running the tests:

```python -m unittest discover```

Running the application:

```python app.py```


## How the application works

The app receives `POST`s with plain text file in `/signal`.

The signal is parsed to a cleaner, standardised format, and saved to  PostgreSQL.

When the signal count reaches 1000, the whole set of events is sent in the format required by the scikit-learn library for its clustering algorithms.

Available reports:

`/report` - All signals parsed and labeled.

`/report/id` - One signal parsed and labeled.

`/average` - The active power average for the events assigned to each cluster

`/distribution` - The number of events associated to each cluster
