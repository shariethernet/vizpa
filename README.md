# VIZPA
```
██    ██ ██ ███████ ██████   █████  
██    ██ ██    ███  ██   ██ ██   ██ 
██    ██ ██   ███   ██████  ███████ 
 ██  ██  ██  ███    ██      ██   ██ 
  ████   ██ ███████ ██      ██   ██ 
```
 - VIZpa is a framework to quickly visualize the area of a synthesized RTL design as a treemap, and the power (probablistic/vector-based) of an RTL design as heatmap on the treemap

- VIZpa currently supports
    - Area reports: Synopsys Design Compiler
    - Power reports: Synopsys DesignCompiler, Synopsys PrimeTime/PrimePower

## Generating Area reports

Use the below command to generate hierarchical area report from Synopsys Design Compiler

```report_area -nosplit -hierarchy ```

## Generating Power reports

Use the below command to generate hierarchical power reports

- Synopsys Design Compiler

    ```report_power -nosplit -hierarchy```

- Synopsys PrimeTime/PrimePower

    ```report_power -nosplit -verbose -cell_power -hierarchy```

## Running the tool

### Tool Options

To view all the options of the tool run 
```python3 vizpa.py -h```

```
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

usage: vizpa.py [-h] [-a AREA] [-p POWER] [-o OUTPUT_DIR] [-md MAX_DEPTH] [-ma MIN_AREA] [-ptpx] [-pm POWER_METRIC]

VIZPA - A Framework to VIZualize Power and Area of a RTL Design. Supports Synopsys DC and PTPX Reports

optional arguments:
  -h, --help            show this help message and exit
  -a AREA, --area AREA  Path to the area report [default: "area.rpt"]
  -p POWER, --power POWER
                        Path to the power report to generate power heatmap also. When not specified power heat map will not be generated
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Specify the output directory for the generated files [default: "out"]
  -md MAX_DEPTH, --max_depth MAX_DEPTH
                        Specify the maximum depth of the hierarchy [default:10]
  -ma MIN_AREA, --min_area MIN_AREA
                        Specify the minimum area to be considered for the heatmap [default:10]
  -ptpx, --ptpx         Specify if the power report is a PTPX report [default:False]
  -pm POWER_METRIC, --power_metric POWER_METRIC
                        Specify the power metric to be used for the heatmap [default:percent_power_total]
```

### Example

A reference, [area report](data/reportarea.rpt) from Synopsys DC, [power report](data/report)
from Synopsys DC and [power report](data/pwr_cell.rpt) from Synopsys PTPX are included in the [data](data/) directory.

To invoke VIZPA on these reports, the below command is used

#### Generating Area Treemap (DC) and Power Heatmap (PTPX) 
```
python3 vizpa.py -a "data/reportarea.rpt" -p "data/pwr_cell.rpt" -md=10 -ma=-1 -ptpx -o=out 
```

This is used to generate both the area treemap and also the power heatmap on the treemap from primepower report (note the usage of -ptpx flag).

#### Generating Area Treemap (DC) and Power Heatmap (DC)
Alternatively, if you want the power report to be generated from the reports generated by Synopsys DC (Probabilistic power analysis) use the below command

```
python3 vizpa.py -a "data/reportarea.rpt" -p "data/reportpower.rpt" -md=10 -ma=-1 -ptpx -o=out 
```

#### Generating Area Treemap (DC) only

One can also just generate the area treemap using the below command

```
python3 vizpa.py -a "data/reportarea.rpt" -md=10 -ma=-1 o=out 
```

### Area Treemap

![Area Treemap](docs/imgs/area_treemap.gif)

### Power Heatmap on a Treemap
![Power Heatmap](docs/imgs/power_heattreemap.gif)

### Extending the tool

Adding support to other tools like Cadence Joules, Cadence Genus etc., would be to just implement the parser to parse the hierarchical area and power reports generated by the tools and fitting into the pandas dataframe used by vizpa.

