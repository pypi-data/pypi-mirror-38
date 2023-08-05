import json
import hashlib
import pandas as pd
import numpy as np
from collections import OrderedDict
from urllib import request
import urllib.parse as urlparse
from urllib.parse import urlencode
from socket import timeout
import os


# The core functionality
class NomiswebApi:

  # static variables
  url = "https://www.nomisweb.co.uk/"
  key = os.environ.get("NOMIS_API_KEY")

  # timeout for http requests
  Timeout = 30

  # Define Nomisweb geographic area codes
  LAD = 293 # check this is consistent
  MSOA = 297
  LSOA = 298
  OA = 299

  # Country-level area codes
  England = 2092957699
  EnglandWales = 2092957703
  GB = 2092957698
  UK = 2092957697

  # initialise, supplying a location to cache downloads, and a LA mappings
  def __init__(self, cacheDir, mappingFile):
    self.cacheDir = cacheDir
    self.mappingFile = mappingFile
    if NomiswebApi.key is None:
      print("Warning - no API key found, downloads may be truncated.\n"
            "Set the key value in the environment variable NOMIS_API_KEY.\n"
            "Register at www.nomisweb.co.uk to obtain a key")

  def geoCodes(self, laCodes, type):
    geoCodes = []
    for i in range(0,len(laCodes)):
      path = "api/v01/dataset/NM_144_1/geography/"+str(laCodes[i])+"TYPE" + str(type) + ".def.sdmx.json?"

      rawdata = self.__fetchJSON(path, { })

      nResults = len(rawdata["structure"]["codelists"]["codelist"][0]["code"])
      # seems a bit daft not to take advantage of the fact we know the length
      for j in range(0,nResults):
        geoCodes.append(rawdata["structure"]["codelists"]["codelist"][0]["code"][j]["value"])
    return self.__shorten(geoCodes)

  def readLADCodes(self, laNames):
    # if single valued arg, convert to a list
    if type(laNames) is not list:
      laNames = [ laNames ]
    geoCodes = pd.read_csv(self.mappingFile, delimiter=',')
    codes = []
    for i in range(0,len(laNames)):
      codes.append(geoCodes[geoCodes["name"] == laNames[i]]["nomiscode"].tolist()[0])
    return codes

  def getUrl(self, table, queryParams):

    # python dicts have nondeterministic order (see https://stackoverflow.com/questions/14956313/why-is-dictionary-ordering-non-deterministic)
    # this is problematic for the cacheing, so we insert alphabetically into an OrderedDict (which preserves insertion order)
    ordered = OrderedDict()
    for key in sorted(queryParams):
      ordered[key] = queryParams[key]

    return NomiswebApi.url + "api/v01/dataset/" + table + ".data.tsv?" + str(urlencode(ordered))

  def getData(self, table, queryParams):
    queryParams["uid"] = NomiswebApi.key
    queryString = self.getUrl(table, queryParams)

    filename = self.cacheDir + hashlib.md5(queryString.encode()).hexdigest()+".tsv"

    # retrieve if not in cache
    if not os.path.isfile(self.cacheDir + filename):
      print("Downloading and cacheing data: " + filename)
      request.urlretrieve(queryString, filename) #, timeout = NomiswebApi.Timeout)

      # check for empty file, if so delete it and report error
      if os.stat(filename).st_size == 0:
        os.remove(filename)
        print("ERROR: Query returned no data. Check table and query parameters")
        return
    else:
      print("Using cached data: " + filename)


    # now load from cache and return
    return pd.read_csv(filename, delimiter='\t')

  def getMetadata(self, tableName):
    path = "api/v01/dataset/def.sdmx.json?"
    queryParams = { "search": "*"+tableName+"*" }

    data = self.__fetchJSON(path, queryParams)

    #print(data)
    # this is the nomis internal table name
    table = data["structure"]["keyfamilies"]["keyfamily"][0]["id"]

    rawfields = data["structure"]["keyfamilies"]["keyfamily"][0]["components"]["dimension"]
    fields = { }
    for rawfield in rawfields:
      field = rawfield["conceptref"]
      fields[field] = {}
      # further query to get categories
      path = "api/v01/dataset/"+table+"/"+field+".def.sdmx.json?"
      #print(path)

      try:
        fdata = self.__fetchJSON(path, {})
      except timeout:
        print("HTTP timeout requesting metadata for " + tableName)
        return {}
      except: # (HTTPError, URLError) as error:
        print("HTTP error requesting metadata for " + tableName)
        return {}
      else:
        values = fdata["structure"]["codelists"]["codelist"][0]["code"]
        #print(field+":")
        for value in values:
          #print("  " + str(value["value"]) + " (" + value["description"]["value"] + ")")
          fields[field][value["value"]] = value["description"]["value"]

    result={"nomis_table": table,
            "description": data["structure"]["keyfamilies"]["keyfamily"][0]["name"]["value"],
            "fields": fields }
    return result

# private

  # given a list of integer codes, generates a string using the nomisweb shortened form
  # (consecutive numbers represented by a range, non-consecutive are comma separated
  def __shorten(self, codeList):
    codeList.sort() # assume this is a modifying operation
    shortString = ""
    i0 = 0
    for i1 in range(1,len(codeList)):
      if codeList[i1] != (codeList[i1-1] + 1):
        if i0 == i1:
          shortString += str(codeList[i0]) + ","
        else:
          shortString += str(codeList[i0]) + "..." + str(codeList[i1-1]) + ","
        i0 = i1
    if (i0 == i1):
      shortString += str(codeList[i0])
    else:
      shortString += str(codeList[i0]) + "..." + str(codeList[i1])
    return shortString

  def __fetchJSON(self, path, queryParams):
    # add API key to params
    queryParams["uid"] = NomiswebApi.key

    queryString = NomiswebApi.url + path + str(urlencode(queryParams))

    response = request.urlopen(queryString, timeout = NomiswebApi.Timeout)
    return json.loads(response.read().decode("utf-8"))


