import datetime
import pandas as pd
from io import StringIO

from ads_api.google.google_adwords import GoogleAdwordsReport
from ads_api.credentials import GoogleAdsCredentials


def get_keyword_performance_to_df(platform_ids, days_from_today=14, columns=None,
                                  include_budget_id=False, include_zero_impressions=False):

    start_date = (datetime.datetime.today() - datetime.timedelta(days=days_from_today)).strftime("%Y%m%d")
    end_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

    if columns:
        columns = ', '.join([col.value for col in columns])
    else:
        columns = ['Date', 'CampaignId', 'CampaignName', 'AdGroupId',
                   'AdGroupName', 'CpcBid', 'Device', 'AverageCost',
                   'SearchExactMatchImpressionShare', 'SearchImpressionShare',
                   'Conversions', 'Cost', 'Impressions', 'Clicks', 'Criteria', 'Id',
                   'CostPerConversion', 'SystemServingStatus']
        columns = ', '.join(columns)

    report_query = (
        'SELECT {columns} '
        'FROM KEYWORDS_PERFORMANCE_REPORT '
        # 'WHERE SystemServingStatus!="RARELY_SERVED" AND '
        # 'Impressions=0 '
        'DURING {start_date}, {end_date}'.format(
            columns=columns, start_date=start_date, end_date=end_date
        )
    )

    print('report query: ', report_query)
    dfs = []
    for platform_id in platform_ids:

        try_times = 3

        while try_times > 0:

            try:

                report_string = GoogleAdwordsReport.download_report_string(
                    adwords_client=GoogleAdsCredentials.get_google_client(client_customer_id=platform_id),
                    report_query=report_query,
                    include_zero_impressions=include_zero_impressions
                )

                if report_string:

                    df = pd.read_csv(StringIO(report_string), header=None)
                    df.columns = columns.split(', ')

                    if include_budget_id:
                        budget_campaign = get_budget_with_campaign_id(platform_id, start_date, end_date)
                        df = df.merge(budget_campaign, on=['CampaignId'], how='left')

                    dfs.append(df.assign(AccountId=platform_id))

                    break

            except Exception as e:
                print('download error: ', e)
                try_times -= 1
                pass

    return pd.concat(dfs)


def get_budget_with_campaign_id(platform_id, start_date, end_date, include_zero_impressions=False):

    report_query = ('SELECT BudgetId, BudgetName, AssociatedCampaignId, Amount '
                    'FROM BUDGET_PERFORMANCE_REPORT '
                    'DURING {}, {}'.format(start_date, end_date))

    report_string = GoogleAdwordsReport.download_report_string(
        adwords_client=GoogleAdsCredentials.get_google_client(client_customer_id=platform_id),
        report_query=report_query,
        include_zero_impressions=include_zero_impressions
    )

    budget_data = pd.read_csv(StringIO(report_string))
    budget_data.columns = ['BudgetId', 'CampaignId', 'Amount']

    return budget_data
