# see the Apple API reference for json key/values in the requests and the responses:
#  https://developer.apple.com/business/documentation/MDM-Protocol-Reference.pdf

import argparse, json, pprint, requests, sys

from vpp_shared import VppConfig

# this call returns a dictionary with adamId keys and the assets record as the value
def get_assets_for_token(vppConfig, vppToken):
    getAssetsRequest = {
        "sToken" : vppToken,
        "includeLicenseCounts" : True
    }

    response = requests.post(vppConfig.getVPPAssetsSrvUrl, json = getAssetsRequest)

    assetsResponse = json.loads(response.text)
    assetsList = (assetsResponse["assets"] if (assetsResponse != None and assetsResponse.get("assets") != None) else [])

    return { asset["adamIdStr"] : asset for asset in assetsList }


def main():
    parser = argparse.ArgumentParser(description = "Calls into Apple's VPP API to get all the assets under a vpp token")    
    parser.add_argument("--token", help = "Apple VPP token file downloaded from ABM/ASM", required = True)

    args = parser.parse_args()

    with open(args.token, "r") as vt:
        vppToken = vt.read()

    vppConfig = VppConfig()

    assets = get_assets_for_token(vppConfig, vppToken)
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(assets)


if __name__ == '__main__':
    main()
