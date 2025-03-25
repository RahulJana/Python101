Setting up Prithvi Environment
=============================

Clone the Chiron repo. ``ssh`` is recommended to make a clone of the repository.
You can learn about how to connect with ssh `here <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh>`_.
If you are using WSL, make sure to clone the chiron repository in ``\\wsl.localhost\Ubuntu-22.04\home\<username>``

.. code-block:: bash

    git clone git@github.com:deepforestsci/chiron.git

When you write your code, create a branch from the deepforestsci repository and make your code changes to it.

We use mamba to manage conda environments. Some of the packages that we use are exclusively supported through Mamba.
It is recommended to install nothing but mamba in the ``base`` conda environment.

Install mamba to your ``base`` conda environment. This can be done using Miniforge(recommended) or using the following command.

.. code-block:: bash

    conda install -n base --override-channels -c conda-forge mamba 'python_abi=*=*cp*'

If the above command does not work, install mamba using Miniforge. If using a Mac/Linux system, the command is 

.. code-block:: bash

      curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" 
      bash Miniforge3-$(uname)-$(uname -m).sh

On a Windows system, you can download and execute the Windows installer from https://github.com/conda-forge/miniforge. For any errors during the installation, refer to the official Mamba documentation https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html

Create a new environment for Prithvi using ``backend/environments/core_enviroment.yml``.

.. code-block:: bash

    cd backend/environments
    mamba env create -f ./core_environment.yml


Activate the newly created environement.

.. code-block:: bash

    mamba activate chiron-env


Install dev dependencies.

.. code-block:: bash

    cd backend/requirements
    pip install -r dev_requirements.txt

Install Prithvi developmental version for backend development in the newly created environment.

.. code-block:: bash

    cd backend
    pip install -e .

**Note:** As on 12th July 2023, some of the packages needed for Chiron/Deepchem to work are only available via the conda-forge channel.
As such, a regular ``pip install`` will not work. It is neccessary to create the environment using mamba/conda.

There are two files, one for creating the core environment and the other for installing dev dependencies.

#. The ``core_enviroment.yml`` file present in ``backend/environemnts`` is a conda environement file and contains the core dependencies for Chiron to work. This includes the dependencies for Deepchem, RDKit, and other core packages.
#. The ``dev_requirements.txt`` file present in ``backend/requirements`` is a pip requirements file and contains the dev dependencies. This includes the dependencies for testing, linting, documentation etc.

(The ``core_requirements.txt``  present in ``backend/requirements`` is deprecated and should **NOT** be used.)

Environment File
----------------
The Prithvi server depends on an environment file `.env` that should be created in `app/` directory. Add the following to the environment file

.. code-block:: bash

   AUTH_SECRET_KEY="5bcd7ed21abf59663188dac0763f3ee69cfa17ab9188283cf8cead28d6f69438"
   AUTH_ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES="120"

Setup mysql database
--------------------

Before starting, you need to install mysql server.

.. code-block:: bash

    sudo apt-get install mysql-server

For details, refer `mysql docs <https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install-linux-quick.html>`_

Configure mysql server by creating `chiron` database and an user. Example:

.. code-block:: bash

    $ mysql
    mysql> CREATE DATABASE chiron;
    mysql> CREATE USER '<username>'@'localhost' identified by 'secret';
    mysql> GRANT ALL ON chiron.* TO '<username>'@'localhost';
    mysql> flush privileges;
    mysql> exit;

Setup AWS credentials
---------------------

This step is optional. Setup of AWS credentials is necessary only to be able to submit jobs on local chiron. You can skip this step during initial setup.

To be able to submit jobs on a local Prithvi instance, you will need to set up AWS credentials on your local machine, otherwise, you will run into the following error when uploading files/submitting jobs:

.. code-block:: bash

    botocore.exceptions.NoCredentialsError: Unable to locate credentials

The AWS credentials are generated manually, on request. Once your credentials have been generated, install ``aws-cli`` on your system. 
Then, follow these steps to set up AWS locally:

