from ads_api.bing.reporting.reporting_helpers import BingAdsReportingHelpers


@staticmethod
def get_budget_summary_report_request(account_id=None, days_from_today=14):
    """
    Build a keyword performance report request, including Format, ReportName, Aggregation,
    Scope, Time, Filter, and Columns.
    """

    report_request = BingAdsReportingHelpers.get_default_report_request(
        report_type='BudgetSummaryReportRequest',
        report_name='My Budget Summary Report'
    )

    # create the scope
    scope = BingAdsReportingHelpers.reporting_service.factory.create('AccountThroughCampaignReportScope')
    if account_id:
        scope.AccountIds = {'long': [int(account_id)]}
    else:
        scope.AccountIds = {'long': None}
    scope.Campaigns = None
    report_request.Scope = scope

    # report_time = BingAdwordsReport.get_report_time(
    #     report_time_type='tns:BudgetSummaryReportTime', days_from_today=90
    # )

    # create the report time
    # report_time = BingAdwordsReport.get_report_time(days_from_today=days_from_today)
    report_time = BingAdsReportingHelpers.reporting_service.factory.create('BudgetSummaryReportTime')

    report_time.PredefinedTime = 'Today'
    # report time
    report_request.Time = report_time

    # create the report columns
    report_columns = BingAdsReportingHelpers.reporting_service.factory.create('ArrayOfBudgetSummaryReportColumn')
    report_columns.BudgetSummaryReportColumn.append([
        'AccountName',
        'AccountNumber',
        'AccountId',
        'CampaignName',
        'CampaignId',
        'Date',
        'CurrencyCode',
        'MonthlyBudget',
        'DailySpend'
    ])

    report_request.Columns = report_columns
    return report_request
