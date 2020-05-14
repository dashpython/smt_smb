import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
from dash.dependencies import Input, Output, State
import paho.mqtt.client as mqtt
import time
import pandas as pd
import sqlite3
import os
import pathlib
import base64
from six.moves.urllib.parse import quote
from sqlalchemy import create_engine
from datetime import datetime,timedelta
import unicodedata
import dash_daq as daq
from flask_mqtt import Mqtt
from flask_socketio import SocketIO


server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
db_URI = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
engine = create_engine(db_URI)
class User(db.Model):
    __tablename__ = 'datatable'

    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.String(26))
    devId = db.Column(db.String(15))
    SPA = db.Column(db.String(10))
    TA = db.Column(db.String(10))

    def __repr__(self):
        return '<User %r %r  %r %r>' % (self.stamp, self.devId, self.SPA, self.TA)

class smb(db.Model):
    __tablename__ = 'smbtable'

    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.String(26))
    devId = db.Column(db.String(15))
    str1 = db.Column(db.String(10))
    str2 = db.Column(db.String(10))
    str3 = db.Column(db.String(10))
    str4 = db.Column(db.String(10))
    str5 = db.Column(db.String(10))
    str6 = db.Column(db.String(10))
    str7 = db.Column(db.String(10))
    str8 = db.Column(db.String(10))
    str9 = db.Column(db.String(10))
    str10 = db.Column(db.String(10))
    str11 = db.Column(db.String(10))
    str12 = db.Column(db.String(10))
    str13 = db.Column(db.String(10))
    vol1 = db.Column(db.String(10))
    vol2 = db.Column(db.String(10))
    vol3 = db.Column(db.String(10))
    vol4 = db.Column(db.String(10))
    vol5 = db.Column(db.String(10))
    vol6 = db.Column(db.String(10))
    vol7 = db.Column(db.String(10))
    vol8 = db.Column(db.String(10))
    vol9 = db.Column(db.String(10))
    vol10 = db.Column(db.String(10))
    vol11 = db.Column(db.String(10))
    vol12 = db.Column(db.String(10))
    vol13 = db.Column(db.String(10))
    temp = db.Column(db.String(10))
    stravg=db.Column(db.Float)
    volavg=db.Column(db.Float)
    poweravg =db.Column(db.Float)

    def __repr__(self):
        return '<User %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r>' % (self.stamp, self.devId, self.str1, self.str2, self.str3, self.str4, self.str5, self.str6, self.str7, self.str8, self.str9,
                self.str10, self.str11, self.str12, self.str13, self.vol1, self.vol2, self.vol3, self.vol4, self.vol5, self.vol6, self.vol7, self.vol8, self.vol9, self.vol10, self.vol11, self.vol12, self.vol13, self.temp, self.stravg, self.volavg, self.poweravg)

db.create_all()

def on_connect(client, userdata, flags, rc):
    print("Connected!", rc)
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))
def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_publish(client, userdata, mid):
    print("Publish:", client)

def on_log(client, userdata, level, buf):
    print("log:", buf)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

messagelist=[]
messagelist2=[]
smbdict={}
teststr=""
a =[]
b= []
c = []
e = []
devicetime=[]
d={}
def on_message(client, userdata, message):
    data={}
    data1={}
    global d
    payload = str(message.payload.decode("utf-8"))#+" "
    print("payload=",payload,len(payload))
    print("payload[:4]",payload[:4],len(payload))
    #messagelist=
    if payload[:4]=="Dev:":# and len(payload)!=45:
        ind=payload.index(",Time")
        #ind=ind+25
        print("index devid=",ind)
        print("payload[ind+25:]",payload[ind+25:],len(payload))
        teststr=payload[:ind]+payload[ind+25:]
        messagelist.append(payload)
        if len(messagelist)>4:
            messagelist.remove(messagelist[0])
        print("smbmessagelist=",messagelist)
        data = dict(x.split(":") for x in teststr.split(","))
        data['Time']=payload[ind+21:ind+25]+"-"+payload[ind+18:ind+20]+"-"+payload[ind+15:ind+17]+"T"+payload[ind+6:ind+14]+".000000"
        print("smb data=",data)
    print("pay data1=",payload[:6])

    if payload[:6]=="DevId:":
        print("hi data1")
        data1 = dict(x.split(":") for x in payload.split(","))
        messagelist2.append(payload)
        if len(messagelist2)>4:
            messagelist2.remove(messagelist2[0])
        print("messagelist2=",messagelist2)
        dp = ", ".join(messagelist2)
        print("dp=",dp)
        dp2 = dict(x.split(":") for x in dp.split(","))
        print("dp2=",dp2)
        keylist=['SPA','TA','MOTOR','MODE']
        for k,v in dp2.items():
            for i in keylist:
                if i==k:
                    d[k] = v
        print("d=",d)
        if "SPA" in d:
            a.append(d["SPA"])
        if len(a)>1:
            a.remove(a[0])
        if "TA" in d:
            b.append(d["TA"])
        if len(b)>1:
            b.remove(b[0])
        if "MODE" in d:
            c.append(d["MODE"])
        if len(c)>1:
            c.remove(c[0])
        if "MOTOR" in d:
            e.append(d["MOTOR"])
        if len(e)>1:
            e.remove(e[0])
        print(a)
        print(b)
        print(c)
        print(e)
    print("data=",data1)
    print("smb data=",data)
    print("len dataa=",len(data))
    if (len(data1)==3):
        print("len",len(data1))
        admin = User(stamp=str(datetime.now()+timedelta(minutes=330)),devId=data1['DevId'],SPA=data1['SPA'],TA=data1['TA'])
        db.session.add(admin)
        db.session.commit()
        print("data saved to datatabe")


    elif len(smbdict)==28:
        print("smb dict=",smbdict)
        stravg=0
        stravg=float(smbdict['str1'])+float(smbdict['str2'])+float(smbdict['str3'])+float(smbdict['str4'])+float(smbdict['str5'])+float(smbdict['str6'])+float(smbdict['str7'])+float(smbdict['str8'])+float(smbdict['str9'])+float(smbdict['str10'])+float(smbdict['str11'])+float(smbdict['str12'])+float(smbdict['str13'])
        stravg=float(stravg/13)
        smbdict['stravg']=stravg
        print("smb dict=",smbdict)
        volavg=0
        volavg=float(smbdict['vol1'])+float(smbdict['vol2'])+float(smbdict['vol3'])+float(smbdict['vol4'])+float(smbdict['vol5'])+float(smbdict['vol6'])+float(smbdict['vol7'])+float(smbdict['vol8'])+float(smbdict['vol9'])+float(smbdict['vol10'])+float(smbdict['vol11'])+float(smbdict['vol12'])+float(smbdict['vol13'])
        volavg=float(volavg/13)
        smbdict['volavg']=volavg
        print("smb dict=",smbdict)
        poweravg=0
        poweravg=float((volavg*stravg)/1000)
        smbdict['poweravg']=poweravg
        smbdict['temp']=data['temp']
        print("smb dict=",smbdict)

        smbdata = smb(stamp=smbdict['Time'],devId=smbdict['Dev'],temp=smbdict['temp'],str1=smbdict['str1'],vol1=smbdict['vol1'],str2=smbdict['str2'],vol2=smbdict['vol2'],str3=smbdict['str3'],vol3=smbdict['vol3'],str4=smbdict['str4'],vol4=smbdict['vol4'],str5=smbdict['str5'],vol5=smbdict['vol5'],str6=smbdict['str6'],vol6=smbdict['vol6'],str7=smbdict['str7'],vol7=smbdict['vol7'],
                str8=smbdict['str8'],vol8=smbdict['vol8'],str9=smbdict['str9'],vol9=smbdict['vol9'],str10=smbdict['str10'],vol10=smbdict['vol10'],str11=smbdict['str11'],vol11=smbdict['vol11'],str12=smbdict['str12'],vol12=smbdict['vol12'],str13=smbdict['str13'],vol13=smbdict['vol13'],stravg=smbdict['stravg'],volavg=smbdict['volavg'],poweravg=smbdict['poweravg'])
        db.session.add(smbdata)
        db.session.commit()
        smbdict.clear()

    elif len(data)==4:
        if len(smbdict)==0:
            smbdict.update(data)
        elif (('str2' not in smbdict) and ('str2' in data)):
            smbdict['str2']=data['str2']
            smbdict['vol2']=data['vol2']
        elif (('str3' not in smbdict) and ('str3' in data)):
            smbdict['str3']=data['str3']
            smbdict['vol3']=data['vol3']
        elif (('str4' not in smbdict) and ('str4' in data)):
            smbdict['str4']=data['str4']
            smbdict['vol4']=data['vol4']
        elif (('str5' not in smbdict) and ('str5' in data)):
            smbdict['str5']=data['str5']
            smbdict['vol5']=data['vol5']
        elif (('str6' not in smbdict) and ('str6' in data)):
            smbdict['str6']=data['str6']
            smbdict['vol6']=data['vol6']
        elif (('str7' not in smbdict) and ('str7' in data)):
            smbdict['str7']=data['str7']
            smbdict['vol7']=data['vol7']
        elif (('str8' not in smbdict) and ('str8' in data)):
            smbdict['str8']=data['str8']
            smbdict['vol8']=data['vol8']
        elif (('str9' not in smbdict) and ('str9' in data)):
            smbdict['str9']=data['str9']
            smbdict['vol9']=data['vol9']
        elif (('str10' not in smbdict) and ('str10' in data)):
            smbdict['str10']=data['str10']
            smbdict['vol10']=data['vol10']
        elif (('str11' not in smbdict) and ('str11' in data)):
            smbdict['str11']=data['str11']
            smbdict['vol11']=data['vol11']
            smbdict['str12']=data['str12']
            smbdict['vol12']=data['vol12']
        elif (('str13' not in smbdict) and ('str13' in data)):
            smbdict['str13']=data['str13']
            smbdict['vol13']=data['vol13']

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_connect = on_connect
client.on_message = on_message
time.sleep(1)

