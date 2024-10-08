# Job Scraper - Timor-Leste

This application scrapes job postings from the following job sites:
1. **Vagaservisu**
2. **Lafeak**
3. **UNJobs**
4. **LinkedIn**

## How to Run

To run this project, follow the steps below:

1. **Install Dependencies**  
   Ensure all the required packages are installed. You can do this by running:
   ```bash
   pip install -r requirements.txt
2. **Run the Spiders**  
   To start the scraping process, simply execute the following command:
   ```bash
   ./run_spiders.sh
   ```
   This will:
   - Run all four spiders
   - Perform data cleaning
   - Insert the cleaned data into the database

## Database Configuration

Database connection details are stored in the config.json file. Ensure this file is properly configured before running the project.

- Install the required Python packages as mentioned in the requirements.txt file.
- Install the latest version of Google Chrome as it is needed for web scraping.
```text
Note: You may need to install the appropriate ChromeDriver to match the version of Chrome on your system.
```
## Cron Job (Optional)

For continuous data scraping, you can set up a cron job to automate the process. Here's an example of how you can configure your cron job to run the scraper every 3 days at 1 AM:

```bash
0 1 */3 * * /var/www/html/job-scraper-timorleste/run_spiders.sh >> /var/www/html/job-scraper-timorleste/cron-job.log 2>&1
```
This will log the output of the cron job to `cron-job.log`.

## Additional Notes
- **Logging:** Ensure the log file is being monitored for errors.
- **ChromeDriver:** The correct version of ChromeDriver should match the version of Chrome installed on your machine. You can download the correct version from ChromeDriver Downloads.