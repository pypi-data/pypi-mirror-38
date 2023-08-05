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

class Benefits(BaseObject):
    """
    
    """

    __config = {
        
        "d03857ee-1eb0-4098-aeec-8d762f05ec18" : OperationConfig("/loyalty/v1/benefits/assigned", "query", ["x-client-correlation-id"], ["ica","userId","panLastFourDigits","channel","preferredLanguage"]),
        
        "bc964203-c101-4b04-a2c2-bec9c7c0547d" : OperationConfig("/loyalty/v1/benefits/{benefitId}/detail", "query", ["x-client-correlation-id"], ["ica","channel","preferredLanguage"]),
        
        "4b3abb62-b588-4a80-a37c-b2b490a3bdfa" : OperationConfig("/loyalty/v1/benefits", "query", ["x-client-correlation-id"], ["ica","cardProductType","channel","preferredLanguage"]),
        
        "2bf98212-ecd3-43f5-99ff-27db56db4c4a" : OperationConfig("/loyalty/v1/benefits", "create", ["x-client-correlation-id"], []),
        
        "1c46cf02-6111-45eb-92b1-bdb7ba2bac0e" : OperationConfig("/loyalty/v1/benefits/programterms", "query", ["x-client-correlation-id"], ["ica","preferredLanguage"]),
        
        "251da548-6066-4dbc-ae3a-354fef23d926" : OperationConfig("/loyalty/v1/users/{userId}/benefits", "query", ["x-client-correlation-id"], ["panLastFourDigits"]),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())







    @classmethod
    def getAssignedBenefits(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("d03857ee-1eb0-4098-aeec-8d762f05ec18", Benefits(criteria))






    @classmethod
    def getBenefitDetail(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("bc964203-c101-4b04-a2c2-bec9c7c0547d", Benefits(criteria))






    @classmethod
    def getBenefits(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("4b3abb62-b588-4a80-a37c-b2b490a3bdfa", Benefits(criteria))

    @classmethod
    def selectBenefits(cls,mapObj):
        """
        Creates object of type Benefits

        @param Dict mapObj, containing the required parameters to create a new object
        @return Benefits of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("2bf98212-ecd3-43f5-99ff-27db56db4c4a", Benefits(mapObj))











    @classmethod
    def getProgramTerms(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("1c46cf02-6111-45eb-92b1-bdb7ba2bac0e", Benefits(criteria))






    @classmethod
    def userBenefitsRegistrationStatus(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("251da548-6066-4dbc-ae3a-354fef23d926", Benefits(criteria))


