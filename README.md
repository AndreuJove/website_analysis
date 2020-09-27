
## Software description:
This software compares HTMLs with and without JavaScript of the same website. After cleaning and minifying them. It extracts the percentages of change of the website. This is used to understand the importance of JavaScript in a group of websites.

#### Input:
- JSON files that contain the HTML with and without JavaScript rendered of the same website. 
HTMLs files without JS come from [mastercrawlerTFG](https://github.com/AndreuJove/mastercrawlerTFG).
HTMLs files with JS come from [SeleniumCrawler](https://github.com/AndreuJove/seleniumCrawler).

#### Output:
- JSON file that contains all the dynamic percentages of the among of websites. The file will be saved in output_data directory as:<br />
        all_dynamic_percentages.json
- JSON file of the dynamic percentages of the primary classification about domains. The file will be saved in output_data directory as:<br />
        dynamic_percentages_domains.json
<br />


## Package installation:

- 1) Open terminal.
- 2) Go to the current directory where you want the cloned directory to be added using 'cd'.
- 3) Run the command:<br />
        $ git clone https://github.com/AndreuJove/website_analysis.
- 4) Taking for granted that you have Python installed in your computer. If not go to: https://www.python.org/downloads/.
- 5) Once you have Python, install requirements.txt:<br />
        $ pip3 install -r requirements.txt
- 5) Finally run the following command. Input percentage to separate static websites (no use of JS) and dynamic websites can be changed, the recommendation is a number between 0-4:<br />
        $ python3 main.py -input_percentage 4
<br />


## Build with:
- [lxml](https://lxml.de) - The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt. It is unique in that it combines the speed and XML feature completeness of these libraries with the simplicity of a native Python API, mostly compatible but superior to the well-known ElementTree API.
- [Pandas](https://pandas.pydata.org/docs/) - is an opensource, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
- [htmlmin](https://htmlmin.readthedocs.io/en/latest/) - htmlmin is an HTML minifier which removes all unnecessary characters from the source code without changing its functionality. It comes with safe defaults and an easily configurable set options. 


<br />


## Authors

Andreu Jové (andreujove@gmail.com)

<br />


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE.MD](https://github.com/AndreuJove/mastercrawlerTFG/blob/master/LICENSE.md) file for details.