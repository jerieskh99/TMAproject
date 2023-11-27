# TMAproject

We developed a simple web crawler designed to identify potential tracking pixels on specified website. The steps in which this crawler works in can be described in these 7 steps:  Certainly! Let's delve into each step with a bit more detail:
1. Target Identification:
• In this step we choose the URL of interest, such as health and government website, where tracking might be a concern.
2. Content Fetching:
• In this step we send HTTP requests to the listed URLs and retrieve their HTML content.
• That way we gather the raw HTML content from each target URL for analysis.
• In this step we used the library ‘requests’, which is a library in Python simplifies the process
of making HTTP requests, allowing you to send HTTP/1.1 requests without needing to manually add query strings to your URLs, or form-encode your POST data. In other words it abstracts away the complexities of crafting HTTP/1.1 requests, which are the standard format for web communication, and automates adding data to URLs and POST requests, and simplifying the interaction with web resources and APIs.
3. HTML Parsing:
• In this step we process the HTML content and create a parse tree that can be easily queried
for specific elements.
• Now the raw HTML code is converted into a searchable, navigable structure.
• In this step we used the library ‘BeautifulSoup’, which is a Python library that enables easy
parsing and navigating of the HTML and XML documents of web pages.
4. Element Extraction:
• In this step we search the parsed HTML for <script> and <img> tags with certain attributes that indicate a potential for tracking - in our simple implementation we look for the attribute <src>.
• This way we can identify elements within the HTML that are commonly used for tracking, like small images and external scripts.
• We also used ‘BeautifulSoup’ library for this step.
5. Domain Analysis:
• Here we analyze the domains of the URLs found in script sources and image sources to identify third-party requests.
• In this way we can determine if the resources are hosted on the website's domain (first- party) or a different one (third-party).
• Here we used the module ‘urllib.parse’ from the Python standard library which is used to Analyze and compare the URLs.
6. JavaScript Execution:
• In this step we go a little further, and we use a browser automation tool to render JavaScript
on the page and then search for tracking pixels.
• Since many tracking pixels are loaded dynamically with JavaScript, this step might be
crucial to detect these types of methods.
• We used the library ‘Selenium’ for implementing this step, which is a powerful tool for
automating web browsers, enabling developers to programmatically interact with webpages
by simulating user actions.
• In this step, the crawler uses Selenium to mimic a browser, capturing tracking pixels that are
dynamically added by JavaScript after the initial page load. Selenium opens a browser, navigates to the URL, and waits for JavaScript to execute, including Asynchronous JavaScript and XML (AJAX) calls, a web development technique used to create asynchronous web applications, allowing for content updates on a web page without reloading the entire page. It then accesses the browser's DOM Document Object Model, a programming interface for web documents that represents the page structure as a tree of objects, which can be manipulated with languages like JavaScript.
• In this approach more advance tracking methods can be uncovered.
7. Reporting:
• Now in the final step we organize the data that we have collected in the previous steps. • Basically we compile the results into a CSV file.
• Here we used the CSV library to create and modify the CSV file.
