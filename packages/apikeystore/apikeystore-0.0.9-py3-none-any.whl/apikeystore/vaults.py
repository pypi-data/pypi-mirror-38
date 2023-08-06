#!/usr/bin/env python
import sqlite3
import uuid
import time
import datetime
import os
import hashlib
import string
import re

class Vault(object):
    def __init__(self, name, path=None):
        '''Initialize vault'''
        if path == None:
            self.path = os.getcwd()
        else:
            self.path = path    
        
        #Verify Directory
        if os.path.isdir(self.path) == False:
            raise Exception("The directory provided does not exist : \n\t {}".format(path))
        
        #Store full path to vault
        self.filepath = os.path.join(self.path,name)

    def new(self,dbname=None):
        '''Creates new vault for storing credentials '''
        ##Desc - This table contains the Name of the database, when it was created and when it was last modified. 
        #   (name, created, lastModified, totalCreds) 
        sql_create_desc_table = """ CREATE TABLE IF NOT EXISTS desc(
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        created text,
                                        lastModified text
                                    );"""
        ##Creds - This table contains the application credentials.
        #   (cid, appName, created, lastModified, authType, UrlBase, apiId, appKey, userId, userPub, userPriv, token)
        sql_create_creds_table = """ CREATE TABLE IF NOT EXISTS creds(
                                        id INTEGER PRIMARY KEY,
                                        appname text NOT NULL,
                                        created text NOT NULL,
                                        lastModified text, 
                                        authType text NOT NULL,
                                        urlBase text NOT NULL,
                                        appId text,
                                        appKey text,
                                        appSec text, 
                                        userId text, 
                                        userPub text, 
                                        userPriv text, 
                                        accessToken text,
                                        unique (appname)
                                        
                                    );"""                             
        #Create sqlite3 database with the above tables and views:
        if dbname !=  None: 
            conn = sqlite3.connect(dbname)
        else: 
            conn = sqlite3.connect(self.filepath)
        
        if conn is not None:
            c = conn.cursor()
            c.execute(sql_create_desc_table)
            c.execute(sql_create_creds_table)

        # Add date created to desc table
        #SELECT count(*) FROM creds as totalCreds;
        #sql_insert_desc_row = """ INSERT INTO desc(
        #                                id,
        #                                name,
        #                                created,
        #                                lastModified
        #                                );""" 

    def open(self,keypath=None):
        '''Decrypt vault (Future Feature)'''
        # Validate selected database matches expected schema. 
        vault_isValid = self.validate()

        #assert value must be valid
        assert (vault_isValid == True), "This vault is not valid!!"
             
    def close(self):
        '''Close vault database (Future Feature)'''          
        
    def deleteVault(self):
        '''Removes vault'''
        #Prompt user to confirm they want to delete the vault. 
        # Provide Vault Name Path and details 
        # Details to include number of Credentials stored in vault
        # Last Modifed Date

    def validate(self):
        '''Validates vault schema'''
        #Get List of all tables and views
        #sort list
        #contatinate table/vien names in to a list with results of pragma info_table
        #Convert list into a string and calculate sha265 hash
        #assign resulting hash to validationCode        
        conn = sqlite3.connect(self.filepath)
        if conn is not None:
            c = conn.cursor()
            tables = c.execute("""SELECT name 
                            FROM sqlite_master 
                            WHERE type='view' 
                            OR type='table' 
                            ORDER BY name;""").fetchall()
            tables.sort()
            TestString = list()
            for t in tables:
                test = """pragma table_info(%s)"""%(t)
                TestString.append(t)
                TestString.extend(c.execute(test).fetchall())

            #Convert to string and get hashed value
            TestString = str(TestString).encode("utf-8")
            TestCode = str((hashlib.sha256(TestString)).hexdigest())
        
        #Buils a Test 
        validatonTest = str(uuid.uuid4()) + ".db"
        self.new(dbname=validatonTest)
        
        conn = sqlite3.connect(validatonTest)
        if conn is not None:
            c = conn.cursor()

        tables = c.execute("""SELECT name 
                        FROM sqlite_master 
                        WHERE type='view' 
                        OR type='table' 
                        ORDER BY name;""").fetchall()
        tables.sort()
        ValString = list()

        for t in tables:
            test = """pragma table_info(%s)"""%(t)
            ValString.append(t)
            ValString.extend(c.execute(test).fetchall())

        #Convert to string and get hashed value
        ValString = str(ValString).encode("utf-8")
        ValidationCode = str((hashlib.sha256(ValString)).hexdigest())
        conn.close()
        #Delete validation DB
        os.remove(validatonTest)

        if ValidationCode == TestCode:
            validationStatus = True
        else:
            validationStatus = False    

        return validationStatus

