# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

setup(name='Pyautomators',
      version='1.6.3',
      url='',
      license='MIT',
      author='Kaue_Bonfim',
      author_email='koliveirab@indracompany.com',
      description='Biblioteca de automação para geracao completa de ambientacao de testes',
      packages=['Pyautomators','Pyautomators.BDD','Pyautomators.Graphic_actions','Pyautomators.BDD.api','Pyautomators.BDD.compat','Pyautomators.BDD.contrib','Pyautomators.BDD.formatter',
      			'Pyautomators.BDD.reporter'],
	install_requires=['webdriver-manager',"pytesseract","pillow",'lackey',"pyyaml","peewee","pyautogui","assertpy","cx_Oracle","selenium","pytractor","numpy","PyMySQL==0.7.8","opencv-python","Appium-Python-Client","behave2cucumber","python-jenkins","behave","django","pandas","pymongo","beautifulsoup4","nltk","TestLink-API-Python-client","sqlalchemy","argparse",'docker'],
      zip_safe=True)
	  



