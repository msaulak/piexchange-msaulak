# Pi Exchange Coding challenge

### Author - Manveer Singh

#### Language, build environments and dependencies

This solution has been coded in Python3.8 using PyCharm IDE on Windows.
The repo has a Dockerfile which has been tested against the code.

#### Docker instructions

There is a Dockerfile in the repository which can be used to create a docker container for this application.
To create an image & container from the Dockerfile, navigate to the parent directory of this repository and run 

    $ docker build -t piexchange-image .

This will create a docker image from the Dockerfile. This may take a while.

    $ docker image ls piexchange-image

This should list the docker image just created.

    REPOSITORY         TAG       IMAGE ID       CREATED         SIZE
    piexchange-image   latest    1cf7ac935fe2   4 minutes ago   639MB

To create & start the docker container using this image, run the following.The following will also get you a bash
shell, as a root user, for the docker container. When you exit, the container it deleted. 
To avoid having containers with same name, a container name is not given below.

    $ docker run --rm -ti piexchange-image /bin/bash

If you with to change the entrypoint to python, please feel free.

## Run tests

There are 17 test cases (16 active + 1 skipped) in total. To run the tests, you can run the following from the shell of 
the above docker container.

        $ python3 -m unittest discover -s tests -t tests    

## How to run

To run the code, you can run the following from the shell of the above docker container. There are sample files placed
in the `data` directory.

    $ python3 send_email.py data/email_template.json data/customers.csv output_emails error_files/errors.csv

If you wish to pass a different email template JSON file and/or customer data CSV file, please add them to the `data`
directory under the parent directory and re-build the docker image.

To see USAGE on the application, please run

    $ python3 send_email.py --help

## Unimplemented APIs to send emails via SMTP or REST API

To activate the code path which can be implemented to send the emails via SMTP, run

    $ python3 send_email.py data/email_template.json data/customers.csv output_emails error_files/errors.csv send --smtp

To activate the code path which can be implemented to send the emails via REST API, run

    $ python3 send_email.py data/email_template.json data/customers.csv output_emails error_files/errors.csv send --rest

## Project Design:

`__init__.py` under each package has a description.

## Application Design:

All modules, class and methods have extensive docstrings with them. Please refer to them for details on their
implementation and usage.

1. `class OutgoingEmailManager` in `outgoing_email_manager.py` is the main processing class. It uses the 
   Composite Design pattern; such that it contains instances of a customer data extractor, email template, paths to
   required locations, and the API which will be used to send out emails.
   
2. `class BaseCustomerDataExtractor` handles most of the data processing for customer data. It does not implement the
   method which loads the customer data. This is done so that we can implement a [cheap] factory method to load customer
   data from different sources. For this exercise, `class CsvCustomerDataExtractor` extends 
   `class BaseCustomerDataExtractor` to load customer data from a CSV file into a pandas Dataframe
   
3. `class CustomerData` and `class EmailTemplate` simply holder customer data and email template record(s) respectively.

4. `class OutgoingEmailApi` is an abstract class, whose implementations `class RESTOutgoingEmailApi` and 
   `class SMTPOutgoingEmailApi` can be implemented later to send out emails. We can also implement a Factory Design
   here for clean code.
   
5. `send_email.py` is the entry point to the code.

6. `utils` package houses all utility features.