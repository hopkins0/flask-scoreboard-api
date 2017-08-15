# Scoreboard-API based on [Boca Judge - - 1.59](https://www.ime.usp.br/~cassio/boca/)


A little Scoreboard-API for contest hosted in the Boca Judge.
The project was designed to work with the project [Boca Judge based API](https://github.com/hopkins0/utm-score-board)


## Getting Started

The project was made by using a little API designed by [hopkins0](https://github.com/hopkins0) and using [Flask framework](http://flask.pocoo.org/).

### Prerequisites

```
pip install virtualenv 
```

## Set up and run
### Required packages

```Shell
$ pip install flask
```

### Install packages

```Shell
$ pip install -r requeriments.txt
```

### Run the project
```Shell
$ virtualenv venv
$ source venv/bin/activate
$ ./manager.py runserver
```

To run the project in an enviroment, set up the enviroment variables.
Set FLASK_CONFIG to one of the following values:
* development
* testing
* production

```Shell
$ export FLASK_CONFIG={OPTION}
$ ./manager.py runserver
```

Add the parameter `--host 0.0.0.0` if you want the application be visible outside of the computer.

## Built With
* Flask


## Contributing

Changes and improvements are more than welcome! Feel free to fork and open a pull request.
It will be my pleasure if you can help me to improve this project. 


## Authors

* **Antonio Mendez** - *Initial work* - [hopkins0](https://github.com/hopkins0)

## Social

You can follow me on Twitter, I'm [@xHopkins0](http://twitter.com/xHopkins0).

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details
