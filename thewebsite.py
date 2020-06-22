from flask import Flask, render_template, url_for, request, send_file
#depen for web stock graph
from pandas_datareader import data
import pandas as pd
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.annotations import Title
from bokeh.models import HoverTool
from bokeh.embed import components
from bokeh.resources import CDN

#dependencies for webscraping
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


app=Flask(__name__)

@app.route('/plot/', methods=['POST', 'GET'])
def plot():

    if request.method == "POST":
        invar = request.form.get("stock_symbol")
    elif type == None:
        invar = "GOOG"
    else:
        invar = "GOOG"

    if request.method == "POST":
        start12 = request.form.get("Graph_start")
        #todo: fix this section to make it cleaner
        str_yr = int(start12[0:4])
        str_mnt = int(start12[5:7])
        str_dy = int(start12[8:10])
        start=datetime(str_yr, str_mnt, str_dy)
        #print(start12)
        #print(type(start12))
    elif type == None:
        start=datetime(2015, 12, 1)
    else:
        start=datetime(2015, 12, 1)

    if request.method == "POST":
        end12 = request.form.get("Graph_end")
        end_yr = int(end12[0:4])
        end_mnt = int(end12[5:7])
        end_dy = int(end12[8:10])
        end=datetime(end_yr, end_mnt, end_dy)
        #print(end12)
        #print(type(end12))
    elif type == None:
        end=datetime(2016, 1, 10)
    else:
        end=datetime(2016, 1, 10)

    df=data.DataReader(name=invar, data_source="yahoo", start=start, end=end)

    def incr_decr(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"]=[incr_decr(c,o) for c, o in zip(df.Close, df.Open)]

    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)


    p=figure(x_axis_type="datetime", width=1000, height=300, sizing_mode="scale_width")
    p.title=Title(text="Candlestick Stock Chart")
    p.grid.grid_line_alpha=0.3


    data_source_increase = ColumnDataSource(df[df.Status=='Increase'])
    data_source_decrease = ColumnDataSource(df[df.Status=='Decrease'])

    hours_12=12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color="Black")

    p.rect('Date', 'Middle', hours_12, 'Height', fill_color="#CCFFFF",
     line_color="black", legend_label="Increase", name ='Increase',source=data_source_increase)

    p.rect('Date', 'Middle', hours_12, 'Height', fill_color="#FF3333",
     line_color="black", legend_label="Decrease", name ='Decrease', source=data_source_decrease)

    p.legend.location = 'bottom_left'
    hover = HoverTool(names=["Increase","Decrease"],
     tooltips=[('Open', '@Open{0.00}'), ('Close', '@Close{0.00}'),
      ('High','@High{0.00}'), ('Low','@Low{0.00}')])
    p.add_tools(hover)

    theplot, div1 = components(p)
    cdn_js=CDN.js_files[0]

    return render_template("plot.html",
    theplot=theplot,
    div1=div1,
    cdn_js=cdn_js)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/etsydata/', methods =["POST", "GET"])
def etsy_data():
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from datetime import datetime

    if request.method == "POST":
        shop_name = request.form.get("shop_name")

        shop_name=str(shop_name)

        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        URL = "https://www.etsy.com/uk/shop/"+shop_name

        r=requests.get("https://www.etsy.com/uk/shop/"+shop_name, headers=headers)
        c=r.content
        soup = BeautifulSoup(c, 'html.parser')
        base_url = "https://www.etsy.com/uk/shop/"+shop_name+"?page="

        l=[]
        pg_nr=soup.find_all("p", {"class": "wt-action-group__item"})[0].text
        page_nr=str(pg_nr)[-2:]
        for page in range(1,(int(page_nr)+1)):
            #print(base_url+str(page)+"#items")
            r = requests.get(base_url+str(page)+"#items", headers=headers)
            c = r.content
            soup = BeautifulSoup(c, 'html.parser')
            all = soup.find_all("a", {"class":"display-inline-block listing-link"})
            #basket=soup.find_all("div", {"class":"text-danger text-body-smaller"})
            for item in all:
                d={}
                try:
                    d["Product_Name"]=item.find_all("h3")[0].text.replace("\n", "").replace(" ", "")
                except:
                    d["Product_Name"]=None
                try:
                    d["Product_Price"]=item.find_all("span", {"class": "currency-value"})[0].text
                except:
                    d["Product_Price"]=None
                try:
                    d["Item_Status"]=item.find_all("div", {"class": "text-danger text-body-smaller"})[0].text.replace("\n", "")
                except:
                    d["Item_Status"]=None
                l.append(d)
        df=pd.DataFrame(l)
        df
        date=((str(datetime.now())[:10]) + " " + (str(datetime.now())[11:13]) + "-" + (str(datetime.now())[14:16]))
        global filename
        filename=(shop_name + date +".csv")
        df.to_csv(filename)
        return render_template("etsy_data.html", text="Please download your spreadsheet", btn="download.html" )
    else:
        return render_template("etsy_data.html")

@app.route("/download-file/")
def download():
    print(filename)
    print(type(filename))
    return send_file(filename_or_fp=filename, attachment_filename=filename, mimetype="csv", as_attachment=True)



if __name__=="__main__":
    app.run(debug=True)
    #when deployed change debug to False
