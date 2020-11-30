
## Software description:
- This software compares HTMLs with and without JavaScript of the same website. After cleaning and minifying them. <br />
It extracts the percentages of change of the website. This is used to understand the importance of JavaScript in a group of websites.

#### Input:
- JSON files that contain the HTML with and without JavaScript rendered of the same website. 
- HTMLs files without JS come from [mastercrawlerTFG](https://github.com/AndreuJove/mastercrawlerTFG). 
- HTMLs files with JS come from [SeleniumCrawler](https://github.com/AndreuJove/seleniumCrawler).


#### Output:
- JSON file that contains all the dynamic percentages of the among of websites. <br />
The file will be saved in output_data directory as: final_df_years_percentages.json<br />

<br />


## Package installation:

1) Open terminal.
2) Go to the current directory where you want the cloned directory to be added using 'cd'.
3) Run the command:<br />
        $ git clone https://github.com/AndreuJove/website_analysis.
4) Taking for granted that you have Python installed in your computer. If not go to: https://www.python.org/downloads/.
5) Once you have Python, install requirements.txt:<br />
        $ pip3 install -r requirements.txt
6) Finally run the following command (default values)<br />
        $ python3 main.py <br />
        -input_percentage 4 <br />
        -path_i_folder_htmls_no_js "../mastercrawlerTFG/htmls_no_js" <br />
        -path_i_folder_htmls_js "../seleniumCrawler/htmls_js" <br />
        -path_i_file_manifest "../mastercrawlerTFG/output_data/manifest_tools_scrapy.json"  <br />
        -path_i_file_tools_pub_year "tools_with_year.json" <br />
        -path_o_directory_data "output_data_website_analysis" <br />
        -o_filename "df_years_percentages.json" <br />
        -log_file_name "websites_analysis.log" <br />
<br />


## Build with:
- [lxml](https://lxml.de) - The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt. It is unique in that it combines the speed and XML feature completeness of these libraries with the simplicity of a native Python API, mostly compatible but superior to the well-known ElementTree API.
- [Pandas](https://pandas.pydata.org/docs/) - is an opensource, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
- [htmlmin](https://htmlmin.readthedocs.io/en/latest/) - htmlmin is an HTML minifier which removes all unnecessary characters from the source code without changing its functionality. It comes with safe defaults and an easily configurable set options. 
- [Argparser](https://docs.python.org/3/library/argparse.html) - The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments it requires, and argparse will figure out how to parse those out of sys.argv. The argparse module also automatically generates help and usage messages and issues errors when users give the program invalid arguments.
- [Logging](https://docs.python.org/3/howto/logging.html) - Logging is a means of tracking events that happen when some software runs. The software’s developer adds logging calls to their code to indicate that certain events have occurred.
- [Regular Expressions](https://docs.python.org/3/howto/regex.html) - Regular expressions (called REs, or regexes, or regex patterns) are essentially a tiny, highly specialized programming language embedded inside Python and made available through the re module.

<br />


## Authors

Andreu Jové.

<br />


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE.MD](https://github.com/AndreuJove/mastercrawlerTFG/blob/master/LICENSE.md) file for details.