class Creds(Vault):
    def __init__(self,vaultName,CredName=None, path=None):
        '''Initialize vault'''
        if path == None:
            self.path = os.getcwd()
        else:
            self.path = path    
        
        #Verify Directory
        if os.path.isdir(self.path) == False:
            raise Exception("The directory provided does not exist : \n\t {}".format(path))
        
        #Store full path of vault
        self.filepath = os.path.join(self.path,vaultName)

        #Validate vault matches expected schema
        vaultValid = self.validate()

        if vaultValid == False:
            raise TypeError

    def addCreds(self, appName, urlBase, authType, appId=None, appKey=None, appSec=None, userId=None, userPub=None, userPriv=None, accessToken=None):
        '''Stores application credential information in vault'''
        '''Auth Types [basic, oauth, oauth2, custom]'''
        
        sql_insert_cred = """ INSERT INTO creds(
                                        appname,
                                        created,
                                        lastModified, 
                                        authType,
                                        urlBase,
                                        appId,
                                        appKey,
                                        appSec, 
                                        userId, 
                                        userPub, 
                                        userPriv, 
                                        accessToken
                                        )
                                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
          
        created = str(datetime.datetime.utcnow())
        lastModified = created
        validAuthTypes = ('basic', 'oauth', 'oauth2', 'custom')
        if authType not in validAuthTypes:
            raise ValueError("must be %s" %validAuthTypes)

        #Input Validation
        invalidChars = set(string.punctuation.replace("_","").replace("-","").replace("@","").replace(".",""))

        # urlBase must start with http:// or https://
        if re.match('^(http)(s){0,1}:\/\/', urlBase):
            pass
        else:
            raise ValueError("urlBase argument input must start with http:// or https://")

        stringArgs = (appName, authType, appId, appKey, appSec, userId, userPub, userPriv, accessToken)
        for arg in stringArgs:
            if any(char in  invalidChars for char in str(arg)):
                raise ValueError(arg)
            else:
                details = (appName, created, lastModified, authType, urlBase, appId, appKey, appSec, userId, userPub, userPriv, accessToken)    

        try:
            conn = sqlite3.connect(self.filepath)
            c = conn.cursor()
            c.execute(sql_insert_cred, details)
            conn.commit()
        except sqlite3.IntegrityError:
            raise IOError("appName must be unique.")
        finally:
            conn.close()

    def listCreds(self, vaultName=None ):
        '''lists appNames, url, authentication type, and creation date of all credentials stored in vault'''
        if vaultName == None:
            vaultName = self.filepath

        sql_select_credList = """SELECT appname,
                                        urlBase,
                                        authType,
                                        created
                                 FROM creds;"""    
        conn = sqlite3.connect(vaultName)
        c = conn.cursor()
        credList = c.execute(sql_select_credList).fetchall()
        conn.close()
        return credList        

    def getCred(self, appName, vaultName=None):
        '''Returns named credential from vault as dict '''
        if vaultName == None:
            vaultName = self.filepath


       ## Need to validate appName input

       #### Insert Code Nere ####

        sql_select_app_details = """SELECT appname,
                                        authtype,
                                        urlBase,
                                        appId,
                                        appKey,
                                        appSec,
                                        userId,
                                        userPub,
                                        userPriv,
                                        accessToken 
                                        FROM creds
                                        WHERE appname='%s';""" %appName 
        try:
            conn = sqlite3.connect(vaultName)
            c= conn.cursor()
            result = c.execute(sql_select_app_details).fetchall()
        
        
        finally:
            conn.close()
        
        Cred = {
            'appName'           : result[0][0],
            'authType'          : result[0][1],
            'urlBase'           : result[0][2],
            'appId'             : result[0][3],
            'appKey'            : result[0][4],
            'appSec'            : result[0][5],
            'userId'            : result[0][6],
            'userPub'           : result[0][7],
            'userPriv'          : result[0][8],
            'accessToken'       : result[0][9]
        }
        return Cred


    def updateCred(self, vaultName, appName, UrlBase, appId, appKey,appSec,userId, userKey, authType,accessToken):
        ''' Updates information for credential stored in vault'''
        '''Auth Types [basic, oauth, oauth2, custom]'''

    def deleteCred(self, vaultName, appName):
        '''Removes stored credential from vault'''   
        