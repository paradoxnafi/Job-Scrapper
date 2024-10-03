import os
import json
import glob
from sqlalchemy import exc
from datetime import datetime
from database import JobPostingSite, Job, session


def get_matching_files(directory, sites):
    files = glob.glob(os.path.join(directory, '*_cleaned.jsonl'))
    matches = {}

    for site in sites:
        for file in files:
            filename = os.path.basename(file)
            if filename.startswith(site.name.split('_')[0]):
                matches[site] = file
                break

    return matches

def populate_jobs_table(matches):
    for site, file in matches.items():
        with open(file, 'r') as f:
            for line in f:
                try:
                    job_data = json.loads(line)
                    
                    post_date_str = job_data.get('post_date', '')
                    post_date = None
                    if post_date_str:
                        try:
                            post_date = datetime.strptime(post_date_str, '%Y-%m-%d').date()
                        except ValueError:
                            print(f"Invalid post_date format in file {file}: {post_date_str}")
                            continue

                    if post_date and post_date.year >= 2023:
                        job = Job(
                            job_posting_site_id=site.id,
                            title=job_data.get('title', '') or '',
                            is_scraped=1,
                            company_name=job_data.get('company_name', '') or '',
                            post_url=job_data.get('post_url', '') or '',
                            tag=job_data.get('tag', '') or '',
                            job_id=job_data.get('job_id', '') or '',
                            post_date=post_date,
                            closing_date=job_data.get('closing_date', '') or None
                        )
                        session.add(job)

                except Exception as e:
                    print(f"Error processing job data from file {file}: {e}")

        try:
            session.commit()
        except exc.IntegrityError as ie:
            session.rollback()
            print(f"IntegrityError: {ie}. Skipping duplicate entries for site {site.name}.")
        except Exception as e:
            session.rollback()
            print(f"Error committing data for site {site.name}: {e}")

def main():
    try:
        job_posting_sites = session.query(JobPostingSite).all()

        # Match files with job posting sites
        directory = 'scraper1/scraper1/data/cleaned/import/'
        matches = get_matching_files(directory, job_posting_sites)

        # Populate the jobs table
        populate_jobs_table(matches)

        print("Job data has been successfully populated.")
    except Exception as e:
        print(f"An error occurred in the main process: {e}")


if __name__ == "__main__":
    main()
