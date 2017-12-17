# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 10:45:23 2017

@ author (C) Cristina Gallego, University of Toronto
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# configure engines
biomatrixengine = create_engine("postgresql+psycopg2://biomatrix_ruser_mri_cad:bi0matrix4mricadSTUDY@142.76.29.187/biomatrixdb_raccess_mri_cad")
localengine = create_engine('sqlite:///myfirstlocaldatabase.db', echo=False)

# later, we create the engine
Base = declarative_base(biomatrixengine)
