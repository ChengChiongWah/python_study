#!/usr/bin/env python3
# coding:utf-8
from flask import Blueprint

recipe = Blueprint('recipe', __name__, static_folder='../static')

from . import views
