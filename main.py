import os
import logging
import json
import argparse
import re
import pandas as pd
from htmlmin import minify
from lxml.html.clean import Cleaner

"""
Python package functionalities:
Comparation of HTMLs with and without JavaScript rendered of websites.
"""

def create_dataframe(data):
    # Create the initial dataframe from manifest JSON.
    # 7 FINAL COLUMNS OF DATAFRAME:
    # ['final_url', 'first_url', 'path_file', 'domain', 'percentage_of_change'
    df_data = pd.DataFrame(data)
    df_data['domain'] = ""
    df_data['percentage_of_change'] = ""
    return df_data

def building_df_with_percentages(df_tools, arguments_argparser, logger):
    # Replace df with the corrresponding values and get percentage of change:
    for i, tool in df_tools.iterrows():
        # Get the domain for each URL
        df_tools.at[i, 'domain'] = tool['first_url'].split(
            '//')[-1].split("/")[0].replace("www.", "").lower()
        # Extract percentage of change
        df_tools.at[i, 'percentage_of_change'] = extract_percentage(
            tool, arguments_argparser, logger)
    return df_tools

def open_json(path):
    # Open JSON file and return a the object as a dict:
    with open(path, "r") as file:
        return json.load(file)

def write_json_file(data, path):
    # Write on a json file a list of dictionaries:
    with open(path, 'w') as file:
        json.dump(data, file)

def clean_and_minify_html(html):
    # Function to clear html leaving only tags and content.
    cleaner = Cleaner(page_structure=True,
                      safe_attrs_only=True, safe_attrs=frozenset())
    html = re.sub(r"\bencoding='[-\w]+'", "", html)
    html = re.sub("<\\?xml.*?\\?>", "", html)
    html = cleaner.clean_html(html)
    html = html.replace("\n", "").replace("\r", "").replace(
        "\t", "").replace("\\n", "").replace("\\\n", "")
    # Minify the html to extract delete comments
    html = minify(html, remove_comments=True, remove_empty_space=True)
    return html

def extract_percentage(tool, arguments_argparser, logger):
    # Extract the html without JS:
    tool_html_no_js = open_json(
        f"{arguments_argparser.path_i_folder_htmls_no_js}/{tool['path_file']}")
    try:
        # Open the html JS:
        tool_html_js = open_json(
            f"{arguments_argparser.path_i_folder_htmls_js}/{tool['path_file']}")

        # Clean HTML no JS:
        tool_html_no_js_cleaned = clean_and_minify_html(
            tool_html_no_js['html_no_js'])

        # Clean HTML JS:
        html_js_cleaned = clean_and_minify_html(tool_html_js['html_js'])
    except Exception as exception:
        logger.error(f"Exception raised: {str(exception)}\t in {tool}")
        return None

    # Calculate percentage of change:
    percentage = (1-(len(tool_html_no_js_cleaned)/len(html_js_cleaned)))*100
    return percentage

def cleaning_df(df_uncleaned):
    # Drop values null
    df_non_na = df_uncleaned.dropna()
    df_non_na = df_non_na.copy()
    # Replace negative values for 0
    df_non_na.loc[df_non_na.percentage_of_change <
                  0, 'percentage_of_change'] = 0
    return df_non_na

def create_dict_website_minimum_year(tools_year):
    # Get all the years of a website. From tools with year.
    dict_web_year = {}
    for tool in tools_year:
        if tool['year']:
            dict_web_year.setdefault(tool['web']['homepage'], []).append(tool['year'])
    for item in dict_web_year.items():
        item[1].sort()
    return dict_web_year

def match_websites_add_year(dict_website_year, df_input):
    # Copy the df to avoid warning from Pandas
    df_copied = df_input.copy()
    df_copied["year"] = ""
    # Match ['first_url'] and add the column value of the year:
    for i, tool in df_copied.iterrows():
        if tool['first_url'] in dict_website_year.keys():
            df_copied['year'][i] = dict_website_year[tool['first_url']]
    return df_copied

def main(arguments):
    # Set up logging to file
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %y %H:%M:%S',
                        filename=f'{args.log_file_name}',
                        filemode='w')
    # Define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # Set a format which is simpler for console use.
    formatter = logging.Formatter('%(levelname)-12s %(filename)-12s %(message)s')

    # Tell the handler to use this format.
    console.setFormatter(formatter)

    # Add the handler to the root logger.
    logging.getLogger().addHandler(console)

    # Open the manifest file from scrapycrawler.
    manifest = open_json(arguments.path_i_file_manifest)

    logging.info(f"{len(manifest['tools_ok'])} total websites from Scrapy.")
    # Create dataframe from tools
    df_tools = create_dataframe(manifest['tools_ok'])

    # Calculated percentage of change
    logging.info("Starting the calculation of the percentage of change.. \nESTIMATED TIME: 12min")
    df_tools_percentages = building_df_with_percentages(df_tools, arguments, logging)

    # Clean dataframe from null values (websites down)
    df_cleaned = cleaning_df(df_tools_percentages)

    # Open file of tools matched with his year of publication
    tools_year = open_json(arguments.path_i_file_tools_pub_year)

    # Create a dict of website and the first year of that website.
    dict_website_year = create_dict_website_minimum_year(tools_year)

    # Add the column year to dataframe and match websites
    final_df_year_websites = match_websites_add_year(dict_website_year, df_cleaned)

    final_df_year_websites.to_json(
        f"{arguments.path_o_directory_data}/{arguments.o_filename}", orient="records")

    logging.info(f"Saved dataframe in {arguments.path_o_directory_data}/{arguments.o_filename}")

if __name__ == "__main__":

    # Instance of the class ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Determine the percentage of change between HTML with JS and HTMLs without JS.")

    # Input directory of htmls without Javascript.
    parser.add_argument(
                        '-path_i_folder_htmls_no_js',
                        type=str,
                        metavar="",
                        default="../mastercrawlerTFG/htmls_no_js",
                        help="Path of the directory that contains HTMLs with no JavaScript."
                        )

    # Input directory of htmls with Javascript.
    parser.add_argument(
                        '-path_i_folder_htmls_js',
                        type=str,
                        metavar="",
                        default="../seleniumCrawler/htmls_js",
                        help="Path of the directory that contains HTMLs with JavaScript."
                        )

    # Input path of the input file of tools:
    parser.add_argument(
                        '-path_i_file_manifest',
                        type=str,
                        metavar="",
                        default="../mastercrawlerTFG/output_data/manifest_tools_scrapy.json",
                        help="Path of the input file of tools. "
                        )

    # Input path of the input file of tools:
    parser.add_argument(
                        '-path_i_file_tools_pub_year',
                        type=str,
                        metavar="",
                        default="tools_with_year.json",
                        help="Path of the tools that have a year of publication. "
                        )

    # Ouput directory for data:
    parser.add_argument(
                        '-path_o_directory_data',
                        type=str,
                        metavar="",
                        default="output_data_website_analysis",
                        help="Name of data output directory. Default: output_data_website_analysis."
                        )

    # # Output filename of stadistics
    parser.add_argument(
                        '-o_filename',
                        type=str,
                        metavar="",
                        default="df_years_percentages.json",
                        help="Name of output filename. Default: df_years_percentages.json "
                        )

    # Add the argument of output's filename of log.
    parser.add_argument(
                        '-log_file_name',
                        type=str,
                        metavar="",
                        default="websites_analysis.log",
                        help="Name of the output log file of the program"
                        )

    args = parser.parse_args()

    if not os.path.isdir(args.path_o_directory_data):
        os.mkdir(args.path_o_directory_data)

    main(args)
