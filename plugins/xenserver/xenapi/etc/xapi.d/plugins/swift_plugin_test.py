import XenAPI
import cPickle as pickle
import swift
import uuid

session = XenAPI.Session('http://localhost')
session.login_with_password('root', 'Iz8-HXk7E0')
host, = session.xenapi.host.get_all()

args = [["c4a91909-e9ee-4fc7-a6ff-4b42b526a2b9"],
        "/var/run/sr-mount/60c0f0a2-4a37-d740-124b-3a0af60100e9",
        'this_is_a_test_5']

kwargs = {
    'swift_enable_snet': False,
    'swift_store_user': 'nova-staging%3Anova-staging-acct',
    'swift_store_key': 'm5XWk8E',
    'swift_store_auth_version': '1',
    'swift_store_container': 'images',
    'swift_store_large_object_size': 5120,
    'swift_store_large_object_chunk_size': 4096,
    'swift_store_create_container_on_put': True,
    'full_auth_address': 'https://auth.dfw1.swift.racklabs.com:443/auth/v1.0',
    'storage_url': 'https://storage101.dfw1.clouddrive.com/v1/SOSO_cd836391-e476-437c-96ef-4930f80dff3e',
    'token': 'SOSO_tkdfedf0db86d44bd2b2292fc84486d503',
    }

pickled = {'params': pickle.dumps(dict(args=args, kwargs=kwargs))}

'''try:
    print session.xenapi.host.call_plugin(host, 'swift', 'upload_vhd', pickled)
except Exception, e:
    print e'''

print swift.upload_vhd(None, *args, **kwargs)