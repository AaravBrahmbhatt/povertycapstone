import csv
import random
from bokeh.plotting import figure, show
from bokeh.models import HoverTool
from bokeh.layouts import column

f = open("poverty.csv", "r", errors = "ignore")

header = ["Year", "ID", "Name", "Poverty Universe", "Number in Poverty", "90% Confidence Interval", "Percent in Poverty", "90% Confidence Interval"]

states = {}

reader = csv.reader(f)

f.readline()

for line in reader:
    stateName = line[2].strip()
    percentPoverty = float(line[6])
    year = int(line[0])

    if stateName not in states:
        states[stateName] = []
    stateInfo = (year, percentPoverty)
    states[stateName].append(stateInfo)

f.close()
#######################################################
wagesData = []
p = open("poverty_level_wages.csv", "r", errors="ignore")

header2 = ["year", "annual_poverty-level_wage", "hourly_poverty-level_wage", "0-75%_of_poverty_wages", "75-100%_of_poverty_wages,share_below_poverty_wages", "100-125%_of_poverty_wages", "125-200%_of_poverty_wages", "200-300%_of_poverty_wages", "300%+_of_poverty_wages", "men_0-75%_of_poverty_wages", "men_75-100%_of_poverty_wages", "men_share_below_poverty_wages", "men_100-125%_of_poverty_wages", "men_125-200%_of_poverty_wages", "men_200-300%_of_poverty_wages", "men_300%+_of_poverty_wages", "women_0-75%_of_poverty_wages", "women_75-100%_of_poverty_wages", "women_share_below_poverty_wages", "women_100-125%_of_poverty_wages", "women_125-200%_of_poverty_wages", "women_200-300%_of_poverty_wages", "women_300%+_of_poverty_wages", "white_share_below_poverty_wages", "white_men_share_below_poverty_wages", "white_women_share_below_poverty_wages", "black_share_below_poverty_wages", "black_men_share_below_poverty_wages","black_women_share_below_poverty_wages","hispanic_share_below_poverty_wages","hispanic_men_share_below_poverty_wages","hispanic_women_share_below_poverty_wages"]


reader2 = csv.reader(p)
p.readline()

for line in reader2:
    year2 = int(line[0])
    annualWage = float(line[1])
    wagesData.append((year2, annualWage))

p.close()

#BOKEH1
f = figure(width = 1500, height = 1300, x_range=(2011, 2022), y_range=(6, 25), title="Poverty Rates by State", x_axis_label="Year", y_axis_label="Poverty Rate (%)", x_minor_ticks = 2, background_fill_color = "black")
f.background_fill_alpha = 0.75
f.xgrid.visible = False
f.ygrid.visible = False

hover = HoverTool()
hover.tooltips = [ ("Year", "@x"), ("Poverty Rate (%)", "@y")]
f.add_tools(hover)


for state in states:

    def yearData(data):
        return data[0]
    
    years = []
    povertyRates = []

    states[state].sort(key=yearData)


    for data in states[state]:
        years.append(data[0])
        povertyRates.append(data[1])
    
    col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    
    f.line(years, povertyRates, color=col, line_width=2, legend_label=state)


f.legend.location = "top_right"
f.legend.orientation = "vertical"
f.legend.background_fill_alpha = 0.8


#BOKEH2
yearData = []
annualWages = []

for data in wagesData:

    yearData.append(data[0])
    
    annualWages.append(data[1])



p = figure(width = 1500, height = 1300, x_range = (1972,2023), title="Annual Poverty Wages Over Time In America", x_axis_label="Year", y_axis_label="Annual Wage", x_minor_ticks = 2, background_fill_color = "black")
p.vbar(x=yearData, top=annualWages, width=0.9, color="white")

p.y_range.start = 0

hover2 = HoverTool()
hover2.tooltips = [("Year", "@x"), ("Annual Wage","$"+"@top")]
p.add_tools(hover2)


layout = column(f, p)

show(layout)
