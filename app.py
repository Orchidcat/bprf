import os
import sys

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit

# from admin.second import second1
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
# app.register_blueprint(second1, url_perfix="/admin")




app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)


class tempData(db.Model):
    __tablename__ = 'tempData'
    dd = db.Column(db.DateTime, primary_key=True)
    sensorData = db.Column(db.Float)
    sensorID = db.Column(db.Integer)

# class vDatatemp(db.Model):
#     __tablename__ = 'v_data_temp'
#     dd = db.Column(db.DateTime, primary_key=True)
#     sensorData = db.Column(db.Float)
#     sensorID = db.Column(db.Integer)
#     ddtime = db.Column(db.text)





# labels = [
#     'JAN', 'FEB', 'MAR', 'APR',
#     'MAY', 'JUN', 'JUL', 'AUG',
#     'SEP', 'OCT', 'NOV', 'DEC'
# ]
#
# values = [
#     967.67, 1190.89, 1079.75, 1349.19,
#     2328.91, 2504.28, 2873.83, 4764.87,
#     4349.29, 6458.30, 9907, 16297
# ]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.before_request
def create_tables():
    db.create_all()

@app.route("/")
def test():
    import datetime
    times = [];
    datas = [];

    gettimes = tempData.query.with_entities(tempData.dd)
    getdatas = tempData.query.with_entities(tempData.sensorData)

    for (i, j) in zip(getdatas, gettimes):
        if i.sensorData is None:
            continue
        else:
            datas.append(i.sensorData)
            times.append(str(j.dd)[-9:])
            print('数据:'+str(i.sensorData), '时间:'+str(j.dd))

    return render_template('home.html', lables=times, values=datas)




if __name__ == "__main__":
    app.run(debug=True)