import concurrent.futures, json, requests, threading, time, sys

from dataclasses import dataclass

# the way to use the Vpp API is start with a static endpoint and then to call it periodically
#  so they can change values like batch size; I've not seen the endpoints change but it gives
#  the flexibility to do so
@dataclass
class VppConfig:
    maxBatchAssociateLicenseCount: int
    maxBatchDisassociateLicenseCount: int
    getUsersSrvUrl: str
    getLicensesSrvUrl: str
    manageVPPLicensesByAdamIdSrvUrl: str
    getVPPAssetsSrvUrl: str
    contentMetadataLookupUrl: str

    # https://developer.apple.com/business/documentation/MDM-Protocol-Reference.pdf
    # this is the starting point URL that does not change; all others are subject to change
    __VPP_SERVICE_CONFIG_SRV_URL = \
        "https://vpp.itunes.apple.com/WebObjects/MZFinance.woa/wa/VPPServiceConfigSrv"

    __GET_USERS_SRV = "getUsersSrvUrl"
    __GET_LICENSES_SRV = "getLicensesSrvUrl"
    __EDIT_USERS_SRV = "editUserSrvUrl"
    __RETIRE_USER_SRV = "retireUserSrvUrl"
    __GET_ASSIGNMENTS_SRV = "getAssignmentsSrvUrl"
    __REGISTER_USER_SRV = "registerUserSrvUrl"
    __GET_VPP_ASSETS_SRV = "getVPPAssetsSrvUrl"
    __GET_USERS_SRV = "getUserSrvUrl"
    __CONTENT_METADATA_LOOKUP = "contentMetadataLookupUrl"
    __CLIENT_CONFIG_SRV = "clientConfigSrvUrl"
    __MANAGED_VPP_LICENSES_BY_ADAMID_SRV = "manageVPPLicensesByAdamIdSrvUrl"
    __INVITATION_EMAIL = "invitationEmailUrl"
    __MAX_BATCH_ASSOCIATED_LICENSE = "maxBatchAssociateLicenseCount"
    __MAX_BATCH_DISASSOCIATED_LICENSE = "maxBatchDisassociateLicenseCount"

    def __init__(self):
        super().__init__()
        endpoints = self._sync_vpp_service_endpoints()

        self.maxBatchAssociateLicenseCount = endpoints[self.__MAX_BATCH_ASSOCIATED_LICENSE]
        self.maxBatchDisassociateLicenseCount = endpoints[self.__MAX_BATCH_DISASSOCIATED_LICENSE]
        self.getUsersSrvUrl = endpoints[self.__GET_USERS_SRV]
        self.getLicensesSrvUrl = endpoints[self.__GET_LICENSES_SRV]
        self.manageVPPLicensesByAdamIdSrvUrl = endpoints[self.__MANAGED_VPP_LICENSES_BY_ADAMID_SRV]
        self.getVPPAssetsSrvUrl = endpoints[self.__GET_VPP_ASSETS_SRV]
        self.contentMetadataLookupUrl = endpoints[self.__CONTENT_METADATA_LOOKUP]

    def _sync_vpp_service_endpoints(self):
        response = requests.post(self.__VPP_SERVICE_CONFIG_SRV_URL)
        response.raise_for_status()
        return response.json()
