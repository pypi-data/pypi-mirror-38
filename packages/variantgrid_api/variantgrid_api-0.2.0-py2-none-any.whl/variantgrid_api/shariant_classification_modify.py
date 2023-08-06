from __future__ import print_function
import sys
import json

from variantgrid_api.api import VariantGridAPI

def modify_classifications(args):
    api = VariantGridAPI.from_args(args)
    upload = sys.stdin.read() or {}
    return api.shariant_classification_modify(args.id, args.method, upload)


def shariant_classifications_modify_handle_args(args):
    classifications = modify_classifications(args)
    print(json.dumps(classifications))