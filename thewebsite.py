from flask import Flask, render_template, url_for, request



app=Flask(__name__)

@app.route('/plot/', methods=['POST', 'GET'])
def plot():
    from pandas_datareader import data
    import pandas as pd
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.models.annotations import Title
    from bokeh.embed import components
    from bokeh.resources import CDN


    if request.method == "POST":
        invar = request.form.get("stock_symbol")
    elif type == None:
        invar = "GOOG"
    else:
        invar = "GOOG"

    #start=datetime.datetime(start_year, start_month, start_day)
    #end=datetime.datetime(end_year, end_month, end_day)


    if request.method == "POST":
        start12 = request.form.get("Graph_start")
        str_yr = (start12[0:4])
        str_mnt = (start12[5:7])
        str_dy = (start12[8:10])
        start_year = int(str_yr)
        start_month = int(str_mnt)
        start_day = int(str_dy)
        start=datetime.datetime(start_year, start_month, start_day)
        print(start12)
        print(type(start12))
    elif type == None:
        start=datetime.datetime(2015, 12, 1)
    else:
        start=datetime.datetime(2015, 12, 1)

    #2020-05-06
    if request.method == "POST":
        end12 = request.form.get("Graph_end")
        end_yr=(end12[0:4])
        end_mnt=(end12[5:7])
        end_dy=(end12[8:10])
        end_year = int(end_yr)
        end_month = int(end_mnt)
        end_day = int(end_dy)
        end=datetime.datetime(end_year, end_month, end_day)
        print(end12)
        print(type(end12))
    elif type == None:
        end=datetime.datetime(2016, 1, 10)
    else:
        end=datetime.datetime(2016, 1, 10)

    #start = datetime.datetime(request.form['startT'], '%d-%m-%Y')

    #start=datetime.datetime(start_year, start_month, start_day)
    #end=datetime.datetime(end_year, end_month, end_day)

    #invar = "GOOG"

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
    df



    p=figure(x_axis_type="datetime", width=1000, height=300, sizing_mode="scale_width")
    p.title=Title(text="Candlestick Chart")
    p.grid.grid_line_alpha=0.3


    hours_12=12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color="Black")

    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"],
           hours_12, df.Height[df.Status=="Increase"], fill_color="#CCFFFF", line_color="black")

    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"],
           hours_12, df.Height[df.Status=="Decrease"], fill_color="#FF3333", line_color="black")


    theplot, div1 = components(p)
    cdn_js=CDN.js_files[0]

    return render_template("plot.html",
    theplot=theplot,
    div1=div1,
    cdn_js=cdn_js)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def first_page():
    return render_template("content.html")

@app.route('/plot/', methods=['Stock_symbol'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

if __name__=="__main__":
    app.run(debug=True)
