from utils import *
import os
import pandas as pd

list_htmls_js = os.listdir("../seleniumCrawler/htmls_js")
df = pd.DataFrame(list_htmls_js, columns=['filename'])
df['final_url'] = ""
df['domain'] = ""
df['percentage_of_change'] = ""

#Log for catching exceptions during the creation of the new dataframe:
logf = open("download.log", "w")

#Replace df with the corrresponding values and get percentage of change:
for i, t in enumerate(df.iterrows()):
    try:
        final_url, domain, percentage_of_change = extract_tool_from_json_and_parse(t[1].filename)
    except Exception as e:
        logf.write(f"Failed in tool {str(t)}: {str(e)}\n\n")
        continue
    df.loc[i, 'final_url'] = final_url
    df.loc[i, 'domain'] = domain
    df.loc[i, 'percentage_of_change'] = percentage_of_change

#Replace null values and drop them and get the new dataframe with only dynamic sites:
df.replace("", float("NaN"), inplace=True)
df.dropna(subset = ["percentage_of_change"], inplace=True)
df_dynamic = df[df['percentage_of_change'] > 4]

#Safe all dynamic percentages about websites:
with open("output_data/all_dynamic_percentages.json", 'w') as f:
    json.dump([{'dynamic_percentages' : df_dynamic['percentage_of_change'].tolist()}], f)

#Get classification about domains:
path_json_file_domains = "../mastercrawlerTFG/mastercrawler/output_data/primary_classifcation_domains.json"
with open(path_json_file_domains, "r") as l:
            group_domains = json.load(l)

#Extract specific percentage of each domain:
percentages_all_domain_classification = []
for t in group_domains:
    name_grupation = list(t.keys())[0]
    list_names_grupation = extract_value_from_list_of_dicts(group_domains, name_grupation)
    list_domains_of_a_group = []
    for domain in list_names_grupation:
        df_extraction = df_dynamic[df_dynamic['domain'] == domain]
        item_domain = {domain : df_extraction['percentage_of_change'].tolist()}
        list_domains_of_a_group.append(item_domain)
    item_groupation = {name_grupation : list_domains_of_a_group}    
    percentages_all_domain_classification.append(item_groupation)
     
#Save all the percentages of ecah domain to a json file:
with open("output_data/dynamic_percentages_domains.json", 'w') as p:
    json.dump([{'dynamic_percentages' : percentages_all_domain_classification}], p)