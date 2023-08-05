# Example of creating an Excel template using the MarinegeoTemplateBuilder package
from MarinegeoTemplateBuilder import *

import sys
import pandas as pd
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

# some values to prefill for the metadata section
metadataValues = {"TemplateVersion": "v0.0.1",
                  "ProtocolVersion": "v0.0.1",
                  "Title": "Test Template"}

# columns to add
fields_csv = 'sheet,fieldName,fieldDefinition,fieldType,formatString,lookup,unit,minValue,maxValue\n' \
           'Location,site,MarineGEO site abbreviation,list,,,,,\n' \
           'Location,locationID,Unique code for each sampling location,string,,,,\n' \
           'Location,decimalLatitude,"Decimal Latitude hh.hhhhhhh, approximate",decimal,,,degree,-90,90\n' \
           'Location,decimalLongitude,"Decimal Longitude hh.hhhhhhh, approximate",decimal,,,degree,-180,180\n' \
           'Cover,locationID,Foreign key to the locationID defined on the Location sheet,fkey,,Location$locationID,,,\n' \
           'Cover,transectNumber,"Transect Number",integer,,,dimensionless,1,3'

# convert to pandas dataframe
fields = pd.read_csv(StringIO(fields_csv))


# controlled vocabulary
vocab_csv = 'fieldName,code,definition\n' \
            'site,A,siteA\n' \
            'site,B,siteB\n' \
            'site,C,siteC\n'

# convert to pandas dataframe
vocab = pd.read_csv(StringIO(vocab_csv))

# create the example template
main('TestTemplate_v0.0.1.xlsx', fields, vocab, "Test Template", 'DEFAULT', protect=True, metadataValues=metadataValues)
