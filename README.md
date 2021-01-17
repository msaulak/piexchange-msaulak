# emailtest

docker build -t piexchange-image .
docker run --rm --name piexchange-container -ti piexchange-image /bin/bash

python3 send_email.py data/email_template.json data/customers.csv output_emails error_files/errors.csv send --smtp