from ads_api.credentials import GoogleAdsCredentials
import pandas as pd


def get_account_budget(client_customer_id, n_entries=1):
    """"""
    client = GoogleAdsCredentials.get_google_client(client_customer_id=client_customer_id)
    budget_order_service = client.GetService('BudgetOrderService', version='v201809')
    selector = {
        'ordering': [{
            'field': 'StartDateTime',
            'sortOrder': 'DESCENDING'
        }]
    }

    page_size = min(500, n_entries)
    offset = 0
    more_results = True
    results = []

    while more_results and offset < n_entries:
        selector['paging'] = {
            'startIndex': str(offset),
            'numberResults': str(page_size)
        }

        page = budget_order_service.get(selector)

        if page['entries']:
            for entry in page['entries']:
                results.append({
                    'spendingLimit': entry['spendingLimit']['microAmount'] / 1000000,
                    'startDateTime': entry['startDateTime'],
                    'endDateTime': entry['endDateTime'],
                    'billingAccountId': entry['billingAccountId'],
                    'billingAccountName': entry['billingAccountName']
                })

            # Increment values to request the next page.
            offset += page_size
        else:
            print('No ad group bid modifiers returned.')
        more_results = int(page['totalNumEntries']) > offset

    return pd.DataFrame(results)


def get_budgets(client_customer_id):

    client = GoogleAdsCredentials.get_google_client(client_customer_id=client_customer_id)
    budget_service = client.GetService('BudgetService', version='v201809')

    selector = {
        'fields': ['BudgetId', 'BudgetName', 'Amount']
    }

    page_size = 500
    offset = 0
    more_results = True
    results = []

    while more_results:
        selector['paging'] = {
            'startIndex': str(offset),
            'numberResults': str(page_size)
        }

        page = budget_service.get(selector)

        if page['entries']:
            for entry in page['entries']:
                results.append({
                    'budgetId': entry.budgetId,
                    'name': entry.name,
                    'amount': entry.amount.microAmount
                })
            # Increment values to request the next page.
            offset += page_size
        else:
            print('No ad group bid modifiers returned.')
        more_results = int(page['totalNumEntries']) > offset

    return pd.DataFrame(results)


if __name__ == '__main__':
    df = get_budgets('104-850-5628')
    print(df)
