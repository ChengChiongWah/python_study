#!/usr/bin/env python3.5
# coding:utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import Recipe, Material, Step, User, Questions
import os

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run(host='0.0.0.0')
