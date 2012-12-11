import swift_client

full_auth_url = 'https://auth.dfw1.swift.racklabs.com:443/auth/v2.0'
user = 'nova-staging%3Anova-staging-acct'
key = 'm5XWk8E'
snet = False
auth_version = '2.0'

connection = swift_client.Connection(
    full_auth_url, user, key, snet=snet, auth_version=auth_version)

print connection.head_object('images', 'this_is_a_test_5')