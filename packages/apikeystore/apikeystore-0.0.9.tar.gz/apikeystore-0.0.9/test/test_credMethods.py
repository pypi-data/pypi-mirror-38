#!/usr/bin/env python
import unittest
from apikeystore import vaults
import os
import sqlite3
import string
import time
import collections
class TestCredMethods(unittest.TestCase):

    def setUp(self):
        self.wellformedDbName = "Test-wellformed.db"
        self.wellformedDb = vaults.Vault(self.wellformedDbName)
        self.wellformedDb.new()

        #set Cred Test config
        self.credConfig = [('appName', "TestApp"),
                            ('authType',"basic"),
                            ('urlBase',"https://testurlbase.com"),
                            ('appId',"123456789abcdefg"),
                            ('appKey',"AnAppkey"),
                            ('appSec',"12345wxyz"),
                            ('userId',"TestUser1@gmail.com"),
                            ('userPub',"TestUserPubKey"),
                            ('userPriv',"TestUserPrivKey"),
                            ('accessToken',"MyTestToken")]
        self.credConfig = collections.OrderedDict(self.credConfig)               
       
    def tearDown(self):
        if os.path.isfile(self.wellformedDbName):
            os.remove(self.wellformedDbName)
        else:
            pass 

    def test_badVaultGiven(self):
        '''Tests that an exception is raised if the provided vault is missing or malformed'''
        with self.assertRaises(Exception):
            self.testVault = vaults.Creds("NotRealVault.db")
        os.remove("NotRealVault.db")    

    def test_goodVaultGiven(self):
        '''Test that no error is returned if a valid vault is given'''
        with self.assertRaises(Exception):
            try:
                vaults.Creds(vaultName=self.wellformedDbName)
            except:
                pass
            else:
                raise Exception        

    def test_addCred(self):
        '''Tests that the credentials were stored in the database'''
        testCred = vaults.Creds(vaultName=self.wellformedDbName)
        testCred.addCreds(**self.credConfig)  
        conn = sqlite3.connect(self.wellformedDbName)
        sql_test_addCred = """SELECT appname,
                                     authType,
                                     urlBase,
                                     appId,
                                     appKey,
                                     appSec,
                                     userId,
                                     userPub,
                                     userPriv,
                                     accessToken
                                     FROM creds
                                     WHERE appname='%s';"""%self.credConfig['appName']
        c = conn.cursor()
        addCredTest = c.execute(sql_test_addCred).fetchall()
        conn.close()
        control = list(self.credConfig.values())

        self.assertEqual(list(addCredTest[0]), control)
        
        

        '''Test each argument received from users contains invalid input.''' 
        with self.assertRaises(Exception):
            testCred = vaults.Creds(vaultName=self.wellformedDbName)
            self.credConfig['appId'] = ");"
            testCred.addCreds(**self.credConfig)
            self.credConfig['appId'] = "123456789abcdefg"
        

        '''Test baseUrl validation. Provided string must start with http:// or https://'''
        with self.assertRaises(Exception):
            testCred = vaults.Creds(vaultName=self.wellformedDbName)
            self.credConfig['urlBase'] = "fake.url.com"
            testCred.addCreds(**self.credConfig)
            self.credConfig['urlBase'] = "https://testurlbase.com"
        
        ''' Test for error if two credentials with same appname are entered. '''
        with self.assertRaises(Exception):
            i = 1
            testCred = vaults.Creds(vaultName=self.wellformedDbName)
            
            while i < 2:
                testCred.addCreds(**self.credConfig)
                


    #def test_listCreds(self):
    #    '''Tests that a list of (appname,authType, and urlBase) is returned by the listCreds function'''
    #    control = [('TestApp', 'https://testurlbase.com','basic')]
    #    #added created date to function need to test this 
    #    testCred = vaults.Creds(vaultName=self.wellformedDbName)
    #    testCred.addCreds(**self.credConfig)
    #    test = testCred.listCreds()
    #    self.assertCountEqual(test, control)


    def test_getCred(self):
        '''Test that appName input is validated prior to using'''


        '''Test that vaultName inpute is validated prior to using'''

        
        '''Tests that the method is able to retreive a named credential'''
        testCred = vaults.Creds(vaultName=self.wellformedDbName)
        testCred.addCreds(**self.credConfig)
        time.sleep(2)
        mycred = testCred.getCred(appName=self.credConfig['appName'])
        self.assertEqual(mycred['urlBase'],self.credConfig['urlBase'] )

#, listCreds, updateCreds, deleteCreds

if __name__ == '__main__':
    unittest.main()        

