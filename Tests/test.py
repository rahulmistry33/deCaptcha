# Importing Libraries
import unittest, os, sys, argparse, re, time, json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from HtmlTestRunner import HTMLTestRunner

# Import modules
from login import *

load_dotenv(os.path.join(os.getcwd(), '.env'))

# Create a Parametrized Test Case Class which inherits unittest module
class ParametrizedTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', params=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.params = params

    # Create Test Suites
    @staticmethod
    def parametrize(testClassName, params=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameters.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testClassName)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testClassName(name, params=params))
        return suite

    # Define Setup Method
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), "chromedriver.exe"))
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:8000/crackCaptcha/home/")

    # Define TearDown Method
    @classmethod
    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        
# create Login Test Suite
class Login(ParametrizedTestCase):
    def testLogin(self):
        login(self)


# Define Login Report Template Arguments
loginTemplateArgs = {
    "test_suite_name": "Login Suite"
}

# Login Suite
loginSuite = unittest.TestSuite()
with open(os.path.join(os.getcwd(), 'testcases.json')) as f:
    data = json.load(f)["login"]
    for case in data:
        loginSuite.addTest(ParametrizedTestCase.parametrize(Login, params=case))
        
#Define Login Runner
loginRunner = HTMLTestRunner(combine_reports=True, 
                             add_timestamp=False,
                             output=os.path.join(os.getcwd(), 'reports'), 
                             report_title="Login Test Report", 
                             report_name="Login Test Report")


loginRunner.run(loginSuite)