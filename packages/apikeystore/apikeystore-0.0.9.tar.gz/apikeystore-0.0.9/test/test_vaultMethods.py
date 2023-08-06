#!/usr/bin/env python
import unittest
from apikeystore import vaults
import os

class TestVaultMethods(unittest.TestCase):
    def setUp(self):
        self.testDb = "Test-187.db"
        self.controlDb = "Control-187.db"
        self.controlVault = vaults.Vault(self.controlDb)
        self.testVault = vaults.Vault(self.testDb) 
    
    def test_NewVault(self):
        '''Test that new Vaults can be created without error.'''
        with self.assertRaises(Exception):
            try:
                self.controlVault.new()
            except:
                pass
            else:
                raise Exception        
    
    def test_MalFormedVault(self):
        '''Tests that vault class rasises an assertion error if the given database does not exist.'''
        with  self.assertRaises(AssertionError):
            self.testVault.open()
        os.remove(self.testDb)

    def test_ValidVault(self):
        '''Tests that a valid vault returns True agains validation''' 
        self.controlVault.new()
        self.assertTrue(self.controlVault.validate()) 
        os.remove(self.controlDb)       

    def tearDown(self):
         pass
        

if __name__ == '__main__':
    unittest.main()