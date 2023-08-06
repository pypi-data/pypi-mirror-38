from ads_api.bing.reporting.reporting_helpers import BingAdsReportingHelpers


def get_campaign_adgroups_report_request(account_id):

    account_id = int(account_id)
    report_request = BingAdsReportingHelpers.get_default_report_request(
        report_type='AdGroupPerformanceReportRequest',
        report_name='My Ad Group Performance Report'
    )

    report_request.Aggregation = 'Summary'  # Hourly, Daily

    scope = BingAdsReportingHelpers.reporting_service.factory.create('AccountReportScope')
    scope.AccountIds = {'long': [account_id]}
    report_request.Scope = scope

    report_request.Time = BingAdsReportingHelpers.get_report_time(1)

    # If you specify a filter, results may differ from data you see in the Bing Ads web application

    report_filter = BingAdsReportingHelpers.reporting_service.factory.create('AdGroupPerformanceReportFilter')
    report_filter.CampaignStatus = ['Active']
    report_filter.Status = ['Active']
    report_request.Filter = report_filter

    # Specify the attribute and data report columns.

    report_columns = BingAdsReportingHelpers.reporting_service.factory.create('ArrayOfAdGroupPerformanceReportColumn')
    report_columns.AdGroupPerformanceReportColumn.append([
        'CampaignName',
        'CampaignId',
        'AdGroupName',
        'AdGroupId',
        'Spend'
    ])
    report_request.Columns = report_columns

    return report_request
