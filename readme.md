## This is a web scraping tool made for Timor-Leste to scrape job posting data for statistical analysis.

**Note:** The architecture used here is modular. While this example targets job boards, the spiders can be quickly reconfigured to scrape news articles, blog posts, or academic papers while maintaining the same high data integrity and automated cleaning pipeline.

### 📊 Sample Scraped Data (Timor-Leste Job Portals)

The following table demonstrates the structured data captured by the spiders. The tool normalizes diverse sources into a consistent format suitable for statistical analysis and database entry.

| Source | Job Title | Company / Organization | Posted Date | Link |
| :--- | :--- | :--- | :--- | :--- |
| **UNjobs** | Consultant - Digital Communications | UN Women | 2024-10-02 | [View Post](https://unjobs.org/vacancies/1727822418135) |
| **UNjobs** | Senior Officer - ICT | Abt Associates | 2024-09-28 | [View Post](https://unjobs.org/vacancies/1727459264270) |
| **LinkedIn** | Front End Developer | GT Ecom | 2024-09-19 | [View Post](https://www.linkedin.com/jobs/view/4029761206) |
| **LinkedIn** | Graphic and UI/UX Designer | PLS | 2024-09-12 | [View Post](https://www.linkedin.com/jobs/view/4024057801) |
| **Lafeak** | Finance and Operations Manager | CARE Learning Media | 2024-09-12	 | [View Post](https://www.lafaek.tl/finance-and-operations-manager-lafaek-learning-media-project/) |
| **Lafeak** | Monitoring & Learning Specialist | CARE Learning Media | 2024-08-19 | [View Post](https://www.lafaek.tl/monitoring-evaluation-and-learning-specialist-2/) |
| **Vagaservisu** | Social Enterprise Director | CARE in Timor-Leste | 2024-10-06 | [View Post](https://www.vagaservisu.com/2024/10/vaga-servisu-lafaek-social-enterprise.html) |
| **Vagaservisu** | Junior Field Assistant | TOMAK | 2024-10-02 | [View Post](https://www.vagaservisu.com/2024/10/vaga-servisu-junior-field-assistant.html) |
   

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

Note: After installing the dependencies it is recommended to create a cron job to run the spiders automatically

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

## Proxy Configuration with scrapy-rotating-proxies

To avoid being blocked while scraping, you can use the `scrapy-rotating-proxies` middleware. Follow the steps below to set it up:

1. **Install the Package**  
   Add `scrapy-rotating-proxies` to your project by running:
   ```bash
   pip install scrapy-rotating-proxies
   ```
2. **Update Settings**  
   In ```settings.py``` file, enable the middleware and configure your list of proxies:
   ```python
   DOWNLOADER_MIDDLEWARES = {
    'scrapy_rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
   }
   ROTATING_PROXY_LIST = [
      'http://user:pass@proxy1:port',
      'http://user:pass@proxy2:port',
      # Add more proxies as needed
   ]
   ```
   More detailed instruction can be found [here](https://scrapeops.io/python-scrapy-playbook/scrapy-rotating-proxy-guide/)
