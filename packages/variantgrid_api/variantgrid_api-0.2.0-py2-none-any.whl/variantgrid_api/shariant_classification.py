from __future__ import print_function
import json

from variantgrid_api.api import VariantGridAPI

def get_classifications(args):
    api = VariantGridAPI.from_args(args)

    if args.keys:
        return api.shariant_keys()
    elif args.id:
        return api.shariant_classification(args.id, args.version)
    if args.all:
        return api.shariant_classification_all()

def shariant_classifications_handle_args(args):
    classifications = get_classifications(args)
    print(json.dumps(classifications))