from flask import Flask, request

from ads_api.bing.reporting.report_to_dataframe.keyword_performance import get_keyword_performance_to_df
from ads_api.bing.reporting.report_to_dataframe.dealer_config import get_configuration_to_df

app = Flask(__name__)


@app.route('/', methods=['POST'])
def get_keyword_performance_df():

    data = request.get_json()

    account_ids = data['account_ids']
    days_from_today = data['days_from_today']
    columns = data['columns']

    return get_keyword_performance_to_df(
        account_ids=account_ids,
        days_from_today=days_from_today,
        columns=columns
    ).to_csv(index=False)


@app.route('/config', methods=['POST'])
def get_config_df():

    data = request.get_json()

    account_ids = data['account_ids']

    return get_configuration_to_df(platform_ids=account_ids).to_csv(index=False)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
