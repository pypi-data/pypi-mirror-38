# -*- coding: utf-8 -*-
import hashlib
import os

class UtFileHashFilter:
    def __init__(self):
        self._dic = dict()
        self._exclude = []
        self._defaultGrName = 'default'

    def appendGroup(self, grName, filterString):
        if grName == self._defaultGrName:
            raise Exception('reserved grName')
        self._dic[grName] = filterString

    def appendExclude(self, stringValue):
        self._exclude.append(stringValue)


"""
filter = utfile_hash.UtFileHashFilter()
filter.appendGroup('template', 'template_type')

myFileHash = utfile_hash.UtFileHash(distributor=True,
 dirDist='/Users/chase/Documents/work/utail/py37/svc_scrap/svc_scrap/scrap_scripts',
  groupFilter=filter)
"""
class UtFileHash:
    def __init__(self,
     distributor=False, dirDist=None,
      groupFilter: UtFileHashFilter=None,
      subscriber=False,
      dirSub=None,
     ):
        self._dirDist = None
        self._dirSub = None
        self._dicDefault = dict()
        self._dicUser = None

        if distributor:
            if (dirDist is None):
                raise Exception('Init failed(distributor)')
            self._dirDist = dirDist
            self._setDistributor(groupFilter)
            
        if subscriber:
            if (dirSub is None):
                raise Exception('Init failed(subscriber)')

        if distributor is False and subscriber is False:
            raise Exception('Init failed')

    def _setDistributor(self, groupFilter):
        file_list = os.listdir(self._dirDist)

        for fn in file_list:
            path = self.get_dist_path(fn)
            if os.path.isfile(path) is not True:
                continue

            if fn[0] is '.':
                # hidden file.
                continue

            foundGrName = ''    
            for registedGrName, registedFilterString in groupFilter._dic.items():
                if registedFilterString in path:
                    foundGrName = registedGrName
                    break

            #print('grName: {}, filePath:{}'.format(foundGrName, path) )
            if '' == foundGrName:
                dic = self._dicDefault
            else:
                if self._dicUser is None:
                    self._dicUser = dict()
                if foundGrName not in self._dicUser:
                    self._dicUser[foundGrName] = dict()
                dic = self._dicUser[foundGrName]

            f = open(path, 'rb')
            data = f.read()
            f.close()
            dic[fn] = hashlib.md5(data).hexdigest()

    def get_dist_path(self, fileName):
        return self._dirDist + '/' + fileName

    def print(self):
        print('========= default =======')
        print(self._dicDefault)
        print('========= user =======')
        print(self._dicUser)

    
 


    
    