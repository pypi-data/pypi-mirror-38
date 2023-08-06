# ioexplorer-dataloader

_This repository contains the code for a command line tool to manage and ingest datasets into a Postgres database, for later use by the IOExplorer web application._

## Pre-Requisites
This CLI has three main depencies: `docker` and `node`, and `python` (specifically Python 3).

Installation instructions for each can be found below:
- `docker`: https://docs.docker.com/install/
- `node`: https://nodejs.org/en/
- `python`: https://www.python.org/downloads/

Once `node` is installed, you will also need to globally install some packages which are used to interact with the database.
```
npm i -g sequelize sequelize-cli pg
```

With some environments, you will get a permission error when you attempt to install these packages. There is a [good article](https://docs.npmjs.com/getting-started/fixing-npm-permissions) on how to fix your environment to avoid these errors.

To do a final check to make sure all software is installed, run the following:
```
docker --version
node --version
npm --version
sequelize --version
python --version
```
Note that `python --version` should return something starting with `3`.
## Installing the CLI
 Installing the CLI:
 simply,
 ```
 pip install ioexplorer-dataloader
 iodl --help
 ```
 ## Example Workflows
 ### 1. Basics
 _A workflow to help you get familiar with the basics of the dataloader._

##### Creating a database.

```
$ mkdir configs

$ iodl database create --database-config configs
? Name the database  my-database
? Choose a host.  127.0.0.1
? Choose a port.  5432
? Choose a username for the root account.  root
? Choose a password for the root account.  password
SUCCESS: Created the database configuration for my-database
```
Here, we just:
1. Made a folder called `configs` to store our database config file.
2. Created a database config file at `configs/my-database.config.json`.

You can check that everything looks alright by running:
```
cat configs/my-database.config.json
```

##### Starting a database.

Note that the database is not live yet, we just created the config file for the database. Start the database by running
```
$ iodl database start my-database --database-config configs
```

The database should now be started. The database just a docker container running the [postgres](https://hub.docker.com/_/postgres/) image, so you can see it being run with `docker ps`.

##### Opening a `psql` shell into a database.
Now lets open a `psql` shell connected to our newly created database:
```
$ iodl database shell my-data --database-config configs
psql (11.0 (Debian 11.0-1.pgdg90+2))
Type "help" for help.

my-database=# \dt
Did not find any relations.
```

The message `Did not find any relations.` lets us know that this database is completely empty and schemaless.

##### Applying migrations to our database.
The `iodl` CLI has a copy of all migrations used to produce the current production version of the IOExplorer database schema. To apply all these migrations run:
```
$ iodl database migrate my-database --database-config configs
```

Now if you open another `psql` shell and list the relations, you get the expected:
```
$ iodl database shell my-database --database-config .
psql (11.0 (Debian 11.0-1.pgdg90+2))
Type "help" for help.

my-database=# \dt
           List of relations
 Schema |     Name      | Type  | Owner
--------+---------------+-------+-------
 public | SequelizeMeta | table | root
 public | cnas          | table | root
 public | datasets      | table | root
 public | fusions       | table | root
 public | mutations     | table | root
 public | samples       | table | root
 public | subjects      | table | root
 public | svs           | table | root
 public | timelines     | table | root
(9 rows)
```

Now our database is ready to get some data.

##### Environment Variables Interlude
You may have noticed that we set the `--database-config configs` option in each call, and we often need to set the database name (e.g. `my-database`) argument.

It would get annoying to do this every time. To set these values as environment variables, you can just run the following:
```
export IOEXPLORER_DATABASE_CONFIG=`realpath configs`
export IOEXPLORER_DATABASE_NAME=my-database
```

Now, you may omit database config / name arguments / options from all commands, e.g.,:
```
iodl database create
iodl database start
iodl database migrate
...
```
For the rest of this section, we will assume those variables are set and will omit arguments / options from our commands.

##### Initializing a dataset


`cd` into a dataset to upload. Ask Ryan for one if you do not have any.
**TODO**: upload example dataset.

The dataset should have the following directory structure:
```
.
├── data_clinical_patient.txt   (R)
├── data_clinical_sample.txt    (R)
├── data_CNA.txt
├── data_fusions.txt
├── data_gene_matrix.txt
├── data_mutations_extended.txt
├── data_SV.txt
└── data_timeline.txt
```
Note: _Only the files denoted with an (R) are actually required_.

We now want to _initialize_ the dataset. This step will
1. Run some quick validations to make sure the data structure is correct.
2. Collect some meta-information from the user.
3. Write a `config.yaml` file which stores information about this dataset and helps with ingestion.

Run:
```
(dataloader) ryan@galliumos:~/MSK/data/Hugo$ iodl dataset init
INFO: Initializing new dataset!

...
 Some success messages will appear here, or a prompt will ask you if you would like to continue with missing data.
...

? What is the dataset name?  my-dataset
? What is a description of the dataset?  this is a test dataset...
? Enter link to paper.  http://google.com
? Who are you (person uploading data)?  Ryan
SUCCESS: Thanks! I made a file called `config.yaml` in this directory! Check it out and make sure everything looks OK!
```

##### Ingesting a dataset
With the `config.yaml` file already formed, ingesting the database is very simple.
```
$ iodl dataset ingest
```

If there are any problems during ingestion, an error will be thrown and the data that already made it into the database (before the error) will be deleted. This will let you diagnose any problems with the data ingestion and re-attempt ingestion without messing with the state of the database.