subtop="tracker/device/sub"
pubtop="tracker/device/pub"
client.username_pw_set("cbocdpsu", "3_UFu7oaad-8")
client.connect('soldier.cloudmqtt.com', 14035,60)
client.loop_start()
client.subscribe(subtop)
client.loop()

app = dash.Dash(__name__,server=server,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

connection1 = engine
df=pd.read_sql("select * from datatable",connection1)

params =list(df)
print("params=",params)
max_length = len(df)
print("ms=",max_length)

def dropdown_list():
    return html.Div([dbc.DropdownMenu(
        children=[dbc.DropdownMenu(nav=True,in_navbar=True,label="Main Control Room",
                    children=[dbc.DropdownMenuItem(dbc.NavLink("InverterRoom1",href="/"))]),
            dbc.DropdownMenu(nav=True,in_navbar=True,label="Layout",
                children=[dbc.DropdownMenuItem(dbc.NavLink("Layout",href="/layout"))]),
            dbc.DropdownMenu(nav=True,in_navbar=True,label="Trackers",
                    children=[dbc.DropdownMenuItem(dbc.NavLink("Table",href="/tracker")),
                        dbc.DropdownMenuItem(dbc.NavLink("Graph", href='/home',)),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem(dbc.NavLink("Read", href='/read')),
                        dbc.DropdownMenuItem(dbc.NavLink("Control", href='/control')),
                        dbc.DropdownMenuItem(dbc.NavLink("Status", href='/status')),
                        dbc.DropdownMenuItem(dbc.NavLink("Location SetUp", href='/location'))]),
                    dbc.DropdownMenu(nav=True,in_navbar=True,label="SMB's",
                    children=[dbc.DropdownMenuItem(dbc.NavLink("Table",href="/smb")),
                        dbc.DropdownMenuItem(dbc.NavLink("Graph", href='/'))])],
                    label="DashBoard",style={'width':'auto'},className="m-2 2 2 2")])



def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-logo",
                children=[
                    html.Img(src=app.get_asset_url("smarttrack.png"), height="50px")
                ],
            ),
            html.Div(
                id="banner-text",
                children=[
                    html.H5("SMARTTRAK DASHBOARD"),
                ],
            ),
            dropdown_list(),
               
             ],
    )


def build_row():
    return html.Div(
            [
            dcc.Link(
                "PlantView",
                href="/plantview",
                className="tab first",
            ),
            dcc.Link(
                "SLD",
                href="/sld",
                className="tab",
            ),
            dcc.Link(
                "Layout",
                href="/layout",
                className="tab",
            ),
            dcc.Link(
                "Power", href="/power", className="tab"
            ),
            dcc.Link(
                "HT-Panels",
                href="/ht-panels",
                className="tab",
            ),
            dcc.Link(
                "Inverters",
                href="/inverters",
                className="tab",
            ),
            dcc.Link(
                "RMU",
                href="/RMU",
                className="tab",
            ),
            dcc.Link(
                "SMB",
                href="/smb",
                className="tab",
            ),
             dcc.Link(
                "Trackers",
                href="/tracker",
                className="tab",
            ),
             dcc.Link(
                "Alarms",
                href="/alarms",
                className="tab",
            ),


        ],
       id="row-container",className="row all-tabs",
    )
    

