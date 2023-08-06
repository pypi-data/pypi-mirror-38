@staticmethod
def download_account_keyword_performance_to_azure(account_id, days_from_today=120, columns=None):
    try:
        report_request = BingAdsDownload.get_keyword_performance_report_request(
            account_id=account_id, days_from_today=days_from_today, columns=columns
        )

        string = BingAdsDownload.download_report_as_string(report_request)

        print("Download data for account {} succeeded".format(account_id))
        blob_service = AzureCredentials(
            account_name='googleadwords',
            account_key=os.environ.get('googleadwords_account_key')
        ).get_blob_service()

        blob_service.create_blob_from_text(
            container_name='bingkeywordperformance',
            blob_name='{}/keyword_performance.csv'.format(account_id),
            text=string
        )

        print("Upload data for account {} to azure succeeded".format(account_id))

    except Exception as e:
        print("Error: ", e)
        print("Downloading data for {} failed".format(account_id))


@staticmethod
def download_all_accounts_keyword_performance_to_azure(days_from_today=120, columns=None):
    """
    This function download all keyword performance data for all bing accounts to azure googleadwords/bingkeywordperformance
    :param days_from_today:
    :param columns:
    :return:
    """

    accounts = BingAdsDownload.get_active_accounts()
    account_ids = [account['client_customer_id'] for account in accounts]

    for account_id in account_ids:
        BingAdsDownload.download_account_keyword_performance_to_azure(
            account_id=account_id, days_from_today=days_from_today, columns=columns
        )