# Global settings for the S3Model Python library
# User editable settings are in S3MPython.conf
import os
import configparser

config = configparser.ConfigParser()
config.read('S3MPython.conf')

VERSION = config['SYSTEM']['version']
RMVERSION = config['SYSTEM']['rmversion']

def getdmlib():
    DM_LIB = config['S3MPython']['dmlib']
    if DM_LIB.lower() == 'default':
        home = os.getenv("HOME")
        DM_LIB = os.path.join(home,'S3MPython', "dmlib")
        if not os.path.exists(DM_LIB):
            os.makedirs(DM_LIB)    
    return(DM_LIB)

DM_LIB = getdmlib()

# set the environment variable for the catalog to be used by lxml
def xmlcatalog():
    home = os.getenv("HOME")
    catdir = os.path.join(home,'S3MPython')
    os.environ["XML_CATALOG_FILES"] = catdir    
    if not os.path.exists(catdir):
        os.makedirs(catdir)
        with open(catdir + os.sep + 'catalog.xml', 'w') as f:
            f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            f.write("<!DOCTYPE catalog PUBLIC '-//OASIS//DTD XML Catalogs V1.1//EN' 'http://www.oasis-open.org/committees/entity/release/1.1/catalog.dtd'>\n")
            f.write("<catalog xmlns='urn:oasis:names:tc:entity:xmlns:xml:catalog'>\n")
            f.write("  <!-- S3Model 3.1.0 RM Schema -->")
            f.write("  <uri name='https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd' uri='s3model_3_1_0.xsd'/>\n")
            f.write("\n")
            f.write("  <!-- S3Model DMs -->")
            f.write("  <rewriteSystem systemIdStartString='https://www.s3model.com/dmlib/' rewritePrefix='" + getdmlib() + "'/>\n")
            f.write("</catalog>\n")
            f.write("\n")
            
    
