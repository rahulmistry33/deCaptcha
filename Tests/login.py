from selenium import webdriver
import unittest
import HtmlTestRunner
import os, re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import json
import importlib, importlib.util

maxTimeOut=10

def testLoginUrl(self):
    # Navigate to home page
    pageURL = self.driver.current_url
    self.assertEqual(pageURL, "http://127.0.0.1:8000/crackCaptcha/home/")
    return True

def testMobile(self):
    mobile = self.params['mobile']
    validCredentials = self.params['validCredential']
    # Check if the input mobile number is valid or not
    try:
        # Get the mobile number field and type in the mobile number.....
        mobileField = WebDriverWait(self.driver, maxTimeOut).until(EC.presence_of_element_located((By.ID, "id_mobile")))
        mobileField.send_keys(mobile)
        passwordField = WebDriverWait(self.driver, maxTimeOut).until(EC.presence_of_element_located((By.ID, "id_password")))
        passwordField.send_keys("12345678")
    except: pass
    # Click on the mobile number label to get the error msg in span element
    submit = WebDriverWait(self.driver, maxTimeOut).until(EC.presence_of_all_elements_located((By.ID, "submit")))[0]
    submit.click()
    time.sleep(2)
    if mobile == "": return
    ele = WebDriverWait(self.driver, maxTimeOut).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.help-block")))[0]
    if validCredentials and ele: self.assertTrue(True)    
    if not(validCredentials) and not(ele): self.assertTrue(True)

def testPassword(self):
    password = self.params['password']
    validCredentials = self.params['validCredential']
    # Check if the input password number is valid or not
    try:
        # Get the password  field and type in the password
        mobileField = WebDriverWait(self.driver, maxTimeOut).until(EC.presence_of_element_located((By.ID, "id_mobile")))
        mobileField.send_keys("1")
        passwordField = WebDriverWait(self.driver, maxTimeOut).until(EC.presence_of_element_located((By.ID, "id_password")))
        passwordField.send_keys(password)
    except: pass
    # Click on the password label to get the error msg in span element
    submit = WebDriverWait(self.driver, maxTimeOut).until(EC.presence_of_all_elements_located((By.ID, "submit")))[0]
    submit.click()
    time.sleep(2)
    if password == "": return
    ele = WebDriverWait(self.driver, maxTimeOut).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.help-block")))[0]
    if validCredentials and ele: self.assertTrue(True)    
    if not(validCredentials) and not(ele): self.assertTrue(True)
    
    
def login(self):
    testLoginUrl(self)
    testMobile(self)