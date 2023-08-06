from setuptools import setup, find_packages

setup(
    name="ads_api",
    version="0.1.3",
    description="major marketing platform python api",
    packages=find_packages(),
    install_requires=[
        'flask==0.12.2',
        'bingads==11.5.8',
        'googleads==10.0.0',
        'pandas==0.22.0',
        'SQLAlchemy==1.2.3',
        'matplotlib==2.1.2',
        'psycopg2==2.7.4',
        'azure-storage==0.36.0'
    ]
)
