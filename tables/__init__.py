# -*- coding: utf-8 -*-
"""
@Time ： 2020/7/5 10:03
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

engine = create_engine("sqlite:///" + PATH("airtest.db"), echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)