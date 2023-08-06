from sqlalchemy.orm import sessionmaker
from ads_api.database.dealer_config import db, DealerConfig
import pandas as pd

Session = sessionmaker(db)
session = Session()


def get_configuration_to_df(platform_ids):

    try:
        rows = session.query(DealerConfig).filter(DealerConfig.platform_id.in_([str(id_) for id_ in platform_ids])).all()
    except Exception as e:
        print('config error', e)
        db.session.rollback()
        return

    return pd.DataFrame([row.__dict__ for row in rows]).drop('_sa_instance_state', axis=1)


if __name__ == '__main__':

    print(get_configuration_to_df(['152010282']))
