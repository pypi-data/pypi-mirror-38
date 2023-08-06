from ads_api.bing.reporting.report_request.keyword_performance import get_keyword_performance_report_request
from ads_api.bing.download_helpers import BingAdsDownload

import pandas as pd
from io import BytesIO


def get_keyword_performance_to_df(account_ids, days_from_today=14, columns=None):

    dfs = []
    for account_id in account_ids:
        try:
            report_request = get_keyword_performance_report_request(account_id, days_from_today, columns)
            # BingAdsDownload.download_helper(report_request, 'keyword_performance.csv')
            s = BingAdsDownload.download_report_as_string(report_request)
            dfs.append(pd.read_csv(BytesIO(s)).assign(AccountId=account_id))
        except Exception as e:
            print('account: ', account_id, 'failed', e)

    return pd.concat(dfs)