* Run ``aws configure``
* Enter the `Access key ID`
* Enter the `Secret access key`
* Enter ``us-east-2`` for the `default region name`
* Leave the `default ouptut format` option empty

Create a new folder ``.aws`` and add a ``config`` file in it. Add the credentials used in ``aws-configure`` to this file.

Upon successful configuration, you should be able to upload files and submit jobs through the local Prithvi instance. 

Please note, for AWS CLI installation, refer `aws docs <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>`_ 

Running Prithvi Server for Development
-------------------------------------

Update `MYSQL_USER` field in `scripts/start_server.sh` to the username which you created in the previous step and make sure the `AWS_REGION` is set to `us-east-2` in `scripts/start_server.sh`.
Make sure you have the config and credentials file in the `.aws` folder. Check if the `region` is set to `us-east-2` in `.aws/config` file.
Start Prithvi Server in local conda chiron environment for development as

.. code-block:: bash

    cd ~/chiron
    pip install -r app/requirements.txt
    ./scripts/start_server.sh

Running Prithvi Frontend 
------------------------

To run the Prithvi Frontend on localhost, run the following commands

.. code-block:: bash

      cd frontend
      yarn install 
      yarn dev:chiron 

This should run Prithvi on localhost:4200. Once you have it running, create a new user with a username and password. 
Please ensure that the username and password you are using here are different from the ones you are using on the actual Prithvi website.
The beta password is ``beta``. Make sure backend is running while creating the user. 


Common errors during setup and workarounds
------------------------------------------

1. While runnning backend, if you encounter errors that say 'Unable to add column' or 'Unable to drop column', comment out the line where the error occurs in the ``app/migrations`` folder.
Drop the Chiron database and create it again. Run backend again now.
For Example, 
Error: Cannot drop column ``is_admin`` in ``profileuserlink`` 
Workaround: Comment out line 24 of ``app/migrations/versions/30edbcc5478b_shift_balance_and_is_admin.py``
 
2. If you face any 'Module not found' errors while trying to run the script, install the modules using pip.

.. code-block:: bash

      pip install <module>

3. Dependecy error: deepchem requires scipy<1.9 but jax requires >=1.9. Run the following command

.. code-block:: bash

      pip install --pre deepchem

4. In case you face issues with installation on Windows, it is recommended to use WSL. 
5. ``dgl`` does not exist. Install using pip

.. code-block:: bash

      pip install dgl
      
6. ``pyg`` not found. Install using pip

.. code-block:: bash

      pip install torch_geometric

WSL Errors
----------

If you are using WSL and come across any ``Can't connect to MYSQL server`` errors run,

.. code-block:: bash

    conda deactivate
    sudo service mysql start

If MYSQL server is unable to start, run

.. code-block:: bash

    conda deactivate
    sudo service mysql restart

Once mysql is running, activate chiron conda environment and run

.. code-block:: bash

    cd ~/chiron
    scripts/start_server.sh 


Running Prithvi Server for Production
------------------------------------

.. code-block:: bash

    cd ~/chiron/scripts
    docker compose up

Notes
^^^^^
1. The environment variable RETRO_DOWNLOAD has to be set to True inside
start_server.sh to download the default retrosynthesis models and stock.

Interacting with the Prithvi Server through Pyprithvi (earlier: Pychiron)
-------------------------------------------------------------------------

You can use the `pyprithvi` user library to send commands to the running Prithvi server. Install pyprithvi by running

.. code-block:: bash

    cd ~/chiron/pyprithvi
    pip install -e .

You can then import pyprithvi from within the python REPL. You can use pyprithvi to  test whether your Prithvi server is running by sending a request::

    >>> import pyprithvi
    >>> pyprithvi.set_backend_url("http://localhost:8000/")
    >>> pyprithvi.healthcheck()
    True  # setup successful


Building Prithvi Docs
--------------------

Prerequisite: install `pandoc <https://pandoc.org/installing.html>`_. `pandoc` is required for 

.. code-block:: bash

    # building user doc
    cd chiron/docs/user
    pip install -r requirements.txt
    make html

    # building internal doc
    cd chiron/docs/internal
    pip install -r requirements.txt
    make html

