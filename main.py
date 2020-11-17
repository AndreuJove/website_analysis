import os
import json
import argparse
import re
import pandas as pd
from htmlmin import minify
from lxml.html.clean import Cleaner
from lxml.etree import ParserError


"""
Python package functionalities:
Comparation of HTMLs with and without JavaScript rendered of websites.
"""

def create_dataframe(data):
    # Create the initial dataframe from manifest JSON.
    # 7 FINAL COLUMNS OF DATAFRAME:
    # ['final_url', 'id', 'name', 'first_url', 'path_file', 'domain', 'percentage_of_change'
    df_data = pd.DataFrame(data)
    df_data['domain'] = ""
    df_data['percentage_of_change'] = ""
    return df_data

def building_df_with_percentages(df_tools, arguments_argparser):
    # Replace df with the corrresponding values and get percentage of change:
    for i, tool in df_tools.iterrows():
        # Get the domain for each URL
        df_tools.at[i, 'domain'] = tool['first_url'].split(
            '//')[-1].split("/")[0].replace("www.", "").lower()
        # Extract percentage of change
        df_tools.at[i, 'percentage_of_change'] = extract_percentage(
            tool, arguments_argparser)
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
    # Function to clear html leaving only tags and content. Posterior minify.
    cleaner = Cleaner(page_structure=True,
                      safe_attrs_only=True, safe_attrs=frozenset())
    html = re.sub(r"\bencoding='[-\w]+'", "", html)
    html = re.sub("<\\?xml.*?\\?>", "", html)
    html = cleaner.clean_html(html)
    html = html.replace("\n", "").replace("\r", "").replace(
        "\t", "").replace("\\n", "").replace("\\\n", "")
    html = minify(html, remove_comments=True, remove_empty_space=True)
    return html

def extract_percentage(tool, arguments_argparser):
    # Extract the html without JS:
    tool_html_no_js = open_json(
        f"{arguments_argparser.path_i_folder_htmls_no_js}/{tool['path_file']}")
    # Remember: the tool_html_no_js has 2 keys ('id', 'htmls_js')

    # Extract the html JS:
    try:
        tool_html_js = open_json(
            f"{arguments_argparser.path_i_folder_htmls_js}/{tool['path_file']}")
    except FileNotFoundError:
        return None
    # Remember: the tool_html_js has 2 keys ('id', 'htmls_js')

    try:
        # Try clean html no JS:
        tool_html_no_js_cleaned = clean_and_minify_html(
            tool_html_no_js['html_no_js'])
    except ParserError:
        return None

    try:
        # Clean html JS:
        html_js_cleaned = clean_and_minify_html(tool_html_js['html_js'])
    except ParserError:
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
    # Create a dict with the first year of the each tool.
    dict_web_year = {}
    for tool in tools_year:
        if tool['web']['homepage'] in dict_web_year.keys():
            if dict_web_year[tool['web']['homepage']] > tool['year']:
                dict_web_year[tool['web']['homepage']] = tool['year']
        else:
            dict_web_year[tool['web']['homepage']] = tool['year']
    return dict_web_year

def match_websites_add_year(dict_website_year, df):
    df = df.copy()
    df["year"] = ""
    # Match ['first_url'] and add the column fill the column year:
    for i, tool in df.iterrows():
        if tool['first_url'] in dict_website_year.keys():
            df['year'][i] = dict_website_year[tool['first_url']]
    return df

def main(arguments):
    # Open the manifest file from scrapycrawler.
    manifest = open_json(arguments.path_i_file_manifest)

    print(f"INFO: {len(manifest['tools_ok'])} are from Scrapy.")
    # Create dataframe from tools
    df_tools = create_dataframe(manifest['tools_ok'])

    # Calculated percentage of change
    print("INFO: Starting the calculation of the percentage of change.. \nESTIMATED TIME: 12min")
    df_tools_percentages = building_df_with_percentages(df_tools, arguments)

    # Clean dataframe from null values (websites down)
    df_cleaned = cleaning_df(df_tools_percentages)

    # Open file of tools matched with his year of publication
    tools_year = open_json(arguments.path_i_file_tools_pub_year)

    # Create a dict of website and the first year of that website.
    dict_website_year = create_dict_website_minimum_year(tools_year)

    # Add the column year to dataframe and match websites
    final_df_year_websites = match_websites_add_year(dict_website_year, df_cleaned)

    final_df_year_websites.to_json("final_1", orient="records")

    final_df_year_websites.to_json(
        f"{arguments.path_o_directory_data}/{arguments.o_filename}", orient="records")


if __name__ == "__main__":

    # Instance of the class ArgumentParser:
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Analysis of websites to determine the percentage of change between HTML with JS and HTMLs without JS.")

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
        default="../mastercrawlerTFG/output_data/manifest_tools.json",
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
        help="Name of the output directory for the output data. Default: output_data_website_analysis. "
    )

    # # Output filename of stadistics
    parser.add_argument(
        '-o_filename',
        type=str,
        metavar="",
        default="final_df_years_percentages.json",
        help="Name of the output filename of this package. Default: final_df_years_percentages.json "
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path_o_directory_data):
        os.mkdir(args.path_o_directory_data)

    main(args)
