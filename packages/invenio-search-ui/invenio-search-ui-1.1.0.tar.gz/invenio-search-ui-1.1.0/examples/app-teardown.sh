#!/bin/sh

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

# clean environment
[ -e "$DIR/static" ] && rm -Rf $DIR/static/
[ -e "$DIR/instance" ] && rm -Rf $DIR/instance/

# Clean the indices
flask index destroy --yes-i-know

# Clean the database
flask db destroy --yes-i-know
