This project takes the trained model (which should know how regular data look like - see `traning`), based on it, it finds the anomalies and tries to find a cluster amongst them. Report is sent to desired endpoint.

- finding anomalies is `supervised` - traning needs to be run first to tell the model how do anomalies look
- finding clusters is `unsupervised` - based on anomalies (trained model), script can automatically find clusters

# How to run with python pip
required python>=3.9

```sh
source venv/bin/activate
```

```sh
pip install -r requirements.txt
```

```sh
PYTHONPATH=$PYTHONPATH:./src python3 bin/main.py
```

## evaluating with default config.toml
```sh
PYTHONPATH=$PYTHONPATH:./src python3 bin/main.py
```

## evaluating with user defined config
```sh
PYTHONPATH=$PYTHONPATH:./src python3 bin/main.py myconfig.toml
```

## tests

```sh
PYTHONPATH=$PYTHONPATH:./src python3 test/runtests.py
```

# How to run with docker


```
docker build --network=host --tag aiscript .
```

```
docker run --network=host aiscript
```

## user defined config toml file
default config toml file is `./config.toml` (specified in Dockerfile)

to change the config.toml path, change in Dockerfile `CMD` argument

```Dockerfile
CMD ["python3", "-u", "bin/main.py", "./config.toml"]
```


# config.toml
input of the script is defined in `config.toml` file

this file can be changed anytime by specifing different toml file in `Dockerfile`

