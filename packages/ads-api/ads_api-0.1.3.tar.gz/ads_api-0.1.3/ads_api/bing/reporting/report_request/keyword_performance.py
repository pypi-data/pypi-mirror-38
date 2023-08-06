from ads_api.bing.reporting.reporting_helpers import BingAdsReportingHelpers


def get_keyword_performance_report_request(account_id, days_from_today=14, columns=None):
    """
    Build a keyword performance report request, including Format, ReportName, Aggregation,
    Scope, Time, Filter, and Columns.
    """

    report_request = BingAdsReportingHelpers.get_default_report_request(
        report_type='KeywordPerformanceReportRequest',
        report_name='My Keyword Performance Report'
    )

    report_request.Aggregation = 'Daily'

    # create the scope
    scope = BingAdsReportingHelpers.reporting_service.factory.create('AccountThroughAdGroupReportScope')
    scope.AccountIds = {'long': [account_id]}
    scope.Campaigns = None
    scope.AdGroups = None
    report_request.Scope = scope

    report_filter = BingAdsReportingHelpers.reporting_service.factory.create('KeywordPerformanceReportFilter')
    report_filter.CampaignStatus = ['Active']
    report_filter.AdGroupStatus = ['Active']
    report_filter.KeywordStatus = ['Active']

    report_request.Filter = report_filter

    # create the report time
    report_time = BingAdsReportingHelpers.get_report_time(days_from_today=days_from_today)

    # report time
    report_request.Time = report_time

    # create the report columns
    report_columns = BingAdsReportingHelpers.reporting_service.factory.create('ArrayOfKeywordPerformanceReportColumn')
    if columns is None:
        report_columns.KeywordPerformanceReportColumn = [
            'TimePeriod',
            'AccountId',
            'CampaignName',
            'AdGroupName',
            'Keyword',
            'CampaignId',
            'AdGroupId',
            'KeywordId',
            'DeviceType',
            'CurrentMaxCpc',
            'Impressions',
            'KeywordStatus',
            'BidMatchType',
            'AveragePosition'
        ]
    else:
        report_columns.KeywordPerformanceReportColumn = columns

    report_request.Columns = report_columns
    return report_request
