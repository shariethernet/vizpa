import csv
import pandas as pd
import numpy as np
import os
import plotly.express as px
import argparse

MIN_DEPTH =10
MIN_AREA = -1

def create_directory_if_not_exists(file_path):
    directory = os.path.dirname(file_path)
    #print("Checking if directory exists: " + directory)
    if not os.path.exists(directory):
        #print("Creating directory: " + directory)
        os.makedirs(directory)

def create_dir_if_dir_not_exists(dir_path):
    if not os.path.exists(dir_path):
        #print("Creating directory: " + dir_path)
        os.makedirs(dir_path)
"""
report_area -nosplit -hierarchy -levels <level_value>
report_power -nosplit -hierarchy -levels <level_value>
"""


def write_area_csv(area_rpt_path, csv_out_path, min_depth, min_area):
    print("============ Parsing Area reports and writing csv =================")
    start_parsing = False
    data = []
    top_module_detect = False
    top_module = ""

    with open(area_rpt_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Hierarchical cell'):
                start_parsing = True
                # Skip two lines
                next(file)
                next(file)
                # Go to the next line in the loop. No need to do anything again with the header line
                continue

            if start_parsing:
                #print(line)
                #Skip 2 lines
                if line.startswith('------'):
                    start_parsing = False
                    continue

                cells = line.split()
                hierarchical_cell = cells[0]
                absolute_total_area = (float(cells[1]))
                percent_total = cells[2]
                cell_hier = cells[0].split('/')
                indent = len(cell_hier) - 1
                leaf_cell = cell_hier[-1]
                if top_module_detect == False:
                    top_module = leaf_cell
                    top_module_detect = True
                    continue
                
                parent_cell = cell_hier[-2] if len(cell_hier) >= 2 else top_module
                unique_id = leaf_cell+"_"+str(indent)+"_"+str(absolute_total_area)
                if(indent < min_depth and int(float(absolute_total_area)) > min_area):
                    data.append({"hierarchy":hierarchical_cell,
                                 "absolute_total_area":absolute_total_area, 
                                "percent_area_total":percent_total, 
                                "indent":indent, 
                                "leaf_cell":leaf_cell, 
                                "parent":parent_cell, 
                                "unique_id":unique_id})
            


    keys = data[0].keys()
    with open(csv_out_path , 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    return top_module

def write_power_csv( power_rpt_path, csv_out_path, min_depth, pp_report = False):
    print("============ Parsing power reports and writing csv =================")
    start_parsing = False
    data = []
    top_module_detect = False
    top_module = ""
    lastindent = -1
    lastinstance = ""
    parent = ""
    parentarray = []

    with open(power_rpt_path, 'r') as file:
        for line in file:
            #line = line.strip()
            if line.startswith('Hierarchy'):
                start_parsing = True
                # Skip one line
                next(file)
                # Go to the next line in the loop. No need to do anything again with the header line
                continue

            if start_parsing:
                #print(line)
                #Skip 2 lines
                if line.startswith('------'):
                    start_parsing = False
                    continue
                
                
                cells = line.split()
                if cells[0] == "1":
                    continue
                indent = int((len(line) - len(line.lstrip()))/2)
                leaf_cell = cells[0]
                if(indent > lastindent):
                    parentarray.append(lastinstance)
                    parent = lastinstance
                elif(indent < lastindent):
                    while(len(parentarray) > (indent+1)):
                        tmp = parentarray.pop()
                    parent = parentarray[-1]
                parent_array_2 =  parentarray[2:] if indent !=1 else parentarray[2:]
                hierarchy = "/".join(parent_array_2)+"/"+leaf_cell if len(parent_array_2) != 0 else leaf_cell
                lastinstance = leaf_cell
                if top_module_detect == False:
                    top_module = cells[0]
                    top_module_detect = True
                    continue
                lastindent = indent
                if pp_report is False:
                    switching_power = float(cells[2]) if "N/A" not in cells[2] else 0 
                    internal_power = float(cells[3]) if "N/A" not in cells[3] else 0
                    leakage_power = float(cells[4]) if "N/A" not in cells[4] else 0
                    total_power = float(cells[5]) if "N/A" not in cells[5] else 0
                    percentage = float(cells[6]) if "N/A" not in cells[6] else 0
                else:
                    switching_power = float(cells[3]) if "N/A" not in cells[3] else 0 
                    internal_power = float(cells[2]) if "N/A" not in cells[2] else 0
                    leakage_power = float(cells[4]) if "N/A" not in cells[4] else 0
                    total_power = float(cells[-2]) if "N/A" not in cells[-2] else 0
                    percentage = float(cells[-1]) if "N/A" not in cells[-1] else 0
       

                unique_id = leaf_cell+"_"+str(indent)+"_"+str(total_power)
                if(indent < min_depth ):
                    data.append({"parent":parent,
                                "hierarchy":hierarchy, 
                                "indent":indent, 
                                "leaf_cell":leaf_cell, 
                                "switching_power":switching_power, 
                                "internal_power":internal_power, 
                                "leakage_power":leakage_power,
                                "total_power":total_power,
                                "percent_power_total":percentage,
                                "unique_id":unique_id})
            


    keys = data[0].keys()
    with open(csv_out_path , 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    return top_module

def consolidate_area_power_csv(area_csv_path, power_csv_path, csv_out_path):
    print("============ Mapping hierarchies in area and power reports and consolidating csv =================")
    area_df = pd.read_csv(area_csv_path)
    power_df = pd.read_csv(power_csv_path)
    common_cols = list(set(area_df.columns) & set(power_df.columns))
    merged_df = pd.merge(area_df, power_df[['hierarchy','switching_power','internal_power','leakage_power','total_power','percent_power_total']], how='outer', on='hierarchy')
    merged_df.to_csv(csv_out_path, index=False)
    

def create_area_treemap(csv_path, top_module, html_path):
    df = pd.read_csv(csv_path)
    print("============ Generating Area treemap =================")
    title = "Area Viz for Top module: " + top_module
    fig = px.treemap(df, parents='parent', names= 'leaf_cell',title=title, values='absolute_total_area',  branchvalues='total')
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig.show()
    fig.write_html(html_path)

def create_power_treemap(csv_path, top_module,html_path, metric="total_power"):
    df=pd.read_csv(csv_path)
    print("============ Generating Power heatmap =================")
    title = "Power Viz for Top module: " + top_module
    fig = px.treemap(df, parents='parent', names= 'leaf_cell',title=title, values='absolute_total_area', color=metric,  branchvalues='total')
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig.show()
    fig.write_html(html_path)
def main():
    header = """
===========================================================
██    ██ ██ ███████ ██████   █████  
██    ██ ██    ███  ██   ██ ██   ██ 
██    ██ ██   ███   ██████  ███████ 
 ██  ██  ██  ███    ██      ██   ██ 
  ████   ██ ███████ ██      ██   ██ 
============================================================                                    
A Framework to VIZualize Power and Area of a RTL Design         
Supports: Synopsys DC and Synopsys PrimeTime Reports  
============================================================                         
"""

    print(header)
    parser = argparse.ArgumentParser(description = "VIZPA - A Framework to VIZualize Power and Area of a RTL Design. Supports Synopsys DC and PTPX Reports")
    parser.add_argument('-a','--area',type=str,help="Path to the area report [default: \"area.rpt\"]", default = "area.rpt")
    parser.add_argument('-p','--power',type=str,help = "Path to the power report to generate power heatmap also. When not specified power heat map will not be generated", default = None)
    parser.add_argument('-o','--output_dir',type=str, help = "Specify the output directory for the generated files [default: \"out\"]", default ="out")
    parser.add_argument('-md','--max_depth', type=int, help = "Specify the maximum depth of the hierarchy [default:10]", default=10)
    parser.add_argument('-ma','--min_area', type=int, help = "Specify the minimum area to be considered for the heatmap [default:10]", default=10)
    parser.add_argument('-ptpx','--ptpx', action="store_true", help = "Specify if the power report is a PTPX report [default:False]", default=False)
    parser.add_argument('-pm','--power_metric', type=str, help = "Specify the power metric to be used for the heatmap [default:percent_power_total]", default="percent_power_total")
    args = parser.parse_args()

    area_rpt_path = args.area
    power_rpt_path = args.power
    
    out_dir = args.output_dir
    create_dir_if_dir_not_exists(out_dir)

    max_depth = args.max_depth
    min_area = args.min_area

    csv_area_out_path = os.path.join(out_dir,"area.csv")
    csv_power_out_path = os.path.join(out_dir,"power.csv")
    csv_consolidated_path = os.path.join(out_dir,"consolidated.csv")
    area_html_path = os.path.join(out_dir,"area.html")
    power_html_path = os.path.join(out_dir,"power.html")

    #area_rpt_path = "/home/local/nu/shg/area_power_viz/data/reportarea.rpt"
    #power_rpt_path = "/home/local/nu/shg/area_power_viz/data/reportpower.rpt"
    #pp_power_rpt_path = "/home/local/nu/shg/area_power_viz/data/pwr_cell.rpt"
    #csv_area_out_path = "/home/local/nu/shg/area_power_viz/out/area.csv"
    #csv_power_out_path = "/home/local/nu/shg/area_power_viz/out/power.csv"
    #csv_consolidated_path = "/home/local/nu/shg/area_power_viz/out/consolidated.csv"
    #area_html_path = "/home/local/nu/shg/area_power_viz/out/area.html" 
    #power_html_path = "/home/local/nu/shg/area_power_viz/out/power.html"
    #create_directory_if_not_exists(csv_area_out_path)

    top_module = write_area_csv(area_rpt_path, csv_area_out_path, min_depth=max_depth, min_area=min_area)
    create_area_treemap(csv_area_out_path, top_module, area_html_path)
    if args.power is not None:
        write_power_csv( power_rpt_path, csv_power_out_path, min_depth=max_depth, pp_report=args.ptpx)
        consolidate_area_power_csv(csv_area_out_path, csv_power_out_path, csv_consolidated_path)
        create_power_treemap(csv_consolidated_path, top_module, power_html_path, metric=args.power_metric)

if __name__ == "__main__":
    main()