def plantview_layout(app):
    # Page layouts
    return html.Div(id="section-container",
            className="row",
            children=[
                html.Div(id="plantview1",className="three columns",
            children=[
                dbc.Card([
                    dbc.CardImg(src=app.get_asset_url("sunpos.png"),top=True,style={'width':'8rem','margin':'1rem 1rem 1rem 1rem'}),],style={'width':'10rem','border':'1px white solid'}),html.Br(),
                html.Div("Radiation Fixed: "),html.Div("Radiation Tilt:"),html.Div("Irradiation Fixed:"),html.Div("Irradiation Tilt:"),html.Div("Ambient Temp:"),html.Div("Module Temp:") ,]),
            html.Div(
                id="plantview2",className="three columns",
                children=[
           dbc.Card([
                    dbc.CardImg(src=app.get_asset_url("solarpower.png"),top=True,style={'width':'8rem','margin':'1rem 1rem 1rem 1rem'}),],style={'width':'10rem','border':'1px white solid'}),html.Br(),
                    html.Div("DC Power: "),html.Div("Max.DC Power:") ]),
                
                 html.Div(
                id="plantview3",className="three columns",
                children=[
           dbc.Card([
                    dbc.CardImg(src=app.get_asset_url("ac.png"),top=True,style={'width':'8rem','margin':'1rem 1rem 1rem 1rem'}),],style={'width':'10rem','border':'1px white solid'}),html.Br(),
                    html.Div("AC Power: "),html.Div("Max.AC Power:"),html.Div("Today Energy:"),html.Div("Total Energy:")  ]),
                                 html.Div(
                id="plantview4",className="three columns",
                children=[
           dbc.Card([
                    dbc.CardImg(src=app.get_asset_url("main-sub.png"),top=True,style={'width':'8rem','margin':'1rem 1rem 1rem 1rem'}),],style={'width':'10rem','border':'1px white solid'}),html.Br(),
                    html.Div("Today IMPORT: "),html.Div("Today EXPORT:"),html.Div("Life IMPORT:"),html.Div("Life EXPORT:")  ]),
                 html.Div(
                id="plantview5",className="three columns",
                children=[
           dbc.Card([
                    dbc.CardImg(src=app.get_asset_url("to220.png"),top=True,style={'width':'8rem','margin':'1rem 1rem 1rem 1rem'}),],style={'width':'10rem','border':'1px white solid'}),]),] )
     
def sld_layout(app):
    return html.Div([html.H3("SLD..........Page on Progress..........",style={'color':'maroon'}),dcc.Link(href='/sld')])

