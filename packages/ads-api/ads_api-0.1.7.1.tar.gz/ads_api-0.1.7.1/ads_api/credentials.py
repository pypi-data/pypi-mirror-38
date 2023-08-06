from bingads.authorization import *
from googleads import adwords
from azure.storage.blob import BlockBlobService
from ads_api.config import LOCAL
import os


class GoogleAdsCredentials:

    _client_id = os.environ.get("googleads_client_id")
    _client_secret = os.environ.get("googleads_client_secret")
    _developer_token = os.environ.get("googleads_developer_token")
    _refresh_token = os.environ.get("googleads_refresh_token")

    yaml_doc = """
        adwords:
            client_id: {client_id}
            client_secret: {client_secret}
            developer_token: {developer_token}
            refresh_token: {refresh_token}
    """.format(
        client_id=_client_id,
        client_secret=_client_secret,
        developer_token=_developer_token,
        refresh_token=_refresh_token
    )

    @staticmethod
    def get_google_client(client_customer_id):

        client = adwords.AdWordsClient.LoadFromString(
            yaml_doc=GoogleAdsCredentials.yaml_doc
        )

        if client_customer_id is not None:
            client.SetClientCustomerId(client_customer_id)

        return client


class BingAdsCredentials:

    _client_id = os.environ.get('bingads_client_id')
    _client_secret = os.environ.get('bingads_client_secret')
    _redirection_uri = os.environ.get('bingads_redirection_uri')
    _refresh_token = os.environ.get('bingads_refresh_token')
    _developer_token = os.environ.get('bingads_developer_token')
    _customer_id = os.environ.get('bingads_customer_id')
    _state = os.environ.get('bingads_state')

    _username_sbx = os.environ.get('bingads_username_sbx')
    _password_sbx = os.environ.get('bingads_password_sbx')
    _developer_token_sbx = os.environ.get('bingads_developer_token_sbx')
    _customer_id_sbx = os.environ.get('bingads_customer_id_sbx')

    @staticmethod
    def get_bing_auth_data(environment, account_id=None):

        if environment == 'sandbox':

            auth_sbx = PasswordAuthentication(BingAdsCredentials._username_sbx, BingAdsCredentials._password_sbx)

            if account_id is None:
                authorization_data = AuthorizationData(
                    customer_id=BingAdsCredentials._customer_id_sbx,
                    developer_token=BingAdsCredentials._developer_token_sbx,
                    authentication=auth_sbx
                )
            else:
                authorization_data = AuthorizationData(
                    account_id=account_id,
                    customer_id=BingAdsCredentials._customer_id_sbx,
                    developer_token=BingAdsCredentials._developer_token_sbx,
                    authentication=auth_sbx
                )

            return authorization_data

        else:

            oauth_web_auth_code_grant = OAuthWebAuthCodeGrant(
                client_id=BingAdsCredentials._client_id,
                client_secret=BingAdsCredentials._client_secret,
                redirection_uri=BingAdsCredentials._redirection_uri
            )

            # It is recommended that you specify a non guessable 'state' request parameter to help prevent
            # cross site request forgery (CSRF).
            oauth_web_auth_code_grant.state = BingAdsCredentials._state

            oauth_web_auth_code_grant.request_oauth_tokens_by_refresh_token(
                refresh_token=BingAdsCredentials._refresh_token
            )

            if not account_id:
                authorization_data = AuthorizationData(
                    customer_id=BingAdsCredentials._customer_id,
                    developer_token=BingAdsCredentials._developer_token,
                    authentication=oauth_web_auth_code_grant
                )
            else:
                authorization_data = AuthorizationData(
                    account_id=account_id,
                    customer_id=BingAdsCredentials._customer_id,
                    developer_token=BingAdsCredentials._developer_token,
                    authentication=oauth_web_auth_code_grant
                )

            return authorization_data


class AzureCredentials:

    if LOCAL:
        _account_name = os.environ.get('azure_account_name_dev')
        _account_key = os.environ.get('azure_account_key_dev')
    else:
        _account_name = os.environ.get('azure_account_name')
        _account_key = os.environ.get('azure_account_key')

    def __init__(self, account_name=None, account_key=None):

        self.account_name = account_name if account_name else AzureCredentials._account_name
        self.account_key = account_key if account_key else AzureCredentials._account_key

    def get_blob_service(self):

        return BlockBlobService(
            account_name=self.account_name,
            account_key=self.account_key
        )