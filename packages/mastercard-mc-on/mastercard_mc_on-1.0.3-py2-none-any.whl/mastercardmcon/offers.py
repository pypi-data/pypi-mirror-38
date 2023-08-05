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

class Offers(BaseObject):
    """
    
    """

    __config = {
        
        "7b1ba8b8-85b5-42b1-8fa6-a8ac6dbb192b" : OperationConfig("/loyalty/v1/offers", "query", ["x-client-correlation-id"], ["userId","preferredLanguage","sort","category","featured","favorite","partner"]),
        
        "460eee16-ed13-4b7a-8233-90071ca4399f" : OperationConfig("/loyalty/v1/offers/{offerId}/activate", "create", ["x-client-correlation-id"], []),
        
        "514d3dc4-18b2-44d5-acf3-d3de5b64025a" : OperationConfig("/loyalty/v1/offers/{offerId}/detail", "query", ["x-client-correlation-id"], ["userId","preferredLanguage"]),
        
        "9aa4381f-0ab0-4fd1-a028-2a28ae33fea5" : OperationConfig("/loyalty/v1/offers/{offerId}/favorite", "create", ["x-client-correlation-id"], []),
        
        "85b85152-da21-49d2-b14b-7de09f516f18" : OperationConfig("/loyalty/v1/offers/{offerId}/redeem", "create", ["x-client-correlation-id"], []),
        
        "65c13d14-4f92-4fb8-8dc9-1111001babe3" : OperationConfig("/loyalty/v1/offers/{offerId}/unfavorite", "create", ["x-client-correlation-id"], []),
        
        "c00a90b1-11c0-4ca0-b881-19db5e6960d0" : OperationConfig("/loyalty/v1/offers/promo", "create", ["x-client-correlation-id"], []),
        
        "1c6237dd-90cd-4aab-99ce-7a1f70f09f35" : OperationConfig("/loyalty/v1/offers/redeemed", "query", ["x-client-correlation-id"], ["userId","preferredLanguage"]),
        
        "54105f1e-6ff8-4cad-ae83-f0d94c826260" : OperationConfig("/loyalty/v1/points/expiring", "query", ["x-client-correlation-id"], ["userId"]),
        
        "9e90450d-9cc3-494c-b032-44f9e89867a9" : OperationConfig("/loyalty/v1/points", "query", ["x-client-correlation-id"], ["userId"]),
        
        "6a36e267-29bf-4c34-892f-7d34764d5030" : OperationConfig("/loyalty/v1/users/{userId}/offers", "query", ["x-client-correlation-id"], []),
        
        "15ff4c59-a170-4259-9452-56a65ed80662" : OperationConfig("/loyalty/v1/vouchers", "query", ["x-client-correlation-id"], ["userId"]),
        
        "51aef484-282f-42fe-8dd7-822ac7da5c6f" : OperationConfig("/loyalty/v1/vouchers/{voucherId}/detail", "query", ["x-client-correlation-id"], ["userId"]),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())







    @classmethod
    def getOffers(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("7b1ba8b8-85b5-42b1-8fa6-a8ac6dbb192b", Offers(criteria))

    @classmethod
    def activateOffer(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("460eee16-ed13-4b7a-8233-90071ca4399f", Offers(mapObj))











    @classmethod
    def getOfferDetail(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("514d3dc4-18b2-44d5-acf3-d3de5b64025a", Offers(criteria))

    @classmethod
    def favoriteOffer(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("9aa4381f-0ab0-4fd1-a028-2a28ae33fea5", Offers(mapObj))






    @classmethod
    def redeemOffer(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("85b85152-da21-49d2-b14b-7de09f516f18", Offers(mapObj))






    @classmethod
    def unfavoriteOffer(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("65c13d14-4f92-4fb8-8dc9-1111001babe3", Offers(mapObj))






    @classmethod
    def submitOfferPromo(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("c00a90b1-11c0-4ca0-b881-19db5e6960d0", Offers(mapObj))











    @classmethod
    def getRedeemedOffers(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("1c6237dd-90cd-4aab-99ce-7a1f70f09f35", Offers(criteria))






    @classmethod
    def getPointsExpiring(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("54105f1e-6ff8-4cad-ae83-f0d94c826260", Offers(criteria))






    @classmethod
    def getPoints(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("9e90450d-9cc3-494c-b032-44f9e89867a9", Offers(criteria))






    @classmethod
    def userOffersRegistrationStatus(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("6a36e267-29bf-4c34-892f-7d34764d5030", Offers(criteria))






    @classmethod
    def getVouchers(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("15ff4c59-a170-4259-9452-56a65ed80662", Offers(criteria))






    @classmethod
    def getVoucherDetail(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("51aef484-282f-42fe-8dd7-822ac7da5c6f", Offers(criteria))


