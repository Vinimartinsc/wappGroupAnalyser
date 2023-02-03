'''
    File: main.py
    Author: Vinícius Martins

    Expose methods, functions and params from internal modules
'''

# Re-exports
from app.DatabaseService.Database import engine 
from app.WappMessageIngestService.WppMessage import *
