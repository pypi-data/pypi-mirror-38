from ads_api.bing.reporting.reporting_helpers import BingAdsReportingHelpers
from suds.sudsobject import asdict


def get_change_history_report_request(account_id, days_from_today, columns=None):

    report_request = BingAdsReportingHelpers.get_default_report_request(
        report_type='SearchCampaignChangeHistoryReportRequest',
        report_name='My Change History Report'
    )

    factory = BingAdsReportingHelpers.reporting_service.factory

    scope = factory.create('AccountThroughAdGroupReportScope')
    scope.AccountIds = {'long': [account_id]}
    report_request.Scope = scope

    report_filter = factory.create('SearchCampaignChangeHistoryReportFilter')
    print('filter: ', asdict(report_filter).keys())

    report_filter.HowChanged = ['Changed']
    report_filter.ItemChanged = ['Keyword']

    report_request.Filter = report_filter

    # create the report time
    report_time = BingAdsReportingHelpers.get_report_time(days_from_today=days_from_today)
    report_request.Time = report_time

    # create the report columns
    report_columns = factory.create('ArrayOfSearchCampaignChangeHistoryReportColumn')
    print('report_columns', type(report_columns.SearchCampaignChangeHistoryReportColumn))
    if columns is None:
        report_columns.SearchCampaignChangeHistoryReportColumn = [
            'CampaignId',
            'CampaignName',
            'AdGroupId',
            'AdGroupName',
            'DateTime',
            'Keyword',
            'AttributeChanged',
            'HowChanged',
            'ItemChanged',
            'OldValue',
            'NewValue'
        ]
    else:
        report_columns.KeywordPerformanceReportColumn = columns

    report_request.Columns = report_columns

    return report_request
