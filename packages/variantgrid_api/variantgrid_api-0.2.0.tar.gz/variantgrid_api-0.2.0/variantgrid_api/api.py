import json
import logging
import os
import requests
from requests_oauthlib.oauth2_auth import OAuth2
from requests_oauthlib.oauth2_session import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

class VariantGridAPI(object):
    def __init__(self,
        user = None,
        password = None,
        host = 'https://shariant.org.au',
        basic_auth = False,
        oauth_url = 'https://shariant.org.au/auth/realms/agha/protocol/openid-connect/token',
        client_id = 'shariant-client-tools',
        verbose=False):

        if user and password and basic_auth:
            self.auth = (user, password)
        elif user and password and oauth_url and client_id:
            oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
            if verbose:
                print(user)
                print(password)
                print(client_id)
                print(oauth_url)
            token = oauth.fetch_token(token_url=oauth_url, username=user, password=password, client_id=client_id)
            self.auth = OAuth2(client_id = client_id, token = token)
        else:
            self.auth = None
        self.host = host
        self.verbose = verbose
    
    @staticmethod
    def from_args(args):
        return VariantGridAPI(user = args.user,
                              password = args.password,
                              host = args.host,
                              basic_auth = args.basic_auth,
                              oauth_url = args.oauth_url,
                              client_id = args.client_id,
                              verbose = args.verbose)
        
    
    @property
    def url(self):
        u = "%s" % self.host
        return u
    
    def get(self, path, extension = '.json'):
        # extension defaults to .json for variantgrid methods that expect it
        # maybe should add .json to the end of shariant methods for consistancy?
        url_path = os.path.join(self.url, path) + extension
        r = requests.get(url_path, auth=self.auth)
        r.raise_for_status()
        try:
            return json.loads(r.text)
        except Exception as e:
            logging.error("Couldn't decode: %s" % r.text)
            logging.error(e)
        return None
    
    def _send(self, path, method, data):
        url_path = os.path.join(self.url, path)
        r = None
        if data is not None:
            data = json.loads(data)
        
        if method == 'POST':
            r = requests.post(url_path, auth=self.auth, data=data)
        elif method == 'PUT':
            r = requests.put(url_path, auth=self.auth, data=data)
        elif method == 'PATCH':
            r = requests.patch(url_path, auth=self.auth, data=data)
        elif method == 'DELETE':
            r = requests.put(url_path, auth=self.auth, data=data)
        else:
            raise ValueError('Unsupported method ' + str(method))

        r.raise_for_status()
        try:
            return json.loads(r.text)
        except Exception as e:
            logging.error("Couldn't decode: %s" % r.text)
            logging.error(e)
            raise e

    def put(self, path, data):
        return self._send(path, 'PUT', data)
    
    def patch(self, path, data):
        return self._send(path, 'PATCH', data)

    def post(self, path, data):
        return self._send(path, 'POST', data)

    def delete(self, path, data):
        return self._send(path, 'PUT', data)

    # shariant stuff below

    def shariant_classification_all(self):
        '''
        Retrieves a list of shariant classifications the user has access to, will just provide ids
        '''
        return self.get('variantclassification/api/shariant/classification', extension = '')

    def shariant_classification(self, record_id, version = None):
        '''
        Retrieves a shariant classification
        @param record_id either number that match internal id or previously posted lab id prefixed with 'L_'
        @param version optional, load the classification at this version (or latest if None)
        '''
        if version is None:
            return self.get('variantclassification/api/shariant/classification/' + str(record_id), extension = '')
        else:
            return self.get('variantclassification/api/shariant/classification/' + str(record_id) + '?version=' + str(version), extension = '')

    def shariant_classification_modify(self, record_id = None, method = 'POST', change = {}):
        '''
        Lets you update or create a shariant classification.
        If POST, record_id can be left blank or to use an internal code prefix any string with 'L_'
        If PATCH or PUT record_id can be it's internal id number or a previously used lab id prefixed with 'L_'
        '''
        #FIXME escape record_id in case it has a slash in it
        return self._send('variantclassification/api/shariant/classification/' + str(record_id) + '?overwrite=true', method, change)

    def shariant_keys(self):
        '''
        Returns all the currently registered key values for classification evidence and meta data about them.
        '''
        return self.get('variantclassification/api/shariant/keys', extension = '')


    # variant grid stuff below

    def loci_variants(self, variant_string):
        ''' returns a list of variant objects for this loci '''
        pass

    def gene_annotation(self, ensembl_gene__id, version=None):
        return self.get('annotation/api/gene_id/%(ensembl_gene__id)s' % {'ensembl_gene__id' : ensembl_gene__id})

    def gene_annotations(self, gene_symbol, version=None):
        ''' This may return multiple annotations for multiple genes '''
        return self.get('annotation/api/gene/%(gene_symbol)s' % {'gene_symbol' : gene_symbol})

    def variant_annotation(self, variant_string, version=None):
        ''' variant_string can be ID, rsId, HGVS '''
        return self.get('annotation/api/variant/%(variant_string)s' % {'variant_string' : variant_string})


    def get_gene_list_genes(self, pk=None, category=None, name=None, version=None):
        ''' Use either PK or both (category, name) '''
        too_many = pk and any([category, name])
        too_few = pk is None and not all([category, name])
        if too_many or too_few:
            msg = "You need to supply either 'pk' OR both ('category' AND 'name') arguments"
            raise ValueError(msg)

        if pk:
            gene_list = self.get('snpdb/gene_list/%s' % pk)
        else:
            gene_list = self.get('snpdb/named_gene_list/%s/%s' % (category, name))
        return gene_list["genelistgene_set"]
