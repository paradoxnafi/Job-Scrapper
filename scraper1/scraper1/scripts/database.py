import json
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

with open('config.json') as f:
    config = json.load(f)

# Database configuration
user = config['SIMETRA_USER']
password = config['SIMETRA_PASSWORD']
host = config['HOST']
port = config['PORT']
database = config['DATABSE']

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# job_posting_sites table schema
class JobPostingSite(Base):
    __tablename__ = 'job_posting_sites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(1024), nullable=False)
    url = Column(String(1024), nullable=False)
    created_at = Column(Date, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(Date, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # jobs = relationship('Job', backref='job_posting_site', lazy=True)

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)


# jobs table schema
class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_posting_site_id = Column(Integer, ForeignKey('job_posting_sites.id'), nullable=False)
    title = Column(String(1024))
    is_scraped = Column(Boolean, default=False, nullable=False)
    company_name = Column(String(1024))
    post_url = Column(String(1024), unique=True, nullable=False)
    tag = Column(String(1024))
    job_id = Column(String(1024))
    post_date = Column(Date)
    closing_date = Column(Date)
    created_at = Column(Date, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(Date, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, job_posting_site_id, title=None, is_scraped=False, company_name=None, post_url=None, tag=None, job_id=None, post_date=None, closing_date=None):
        self.job_posting_site_id = job_posting_site_id
        self.title = title
        self.is_scraped = is_scraped
        self.company_name = company_name
        self.post_url = post_url
        self.tag = tag
        self.job_id = job_id
        self.post_date = post_date
        self.closing_date = closing_date
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