card_1 =  html.Div([dbc.Row([dbc.Col(html.A(dbc.Button("Trackers", id="tracker-button",href="/page-1",color="primary",className="mt 2")),style={"margin-top":"2rem"})])
    ,html.Br(),dbc.Container([dbc.Row([html.H4("TRACKER Devices",style={'color':'red','font-family': 'Open Sans Semi Bold'},className="mr-1")]),
dbc.Row([html.A(html.Button("R1",className="mr-1"),href="/page-2")]),html.Br(),
html.A(html.Button("A1",className="mr-1"),href="/page-2"),
html.A(html.Button("A2",className="mr-1"),href="/page-2"),
html.A(html.Button("A3",className="mr-1"),href="/page-2"),
html.A(html.Button("A4",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("B1",className="mr-1"),href="/page-2"),
html.A(html.Button("B2",className="mr-1"),href="/page-2"),
html.A(html.Button("B3",className="mr-1"),href="/page-2"),
html.A(html.Button("B4",className="mr-1"),href="/page-2"),
html.A(html.Button("B5",className="mr-1"),href="/page-2"),
html.A(html.Button("B6",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("C1",className="mr-1"),href="/page-2"),
html.A(html.Button("C2",className="mr-1"),href="/page-2"),
html.A(html.Button("C3",className="mr-1"),href="/page-2"),
html.A(html.Button("C4",className="mr-1"),href="/page-2"),
html.A(html.Button("C5",className="mr-1"),href="/page-2"),
html.A(html.Button("C6",className="mr-1"),href="/page-2"),
html.A(html.Button("C7",className="mr-1"),href="/page-2"),
html.A(html.Button("C8",className="mr-1"),href="/page-2"),
html.A(html.Button("C9",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("D1",className="mr-1"),href="/page-2"),
html.A(html.Button("D2",className="mr-1"),href="/page-2"),
html.A(html.Button("D3",className="mr-1"),href="/page-2"),
html.A(html.Button("D4",className="mr-1"),href="/page-2"),
html.A(html.Button("D5",className="mr-1"),href="/page-2"),
html.A(html.Button("D6",className="mr-1"),href="/page-2"),
html.A(html.Button("D7",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("E1",className="mr-1"),href="/page-2"),
html.A(html.Button("E2",className="mr-1"),href="/page-2"),
html.A(html.Button("E3",className="mr-1"),href="/page-2"),
html.A(html.Button("E4",className="mr-1"),href="/page-2"),
html.A(html.Button("E5",className="mr-1"),href="/page-2"),
html.A(html.Button("E6",className="mr-1"),href="/page-2"),
html.A(html.Button("E7",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("F1",className="mr-1"),href="/page-2"),
html.A(html.Button("F2",className="mr-1"),href="/page-2"),
html.A(html.Button("F3",className="mr-1"),href="/page-2"),
html.A(html.Button("F4",className="mr-1"),href="/page-2"),
html.A(html.Button("F5",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("G1",className="mr-1"),href="/page-2"),
html.A(html.Button("G2",className="mr-1"),href="/page-2"),
html.A(html.Button("G3",className="mr-1"),href="/page-2"),
html.A(html.Button("G4",className="mr-1"),href="/page-2"),
html.A(html.Button("G5",className="mr-1"),href="/page-2"),
html.A(html.Button("G6",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("H1",className="mr-1"),href="/page-2"),
html.A(html.Button("H2",className="mr-1"),href="/page-2"),
html.A(html.Button("H3",className="mr-1"),href="/page-2"),
html.A(html.Button("H4",className="mr-1"),href="/page-2"),
html.A(html.Button("H5",className="mr-1"),href="/page-2"),
html.A(html.Button("H6",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("I1",className="mr-1"),href="/page-2"),
html.A(html.Button("I2",className="mr-1"),href="/page-2"),
html.A(html.Button("I3",className="mr-1"),href="/page-2"),
html.A(html.Button("I4",className="mr-1"),href="/page-2"),
html.A(html.Button("I5",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("J1",className="mr-1"),href="/page-2"),
html.A(html.Button("J2",className="mr-1"),href="/page-2"),
html.A(html.Button("J3",className="mr-1"),href="/page-2"),
html.A(html.Button("J4",className="mr-1"),href="/page-2"),
html.A(html.Button("J5",className="mr-1"),href="/page-2"),
html.A(html.Button("J6",className="mr-1"),href="/page-2"),html.Br(),
html.A(html.Button("K1",className="mr-1"),href="/page-2"),
html.A(html.Button("K2",className="mr-1"),href="/page-2"),
html.A(html.Button("K3",className="mr-1"),href="/page-2"),
html.A(html.Button("K4",className="mr-1"),href="/page-2"),
html.A(html.Button("K5",className="mr-1"),href="/page-2"),
html.A(html.Button("K6",className="mr-1"),href="/page-2")],style={"border":"2px darkblue solid",'width':'auto',"height":"calc(100vh - 10rem - 1px)"})])

#/*------------------------------------------------------------------------------------------------------------------*/

card_2 = html.Div([dbc.Row([dbc.Col(html.A(dbc.Button("SMB's", id="SMB-button",href="/page-5",color="primary",className="mt 2")),style={"margin-top":"2rem"})])
    ,html.Br(),dbc.Container([dbc.Row([html.H4("SMB Devices",style={'color':'red','font-family': 'Open Sans Semi Bold'},className="mr-1")]),
dbc.Row([html.A(html.Button("G1",className="mr-1"),href="/page-6")]),html.Br(),
html.A(html.Button("A1",className="mr-1"),href="/page-6"),
html.A(html.Button("A2",className="mr-1"),href="/page-6"),
html.A(html.Button("A3",className="mr-1"),href="/page-6"),
html.A(html.Button("A4",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("B1",className="mr-1"),href="/page-6"),
html.A(html.Button("B2",className="mr-1"),href="/page-6"),
html.A(html.Button("B3",className="mr-1"),href="/page-6"),
html.A(html.Button("B4",className="mr-1"),href="/page-6"),
html.A(html.Button("B5",className="mr-1"),href="/page-6"),
html.A(html.Button("B6",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("C1",className="mr-1"),href="/page-6"),
html.A(html.Button("C2",className="mr-1"),href="/page-6"),
html.A(html.Button("C3",className="mr-1"),href="/page-6"),
html.A(html.Button("C4",className="mr-1"),href="/page-6"),
html.A(html.Button("C5",className="mr-1"),href="/page-6"),
html.A(html.Button("C6",className="mr-1"),href="/page-6"),
html.A(html.Button("C7",className="mr-1"),href="/page-6"),
html.A(html.Button("C8",className="mr-1"),href="/page-6"),
html.A(html.Button("C9",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("D1",className="mr-1"),href="/page-6"),
html.A(html.Button("D2",className="mr-1"),href="/page-6"),
html.A(html.Button("D3",className="mr-1"),href="/page-6"),
html.A(html.Button("D4",className="mr-1"),href="/page-6"),
html.A(html.Button("D5",className="mr-1"),href="/page-6"),
html.A(html.Button("D6",className="mr-1"),href="/page-6"),
html.A(html.Button("D7",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("E1",className="mr-1"),href="/page-6"),
html.A(html.Button("E2",className="mr-1"),href="/page-6"),
html.A(html.Button("E3",className="mr-1"),href="/page-6"),
html.A(html.Button("E4",className="mr-1"),href="/page-6"),
html.A(html.Button("E5",className="mr-1"),href="/page-6"),
html.A(html.Button("E6",className="mr-1"),href="/page-6"),
html.A(html.Button("E7",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("F1",className="mr-1"),href="/page-6"),
html.A(html.Button("F2",className="mr-1"),href="/page-6"),
html.A(html.Button("F3",className="mr-1"),href="/page-6"),
html.A(html.Button("F4",className="mr-1"),href="/page-6"),
html.A(html.Button("F5",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("G1",className="mr-1"),href="/page-6"),
html.A(html.Button("G2",className="mr-1"),href="/page-6"),
html.A(html.Button("G3",className="mr-1"),href="/page-6"),
html.A(html.Button("G4",className="mr-1"),href="/page-6"),
html.A(html.Button("G5",className="mr-1"),href="/page-6"),
html.A(html.Button("G6",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("H1",className="mr-1"),href="/page-6"),
html.A(html.Button("H2",className="mr-1"),href="/page-6"),
html.A(html.Button("H3",className="mr-1"),href="/page-6"),
html.A(html.Button("H4",className="mr-1"),href="/page-6"),
html.A(html.Button("H5",className="mr-1"),href="/page-6"),
html.A(html.Button("H6",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("I1",className="mr-1"),href="/page-6"),
html.A(html.Button("I2",className="mr-1"),href="/page-6"),
html.A(html.Button("I3",className="mr-1"),href="/page-6"),
html.A(html.Button("I4",className="mr-1"),href="/page-6"),
html.A(html.Button("I5",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("J1",className="mr-1"),href="/page-6"),
html.A(html.Button("J2",className="mr-1"),href="/page-6"),
html.A(html.Button("J3",className="mr-1"),href="/page-6"),
html.A(html.Button("J4",className="mr-1"),href="/page-6"),
html.A(html.Button("J5",className="mr-1"),href="/page-6"),
html.A(html.Button("J6",className="mr-1"),href="/page-6"),html.Br(),
html.A(html.Button("K1",className="mr-1"),href="/page-6"),
html.A(html.Button("K2",className="mr-1"),href="/page-6"),
html.A(html.Button("K3",className="mr-1"),href="/page-6"),
html.A(html.Button("K4",className="mr-1"),href="/page-6"),
html.A(html.Button("K5",className="mr-1"),href="/page-6"),
html.A(html.Button("K6",className="mr-1"),href="/page-6")],style={"border":"2px darkblue solid",'width':'auto', "height":"calc(100vh - 10rem - 1px)"})])

def layout_layout(app):
    return html.Div([dbc.Row([dbc.Col(card_1),dbc.Col(card_2)]), dcc.Link(href='/layout')])


def power_layout(app):
    return  html.Div([html.H3("POWER...........Page on Progress..........",style={'color':'maroon'}), dcc.Link(href='/power')])

def htpanels_layout(app):
    return html.Div([html.H3("HT-PANELS............Page on Progress..........",style={'color':'maroon'}), dcc.Link(href='/htpanels')])

def inverters_layout(app):
    return html.Div([html.H3("Inverter..............Page on Progress..........",style={'color':'maroon'}), dcc.Link(href='/inverters')])
def RMU_layout(app):
    return html.Div([html.H3("RMU...............Page on Progress..........",style={'color':'maroon'}), dcc.Link(href='/RMU')])


def tablesmb(filtered_df):

    table_header=[html.Thead(html.Tr([html.Th('Id'),html.Th('stamp'),html.Th('devId'),html.Th('str1') ,html.Th('str2'),html.Th('str3') ,html.Th('str4'),html.Th('str5') ,html.Th('str6'),html.Th('str7') ,html.Th('str8'),html.Th('str9') ,html.Th('str10'),html.Th('str11') ,html.Th('str12'),html.Th('str13'),html.Th('vol1'),html.Th('vol2'),html.Th('vol3'),html.Th('vol4'),html.Th('vol5'),html.Th('vol6'),html.Th('vol7'),html.Th('vol8'),html.Th('vol9'),html.Th('vol10'),html.Th('vol11'),html.Th('vol12'),html.Th('vol13'),html.Th('temp')
         ]))]
    table_body=[html.Tbody(html.Tr([html.Td(dev[0]),html.Td(dev[1]),html.A(html.Td(dev[2]),href="/page-6"),html.Td(dev[3]),html.Td(dev[4]),html.Td(dev[5]),html.Td(dev[6]),html.Td(dev[7]),html.Td(dev[8]),html.Td(dev[9]),html.Td(dev[10]),html.Td(dev[11]),html.Td(dev[12]),html.Td(dev[13]),html.Td(dev[14]),html.Td(dev[15]),html.Td(dev[16]),html.Td(dev[17]),html.Td(dev[18]),html.Td(dev[19]),html.Td(dev[20]),html.Td(dev[21]),html.Td(dev[22]),html.Td(dev[23]),html.Td(dev[24]),html.Td(dev[25]),html.Td(dev[26]),html.Td(dev[27]),html.Td(dev[28]),html.Td(dev[29])]))for dev in filtered_df]
    table=dbc.Table(table_header+table_body,bordered=True,responsive=True,striped=True)
    return table


def smb_layout(app):
    return html.Div([html.H3('SMB TABLE DATA',style={'font-style': 'Times New Roman','color':'#FF5733'}),
          html.Br(),
          html.Div([ dbc.Button(html.A(
        "Download CSV",
        id='download-linksmb',
        download="rawtable.csv",href="",target="_blank"),outline=True,color="secondary"),

]), html.Br(),
          dcc.DatePickerRange(
            id='my-date-picker-range2smb',
            min_date_allowed=datetime(1995, 8, 5,1,1,1,1),
            max_date_allowed=datetime.now(),
            initial_visible_month=datetime.now(),
            end_date=datetime.now(),
            start_date=datetime.now()-timedelta(days=1)),
    html.Div(id='output-container-date-picker-range2smb'),
            dcc.Link(href='/page-5'),
            html.Br(),

            html.Div([html.Table(id="live-update-text-smb",className="tiny-header")],style={'maxHeight':"380px","overflowY":"scroll"}),
            ],className="twelve columns")


def table(filtered_df):
    table_header=[html.Thead(html.Tr([html.Th('SERIAL NO.'),html.Th('TIME_STAMP'),html.Th('DEV_ID'),html.Th('SUN ANGLE') ,html.Th('TRACKER ANGLE')]))]
    table_body=[html.Tbody(html.Tr([html.Td(dev[0]),html.Td(dev[1]),html.A(html.Td(dev[2]),href="/page-2"),html.Td(dev[3]),html.Td(dev[4])]))for dev in filtered_df]
    table=dbc.Table(table_header+table_body,bordered=True,hover=True, dark=True,responsive=True,striped=True)
    return table


def tracker_layout(app):
    return html.Div(id="top-container",
        className="row",
        children=[
            html.Div(id="metric-row",className="fourteen columns",
                children=[
                    html.A(html.Button("Home",className="mr-4",style={'backgroundColor':'black','color':'white'}),href="/home"),
    html.A(html.Button("Status",className="mr-4",style={'backgroundColor':'black','color':'white'}),href="/status"),
    html.A(html.Button("Location Setup",className="mr-4",style={'backgroundColor':'black','color':'white'}),href="/location"),
    html.A(html.Button("Control",className="mr-4",style={'backgroundColor':'black','color':'white'}),href="/control"),
    html.A(html.Button("Tracker Table",className="mr-4",style={'backgroundColor':'black','color':'white'}),href="/tracker"),
    html.A(html.Button("Read",className="mr-4",style={'backgroundColor':'black','color':'white'}),href="/read"),]),
                 html.Div(id="metric-header",className="four columns",
                        children=[
                            html.H3('TRACKER TABLE DATA')]),             
                   html.Div(id="metric-header",className="four columns",
                        children=[
                            dbc.Button(html.A(
        "Download CSV",
        id='download-link',
        download="rawtable.csv",href="",target="_blank"),outline=True,color="secondary"),]),
                    html.Br(),
                                       html.Div(id="metric-header",className="four columns",
                        children=[ dcc.DatePickerRange(
            id='my-date-picker-range2',
            min_date_allowed=datetime(1995, 8, 5,1,1,1,1),
            max_date_allowed=datetime.now(),
            initial_visible_month=datetime.now(),
            end_date=datetime.now(),
            start_date=datetime.now()-timedelta(days=1)),
    html.Div(id='output-container-date-picker-range2'),]),
                                                 html.Div(id="metric-table",className="twelve columns",
                                                     children=[html.Table(id="live-update-text",className="tiny-header")],style={'overflowX':'scroll','overflowY':'scroll'}),           
                ])



def home_layout(app):
    return  dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H3('TRACKER SPA VS TIME GRAPH',style={'font-style': 'Times New Roman','color':'#FF5733'}),
                    dcc.Dropdown(id='devices',
                options=[{'label': 'R1', 'value': 'R1'},{'label': 'R2', 'value': 'R2'},{'label': 'R3', 'value': 'R3'},{'label': 'R4', 'value': 'R4'},{'label': 'A1', 'value': 'A1'},{'label': 'A2', 'value': 'A2'},{'label': 'A3', 'value': 'A3'},{'label': 'A4', 'value': 'A4'},{'label': 'B1', 'value': 'B1'},{'label': 'B2', 'value': 'B2'},{'label': 'B3', 'value': 'B3'},{'label': 'B4', 'value': 'B4'},{'label': 'B5', 'value': 'B5'},{'label': 'B6', 'value': 'B6'},{'label': 'C1', 'value': 'C1'},{'label': 'C2', 'value': 'C2'},{'label': 'C3', 'value': 'C3'},{'label': 'C4', 'value': 'C4'},{'label': 'C5', 'value': 'C5'},{'label': 'C6', 'value': 'C6'},{'label': 'C7', 'value': 'C7'},{'label': 'C8', 'value': 'C8'},{'label': 'C9', 'value': 'C9'},{'label': 'D1', 'value': 'D1'},{'label': 'D2', 'value': 'D2'},{'label': 'D3', 'value': 'D3'},{'label': 'D4', 'value': 'D4'},{'label': 'D5', 'value': 'D5'},{'label': 'D6', 'value': 'D6'},{'label': 'D7', 'value': 'D7'},{'label': 'E1', 'value': 'E1'},{'label': 'E2', 'value': 'E2'},{'label': 'E3', 'value': 'E3'},{'label': 'E4', 'value': 'E4'},{'label': 'E5', 'value': 'E5'},{'label': 'E6', 'value': 'E6'},{'label': 'E7', 'value': 'E7'},{'label': 'F1', 'value': 'F1'}, {'label': 'F2', 'value': 'F2'}, {'label': 'F3', 'value': 'F3'},  {'label': 'F4', 'value': 'F4'},{'label': 'F5', 'value': 'F5'},{'label': 'G1', 'value': 'G1'},{'label': 'G2', 'value': 'G2'},{'label': 'G3', 'value': 'G3'},
                    {'label': 'G4', 'value': 'G4'},
                    {'label': 'G5', 'value': 'G5'},
                    {'label': 'G6', 'value': 'G6'},
                    {'label': 'H1', 'value': 'H1'},
                    {'label': 'H2', 'value': 'H2'},
                    {'label': 'H3', 'value': 'H3'},
                    {'label': 'H4', 'value': 'H4'},
                    {'label': 'H5', 'value': 'H5'},
                    {'label': 'H6', 'value': 'H6'},
                    {'label': 'I1', 'value': 'I1'},
                    {'label': 'I2', 'value': 'I2'},
                    {'label': 'I3', 'value': 'I3'},
                    {'label': 'I4', 'value': 'I4'},
                    {'label': 'I5', 'value': 'I5'},
                    {'label': 'J1', 'value': 'J1'},
                    {'label': 'J2', 'value': 'J2'},
                    {'label': 'J3', 'value': 'J3'},
                    {'label': 'J4', 'value': 'J4'},
                    {'label': 'J5', 'value': 'J5'},
                    {'label': 'J6', 'value': 'J6'},
                    {'label': 'K1', 'value': 'K1'},
                    {'label': 'K2', 'value': 'K2'},
                    {'label': 'K3', 'value': 'K3'},
                    {'label': 'K4', 'value': 'K4'},
                    {'label': 'K5', 'value': 'K5'},
                    {'label': 'K6', 'value': 'K6'},
                    ],
                value='R1', style={"width":"auto","height":"auto"}),html.Br(),html.Br(),

            dcc.DatePickerRange(id='my-date-picker-range',
                min_date_allowed=datetime(1995, 8, 5,1,1,1,1),
                max_date_allowed=datetime.now(),
                initial_visible_month=datetime.now(),
                end_date=datetime.now(),
                start_date=datetime.now()-timedelta(days=1)),
            html.Div(id='output-container-date-picker-range'),
            html.Div(id='dd-output-container'),
            dcc.Graph(id='graph-with-slider',style={"width":"auto","height":"300px"}, figure={
                            "layout": {
                                "paper_bgcolor": "#272a31",
                                "plot_bgcolor": "#272a31",
                            }
                        },),
            dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),dcc.Link(href='/page-2'),
],style={'maxHeight':"470px","overflowY":"scroll"})),
                ]),], style={"border":"2px black solid",'margin':"2rem 2rem 2rem 2rem"})
 

def control_layout(app):
    return  html.Div([
    dbc.Row([dbc.Col([ html.H4('DEVICES DROPDOWN LIST',style={'color':'white'}),
        dcc.Dropdown(id='device',
        options=[{'label': 'R1', 'value': 'R1'},{'label': 'R2', 'value': 'R2'},{'label': 'R3', 'value': 'R3'}],
        value='',style={"width":"8rem"}),html.Br(),html.Br(),
        dbc.Button("AUTOMODE", id="AUTOMODE button",className="mr-1",style={'width':'15rem','backgroundColor':'black','color':'white'}),html.Br(),html.Br(),

        # dbc.Button("Sun Track Start", id="SUNTRACK button",className="mr-1"),html.Br(),html.Br(),

        dbc.Button("STOP", id="STOP button",color='danger',className="mr-1",style={'width':'15rem','backgroundColor':'red'}),html.Br(),html.Br(),

        dbc.Button("MANUALMODE", id="MANUALMODE button",className="mr-1",style={'width':'15rem','backgroundColor':'black','color':'white'}),html.Br(),html.Br(),

         dbc.Button("EAST", id="EAST button",color='primary',outline=True,className="mr-2"),
           dbc.Button("WEST", id="WEST button",color='primary',outline=True,)
         ]),
         dbc.Col([dbc.Card([dbc.CardBody([dbc.CardHeader([ "Tracker Status"],style={'fontSize':'20px','fontColor':'darkblue'}),
             html.Div(["Sun Angle:"],style={'fontSize':"20px"}),html.Div(a,style={'fontSize':"20px",'textAlign':'left'}),html.Br(),
             html.Div(["Tracker Angle:"],style={'fontSize':"20px"}),html.Div(b,style={'fontSize':"20px",'textAlign':'left'}),html.Br(),
             html.Div(["Tracker Mode:"],style={'fontSize':"20px"}),html.Div(c,style={'fontSize':"20px",'textAlign':'left'}),html.Br(),
             html.Div(["Motor Status:"],style={'fontSize':"20px"}),html.Div(e,style={'fontSize':"20px",'textAlign':'left'}),html.Br(),

             ])],style={'width':'18rem'}),
         ]),            dcc.Link(href='/control'),])])



def location_layout(app):
    return html.Div(id="location-container",className="row",
            children=[
                html.Div(id="location1",className="twelve columns",
                    children=[html.H4('Using these you can write the commands for setting the values in the device'),]),
                html.Div(id="location2",className="twelve columns",
                    children=[
                        dcc.Dropdown(id='device', options=[{'label': 'R1', 'value': 'R1'},{'label': 'R2', 'value': 'R2'},{'label': 'R3', 'value': 'R3'}],value='',style={"width":"8rem",'color':'black'}    ),  html.Div(id="output"),] ), 
        html.Div(id="location3",className="twelve columns",
            children=[html.H4("TimeStamp")]),
          html.Div(id="location4",className="six columns",
            children=[
                html.H6("Seconds",className="mr-1",style={'color':'white'}), dcc.Input(id="input SEC", type="text",className="mr-1"),
                dbc.Button("Send", id="SEC button",color='primary',outline=True),html.Br(),
        html.H6("Minute",className="mr-3",style={'color':'white'}),dcc.Input(id="input MIN", type="text",className="mr-1"),
           dbc.Button("Send", id="MIN button",color='primary',outline=True),html.Br(),
       html.H6("Hour",className="mr-4",style={'color':'white'}),dcc.Input(id="input HOUR", type="text",className="mr-1"),
           dbc.Button("Send", id="HOUR button",color='primary',outline=True),html.Br(),
     html.H6("Date",className="mr-4",style={'color':'white'}),dcc.Input(id="input DATE", type="text",className="mr-1"),
          dbc.Button("Send", id="DATE button",color='primary',outline=True),html.Br(),
     html.H6("Month",className="mr-3",style={'color':'white'}),dcc.Input(id="input MONTH", type="text",className="mr-1"),
          dbc.Button("Send", id="MONTH button",color='primary',outline=True),html.Br(),
    html.H6("Year",className="mr-4",style={'color':'white'}),dcc.Input(id="input YEAR", type="text",className="mr-1"),
         dbc.Button("Send", id="YEAR button",color='primary',outline=True),html.Br(),]),
        html.Div(id="location5",className="twelve columns",
            children=[html.H4("Location")]),
        html.Div(id="location6",className="six columns",
            children=[
                html.H6("Latitude",className="mr-3",style={'color':'white'}),dcc.Input(id="input LAT", type="text",className="mr-1"),
            dbc.Button("Send", id="LAT button",color='primary',outline=True,),
        html.H6("Longitude",className="mr-2",style={'color':'white'}),dcc.Input(id="input LONGITUDE", type="text",className="mr-1"),
            dbc.Button("Send", id="LONGITUDE button",color='primary',outline=True),
       html.H6("Timezone",className="mr-2",style={'color':'white'}), dcc.Input(id="input TIMEZONE", type="text",className="mr-1"),
            dbc.Button("Send", id="TIMEZONE button",color='primary',outline=True)]),
       html.Div(id="location7",className="five columns",
            children=[html.H4("Tracker Limits")]),
       html.Div(id="location8",className="five columns",
            children=[html.H6("East Limit",className="mr-1",style={'color':'white'}),  dcc.Input(id="input ELIM", type="text",className="mr-1"),
          dbc.Button("Send", id="ELIM button",color='primary',outline=True,),
       html.H6("West Limit",className="mr-1",style={'color':'white'}), dcc.Input(id="input WLIM", type="text",className="mr-1"),
           dbc.Button("Send", id="WLIM button",color='primary',outline=True),]),dcc.Link(href='/location')])



def status_layout(app):
    return html.Div(id="top-status-container",className="row",
            children=[
                html.Div(id="status1",className="three columns",
            children=[dbc.Card([html.Div(["Sun Angle"],style={'fontSize':"20px",'margin':'1rem','textAlign':'center'}),html.Div(a,style={'fontSize':"30px",'margin':'1rem','textAlign':'center'})],style={'width':'11rem','height':'8rem','backgroundColor':'#488AC7','height':'8rem'})]),
                html.Div(id="status2",className="three columns",
            children=[dbc.Card([html.Div(["Tracker Angle"],style={'fontSize':"20px",'margin':'1rem','textAlign':'center'}),html.Div(b,style={'fontSize':"30px",'margin':'1rem','textAlign':'center'})],style={'width':'11rem','height':'8rem','backgroundColor':'#488AC7','height':'8rem'})]),
                html.Div(id="status3",className="three columns",
            children=[dbc.Card([html.Div(["TRACKER MODE"],style={'fontSize':"20px",'margin':'1rem','textAlign':'center'}),html.Div(c,style={'fontSize':"30px",'margin':'1rem','textAlign':'center'})],style={'width':'11rem','height':'8rem','backgroundColor':'#488AC7','height':'8rem'})]),
    html.Div(id="status4",className="three columns",
            children=[dbc.Card([html.Div(["Motor Status"],style={'fontSize':"20px",'margin':'1rem','textAlign':'center'}),html.Div(e,style={'fontSize':"30px",'margin':'1rem','textAlign':'center'})],style={'width':'11rem','height':'8rem','backgroundColor':'#488AC7','height':'8rem'})]),
 dcc.Link(href='/status'),])

def read_layout(app):
    return  html.Div([
    html.H4('You can read the data using these dropdown buttons'),html.Br(),

    dcc.Dropdown(
        id='devices1',
        options=[
            {'label': 'R1', 'value': 'R1'},
            {'label': 'G2', 'value': 'G2'},
            {'label': 'R2', 'value': 'R2'}
        ],
        value='', style={"width":"8rem"}),html.Br(),html.Br(),


    dcc.Dropdown(
        id='options1',
        options=[
            {'label': 'ELIM', 'value': 'ELIM'},
            {'label': 'LAT', 'value': 'LAT'},
            {'label': 'LON', 'value': 'LON'},
            {'label': 'TA', 'value': 'TA'},
            {'label': 'WLIM', 'value': 'WLIM'},
            {'label': 'SPA', 'value': 'SPA'},
            {'label': 'MOTOR', 'value': 'MOTOR'},
            {'label': 'ZONE', 'value': 'ZONE'},
            {'label': 'MODE', 'value': 'MODE'},
            {'label': 'HR', 'value': 'HR'},
            {'label': 'MIN', 'value': 'MIN'},
            {'label': 'SEC', 'value': 'SEC'},
            {'label': 'DATE', 'value': 'DATE'},
            {'label': 'MONTH', 'value': 'MONTH'},
            {'label': 'YEAR', 'value': 'YEAR'},
            {'label': 'DAY', 'value': 'DAY'},
                    ],
        value='', style={"width":"8rem"}),html.Br(),html.Br(),
    dbc.Button("Read", id="buttons1"),

    html.Div(id='display'),
    dcc.Link(href='/page-3'),html.H5("Tracker Data:"),
    html.Div(messagelist2),html.H5("SMB Data:"),html.Div(messagelist)],style={'minHeight':"500px","overflowY":"scroll",'backgroundColor':'info'})






def alarms_layout(app):
    return html.Div([html.H3("ALARMS.................Page on Progress..........",style={'color':'maroon'}), dcc.Link(href='/alarms')])


app.config['suppress_callback_exceptions']=True



app.layout = html.Div( id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_row(),
                # Main app
              dcc.Location(id="url", refresh=False),html.Div(id="app-content"),
            ],
        ),
        ])


@app.callback(
        Output('display', 'children'),
        [Input('devices1', 'value'),Input('options1', 'value'),Input('buttons1','n_clicks')])

def output(val1,val2,n):
    if n:
        client.publish(pubtop,"{} READ:{}".format(val1,val2))
        return "published for getting {}".format(val2)

@app.callback( Output('SEC button', 'value'),[Input('device', 'value'),Input('input SEC', 'value'),Input('SEC button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:SEC_{}".format(valueDEV,value2))
        #return 'You have published "{} SEC write {}"'.format(valueDEV,value2)
#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('MIN button', 'value'),[Input('device', 'value'),Input('input MIN', 'value'),Input('MIN button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:MIN_{}".format(valueDEV,value2))
        return 'You have published "{} MIN write {}"'.format(valueDEV,value2)
#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('HOUR button', 'value'),[Input('device', 'value'),Input('input HOUR', 'value'),Input('HOUR button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:HOUR_{}".format(valueDEV,value2))
        return 'You have published "{} HOUR write {}"'.format(valueDEV,value2)

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('DATE button', 'value'),[Input('device', 'value'),Input('input DATE', 'value'),Input('DATE button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:DATE_{}".format(valueDEV,value2))
        return 'You have published "{} DATE write {}"'.format(valueDEV,value2)

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('MONTH button', 'value'),[Input('device', 'value'),Input('input MONTH', 'value'),Input('MONTH button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:MONTH_{}".format(valueDEV,value2))
        return 'You have published "{} MONTH write {}"'.format(valueDEV,value2)

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('YEAR button', 'value'),[Input('device', 'value'),Input('input YEAR', 'value'),Input('YEAR button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:YEAR_{}".format(valueDEV,value2))
        return 'You have published "{} YEAR write {}"'.format(valueDEV,value2)

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('LAT button', 'value'),[Input('device', 'value'),Input('input LAT', 'value'),Input('LAT button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:LAT_{}".format(valueDEV,value2))
        return 'You have published "{} LAT write {}"'.format(valueDEV,value2)

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('LONGITUDE button', 'value'),[Input('device', 'value'),Input('input LONGITUDE', 'value'),Input('LONGITUDE button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:LONGITUDE_{}".format(valueDEV,value2))
        return 'You have published "{} LONGITUDE write {}"'.format(valueDEV,value2)

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('ELIM button', 'value'),[Input('device', 'value'),Input('input ELIM', 'value'),Input('ELIM button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:ELIM_{}".format(valueDEV,value2))
        return 'You have published "{} ELIM write {}"'.format(valueDEV,value2)
#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('WLIM button', 'value'),[Input('device', 'value'),Input('input WLIM', 'value'),Input('WLIM button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:WLIM_{}".format(valueDEV,value2))
        return 'You have published "{} WLIM write {}"'.format(valueDEV,value2)

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('TIMEZONE button', 'value'),[Input('device', 'value'),Input('input TIMEZONE', 'value'),Input('TIMEZONE button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:TIMEZONE_{}".format(valueDEV,value2))
        return 'You have published "{} TIMEZONE write {}"'.format(valueDEV,value2)
#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('EAST button', 'value'),[Input('device', 'value'),Input('EAST button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:EAST".format(valueDEV))
        return 'You have published "{} write EAST"'.format(valueDEV)

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('WEST button', 'value'),[Input('device', 'value'),Input('WEST button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:WEST".format(valueDEV))
        return 'You have published "{} write WEST"'.format(valueDEV)

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('AUTOMODE button', 'value'),[Input('device', 'value'),Input('AUTOMODE button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:AUTOMODE".format(valueDEV))
        return 'You have published "{} write AUTOMODE"'.format(valueDEV)

#/*------------------------------------------------------------------------------------------------------------------*/
    
@app.callback( Output('MANUALMODE button', 'value'),[Input('device', 'value'),Input('MANUALMODE button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:MANUALMODE".format(valueDEV))
        return 'You have published "{} write MANUALMODE"'.format(valueDEV)
#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback( Output('STOP button', 'value'),[Input('device', 'value'),Input('STOP button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:STOP".format(valueDEV))
        return 'You have published "{} write STOP"'.format(valueDEV)

#/*------------------------------------------------------------------------------------------------------------------*/

def conv(x):
    val=unicodedata.normalize('NFKD', x).encode('ascii','ignore')
    print("val=",val)
    return val



def timeconvert(dftime):
    print("dftime=",dftime[0])
    print("dftime=",len(dftime))
    #x=dftime[:8]+".00000"+dftime[9:]
    for i in dftime:
        dftime[i]=datetime.strptime(dftime[i],"%d/%m/%Y %H:%M:%S.%f")
    return dftime

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback(Output("download-link", "href"),
              [Input("download-link", "className"),Input('my-date-picker-range2', 'start_date'),
                  Input('my-date-picker-range2', 'end_date')])
def update_download_link(input_value,start,end):
    print("executing")
    connection1 = engine
    df=pd.read_sql("select * from datatable",connection1)
    filtered_df = df.loc[(df['stamp'] > start) & (df['stamp'] <= end)]
    filtered_df=filtered_df.values.tolist()
    con_df = pd.DataFrame(filtered_df, columns=['id','stamp','devId','SPA','TA'])
    print("con_df=",con_df)

    cv = con_df.to_csv(index=False, encoding='utf-8')
    cv = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(cv)
    return cv

#/*------------------------------------------------------------------------------------------------------------------*/
@app.callback(Output("download-linksmb", "href"),
              [Input("download-linksmb", "className"),Input('my-date-picker-range2smb', 'start_date'),
                  Input('my-date-picker-range2smb', 'end_date')])
def update_download_link(input_value,start,end):
    print("executing")
    connection1 = engine
    df=pd.read_sql("select * from smbtable",connection1)
    filtered_df = df.loc[(df['stamp'] > start) & (df['stamp'] <= end)]
    filtered_df=filtered_df.values.tolist()
    con_df = pd.DataFrame(filtered_df, columns=['id','stamp','devId','str1','str2','str3','str4','str5','str6','str7','str8','str9','str10','str11','str12','str13','vol1','vol2','vol3','vol4','vol5','vol6','vol7','vol8','vol9','vol10','vol11','vol12','vol13','temp','stravg','volavg','poweravg'])
    print("con_df=",con_df)

    cv = con_df.to_csv(index=False, encoding='utf-8')
    cv = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(cv)
    return cv

#/*------------------------------------------------------------------------------------------------------------------*/

@app.callback(Output("live-update-text", "children"),
              [Input("live-update-text", "className"),Input('my-date-picker-range2', 'start_date'),Input('my-date-picker-range2', 'end_date')])
def update_output_div(input_value,start,end):
    connection1 = engine#.connnect()
    df=pd.read_sql("select * from datatable",connection1)
    filtered_df = df.loc[(df['stamp'] > start) & (df['stamp'] <= end)]
    print("table filtereddf=",filtered_df.stamp)
    print("table filtereddf=",filtered_df.all)
    filtered_df=filtered_df.values.tolist()
    return [html.Table(table(filtered_df)
        )]

@app.callback(Output("live-update-text-smb", "children"),
              [Input("live-update-text-smb", "className"),Input('my-date-picker-range2smb', 'start_date'),Input('my-date-picker-range2smb', 'end_date')])
def update_output_div(input_value,start,end):
    connection1 = engine#.connnect()
    df=pd.read_sql("select * from smbtable",connection1)
    print("smb table=",df)
    print("smb table df time=",df['stamp'])
    print("smb start=",str(start),"smb end",end)
    filtered_df = df.loc[(start < df['stamp']) & (end >= df['stamp'])]
    filtered_df=filtered_df.values.tolist()
    return [html.Table(tablesmb(filtered_df))]

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('devices', 'value'),Input('my-date-picker-range', 'start_date'),Input('my-date-picker-range', 'end_date')])
def update_figure(selected_device,start,end):
    connection1 = engine
    print("start=",start,"end=",end,"dt.now=",datetime.now())
    df=pd.read_sql("select * from datatable",connection1)
    filtered_d = df[df.devId == selected_device]
    filtered_df = filtered_d.loc[(filtered_d['stamp'] > start) & (filtered_d['stamp'] <= end)]
    print("filtered df=",filtered_df)
    client.publish(pubtop,"{} READ:GETALL".format(selected_device))
    return {'data': [{'x': filtered_df.stamp, 'y':filtered_df.SPA, 'name': 'SPA'},
        {'x': filtered_df.stamp, 'y':filtered_df.TA, 'name': 'TA'}, ],
            'layout': {
                'title':'(SPA and TA)  vs Time',
                "font":{"color":"white"},
                    "paper_bgcolor": "#000000",
                                "plot_bgcolor": "#172a31",
                                "xaxis": dict(
                                showline=False, showgrid=False, zeroline=False,color='white'
                            ),
                            "yaxis": dict(
                                showgrid=False, showline=False, zeroline=False,color="white"
                            ),
                            "autosize": True,}}

@app.callback(Output("app-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/plantview":
        return plantview_layout(app)
    if pathname == "/sld":
        return sld_layout(app)
    if pathname == "/layout":
        return layout_layout(app)
    if pathname == "/power":
        return power_layout(app)
    if pathname == "/ht-panels":
        return htpanels_layout(app)
    if pathname == "/inverters":
        return inverters_layout(app)
    if pathname == "/RMU":
        return RMU_layout(app)
    if pathname == "/smb":
        return smb_layout(app)
    if pathname == "/tracker":
        return tracker_layout(app)
    if pathname == "/alarms":
        return alarms_layout(app)
    if pathname == "/control":
        return control_layout(app)
    if pathname == "/location":
        return location_layout(app)
    if pathname == "/status":
        return status_layout(app)
    if pathname == "/read":
        return read_layout(app)
    if pathname == "/home":
        return home_layout(app)



   
if __name__ == '__main__':
    app.run_server(debug=True,threaded=True, use_reloader=False)

