#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from __future__ import absolute_import
from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from mastercardmcon import ResourceConfig

class BundleProfile(BaseObject):
    """
    
    """

    __config = {
        
        "5d7dd404-85b1-481f-ad2c-afb395dcf18c" : OperationConfig("/bundle/profile/v1/users", "create", ["x-client-correlation-id"], []),
        
        "6da189ef-7300-47aa-959c-a2150b20f2cb" : OperationConfig("/bundle/profile/v1/users/{userId}", "delete", ["x-client-correlation-id"], []),
        
        "1c9b5edb-46bc-40cd-90c8-5721c673bcbf" : OperationConfig("/bundle/profile/v1/users/{userId}/patch", "create", ["x-client-correlation-id"], []),
        
        "15fa34d5-0539-4447-b3d9-73ae78749d99" : OperationConfig("/bundle/profile/v1/users/{userId}", "read", ["x-client-correlation-id"], []),
        
        "1ff90686-79b9-4d1c-bef9-614fc0528667" : OperationConfig("/bundle/profile/v1/users/{userId}", "update", ["x-client-correlation-id"], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())


    @classmethod
    def createUser(cls,mapObj):
        """
        Creates object of type BundleProfile

        @param Dict mapObj, containing the required parameters to create a new object
        @return BundleProfile of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("5d7dd404-85b1-481f-ad2c-afb395dcf18c", BundleProfile(mapObj))









    @classmethod
    def deleteUserById(cls,id,map=None):
        """
        Delete object of type BundleProfile by id

        @param str id
        @return BundleProfile of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("6da189ef-7300-47aa-959c-a2150b20f2cb", BundleProfile(mapObj))

    def deleteUser(self):
        """
        Delete object of type BundleProfile

        @return BundleProfile of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("6da189ef-7300-47aa-959c-a2150b20f2cb", self)



    @classmethod
    def patchUser(cls,mapObj):
        """
        Creates object of type BundleProfile

        @param Dict mapObj, containing the required parameters to create a new object
        @return BundleProfile of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("1c9b5edb-46bc-40cd-90c8-5721c673bcbf", BundleProfile(mapObj))










    @classmethod
    def readUser(cls,id,criteria=None):
        """
        Returns objects of type BundleProfile by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of BundleProfile
        @raise ApiException: raised an exception from the response status
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("15fa34d5-0539-4447-b3d9-73ae78749d99", BundleProfile(mapObj))



    def updateUser(self):
        """
        Updates an object of type BundleProfile

        @return BundleProfile object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("1ff90686-79b9-4d1c-bef9-614fc0528667", self)






