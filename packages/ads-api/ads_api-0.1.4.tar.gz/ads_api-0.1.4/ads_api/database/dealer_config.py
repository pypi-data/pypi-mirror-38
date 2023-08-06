from sqlalchemy import create_engine, Column, String, FLOAT
from sqlalchemy.ext.declarative import declarative_base
import os

db = create_engine(
    os.environ.get("bid_model_database_url"),
    isolation_level="READ UNCOMMITTED"
)

base = declarative_base()


class DealerConfig(base):
    """"""
    __tablename__ = 'dealer_config'

    platform = Column(String(20), nullable=False, primary_key=True)
    platform_id = Column(String(20), nullable=False, primary_key=True)
    campaign_id = Column(String(50), nullable=False, primary_key=True)
    ad_group_id = Column(String(50), nullable=False, primary_key=True)
    bid_strategy = Column(String(80), nullable=False, primary_key=True)

    campaign_name = Column(String(255), nullable=False)
    ad_group_name = Column(String(255), nullable=False)
    target_position = Column(FLOAT, nullable=False)
    cpc_constraint = Column(FLOAT, nullable=False)
