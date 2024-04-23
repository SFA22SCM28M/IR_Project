# Importing the os module for file and directory operations
import os
# Importing the Scrapy library for web scraping
import scrapy


# Define a Scrapy spider for crawling CS courses
class QuotesSpider(scrapy.Spider):
    # Name of the spider
    name = "crawl_cs"

    # Function to start the requests
    def start_requests(self):
        # Generating a list of URLs to crawl
        urls = ['http://bulletin.iit.edu/search/?P=CS%20'+str(x) for x in range(100, 700)]
        for url in urls:
            # Yielding a request for each URL
            yield scrapy.Request(url=url, callback=self.parse)

    # Function to parse the response from each URL
    def parse(self, response):
        # Extracting the page number from the URL
        page = response.url.split("/")[-1][-3:]
        # Creating a filename to save the HTML content
        filename = f'crawler/cs_courses/{page}.html'
        # Checking if the page has content based on a specific CSS selector
        success = (len(response.css('p.noindent::text').getall()) != 0)
        # If content is found, save the HTML content to a file
        if success:
            with open(filename, 'wb') as f:
                f.write(response.body)
            # Log the successful save
            self.log(f'Saved file {filename}')

# Define another Scrapy spider for parsing CS courses
class CSCourses(scrapy.Spider):
    # Name of the spider
    name = 'cs_course'
    # start_urls = ['http://bulletin.iit.edu/undergraduate/courses/cs/']
    # Define start URLs as local file paths based on existing files in a directory
    start_urls = [f'file://{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/cs_courses/{c}' for c in os.listdir('crawler/cs_courses')]

    # Function to parse the response from each URL
    def parse(self, response):

        # Extracting course information from the response
        classes = response.css('div.searchresults')
        try:
            yield {
                'code': 'CS'+classes.css('h2::text').get().split('\n')[0].strip()[-3:], # Extracting course code
                'title': classes.css('h2::text').get().split('\n')[1].strip(), # Extracting course title
                'link': 'http://bulletin.iit.edu/search/?P=CS%20'+ classes.css('h2::text').get().split('\n')[0].strip()[-3:], # Generating course link
                'description': classes.css('p.noindent::text').get().replace("\n", ""), # Extracting course description
                'credits': classes.css('span::text').extract()[2], # Extracting course credits
                'prerequisites:': ['CS' + x.strip()[-3:] for x in classes.css('div.noindent.courseblockattr').css('a::text').getall()] # Extracting course prerequisites
            }
        # Handling exceptions if parsing fails
        except:
            yield {
                'code': classes.css('div.noindent.coursecode::text').get(), # Extracting course code
                'title': classes.css('strong::text').get(), # Extracting course title
                'link': 'http://bulletin.iit.edu/search/?P=CS%20'+ classes.css('div.noindent.coursecode::text').get()[-3:], # Generating course link
                'description': classes.css('p.noindent::text').get().replace("\n", ""), # Extracting course description
                'credits': classes.css('span::text').extract()[2], # Extracting course credits
                'prerequisites:': ['CS' + x.strip()[-3:] for x in classes.css('div.noindent.courseblockattr').css('a::text').getall()] # Extracting course prerequisites
            }               
