import hashlib

class HashChecker:
    """Made By Peter Gibbs
    CSCI 4800/5800 Princibles of Cyber Security
    University of Colorado Denver

    
    This class allows the validation of files for use in intrusion detection systems
    The object created by this class can take in any file, hash it, and see if the files hash exisists in a prefefiened "valid files" list
    The list of valid files is contained within a NEWLINE delimited plain text document whose filepath is specified as a paramater that is
    fed into the objects constructor

    Varibles:
       validationList, This is a dictionary object that is created and filled apon creation of a HashChecker object
       The HashChecker object will read the hashes stored in the file provided apon construction and put them into the validation list
       when the validate() function validates a file it matches its hash to the one stored in the file
    
   
    HOW TO USE
    create a hashChecker with SomeChecker=HashChecker("SomeFile.txt")
    You can get the hash of a file as a string by using SomeChecker.getHash("SomeOtherFile.txt")
    You can check to see if a file is valid with SomeChecker.Validate("SomeOtherFile.txt") 
    """

    
    
    def __init__(self, _filepath=None):
    
        """This is the constructor It takes a single filepath encoded as a string as an arguement. The file path should point to a NEWLINE dilimited text file that containes the md5 hash values for various files. WILL RAISE EXCEPTION IF NO FILEPATH IS PROVIDED"""
        self.validationList={}

        
        #if the file is not specified then we throw an exception
        if not _filepath:
            raise Exception('No Validation Path specified in construction of hashChecker')
        file=open(_filepath)
        filedata=file.read().splitlines()
        file.close()
        for line in filedata:
            self.validationList[line]=True



        
    def getHash(self,filepath=None):
        """This loads a file from a path then returns its hash as a string. WILL RAISE EXCEPTION IF NO FILEPATH IS PROVIDED"""
        hasher=hashlib.md5()
        if not filepath:
            raise Exception('No input file for hashing specfied')
        
        with open(filepath,'rb') as infile:
            buf=infile.read()
            hasher.update(buf)
        
        return hasher.hexdigest()
        

    def validate(self,filepath=None):
        """This loads a file from a path, hashes it, then checks if the hash exists in the validation list."""
        if self.getHash(filepath) in self.validationList:
            return True
        else:
            return False




        
        
            
