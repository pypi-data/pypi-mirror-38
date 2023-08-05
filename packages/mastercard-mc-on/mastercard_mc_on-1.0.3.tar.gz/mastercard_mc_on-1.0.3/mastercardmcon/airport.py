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

class Airport(BaseObject):
    """
    
    """

    __config = {
        
        "0c72bbb0-059a-4074-ae10-39c353557bcf" : OperationConfig("/loyalty/v1/airport/dmc", "query", ["x-client-correlation-id"], ["userId","panLastFourDigits"]),
        
        "6a380410-f67b-465e-851e-6f7aad1c5c43" : OperationConfig("/loyalty/v1/airport/history", "query", ["x-client-correlation-id"], ["userId","panLastFourDigits","preferredLanguage","transactionDateFrom","transactionDateTo"]),
        
        "00612ed1-afe2-45fd-ad97-dcde2e161379" : OperationConfig("/loyalty/v1/airport/lounges", "query", ["x-client-correlation-id"], ["userId","panLastFourDigits","searchText","preferredLanguage"]),
        
        "22d3b6c0-6b89-4a7e-bc11-fdbf1d112146" : OperationConfig("/loyalty/v1/airport/lounges/{loungeCode}/detail", "query", ["x-client-correlation-id"], ["userId","panLastFourDigits","preferredLanguage"]),
        
        "b68a1cce-baea-4265-bb9e-11da557e71a5" : OperationConfig("/loyalty/v1/users/{userId}/airport", "query", ["x-client-correlation-id"], ["panLastFourDigits"]),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())







    @classmethod
    def getDMC(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("0c72bbb0-059a-4074-ae10-39c353557bcf", Airport(criteria))






    @classmethod
    def getLoungeHistory(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("6a380410-f67b-465e-851e-6f7aad1c5c43", Airport(criteria))






    @classmethod
    def getLounges(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("00612ed1-afe2-45fd-ad97-dcde2e161379", Airport(criteria))






    @classmethod
    def getLoungeDetail(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("22d3b6c0-6b89-4a7e-bc11-fdbf1d112146", Airport(criteria))






    @classmethod
    def userAirportRegistrationStatus(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("b68a1cce-baea-4265-bb9e-11da557e71a5", Airport(criteria))


