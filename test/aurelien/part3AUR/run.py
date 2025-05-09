#!/usr/bin/env python3

from app import create_app
'''
config mode :
development
testing
online
default
'''
config_name = 'default'

app = create_app(config_name=config_name)

if __name__ == "__main__":
    app.run(debug=config_name== 'default')
