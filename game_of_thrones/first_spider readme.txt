Scrapy Tutorial
https://doc.scrapy.org/en/latest/intro/tutorial.html

cd to the directory you want to start a project in
    > scrapy startproject first_spider

This creates a directory with the necessary tools and files:
tutorial/
    scrapy.cfg            # deploy configuration file
    tutorial/             # project's Python module, you'll import your code from here
        __init__.py
        items.py          # project items definition file
        middlewares.py    # project middlewares file
        pipelines.py      # project pipelines file
        settings.py       # project settings file
        spiders/          # a directory where you'll later put your spiders
            __init__.py

Build the python script: first_spider.py

Navigate to the top of the directory called 'first_spider' and run
    > scrapy crawl quotes

Open the Scrapy shell to
