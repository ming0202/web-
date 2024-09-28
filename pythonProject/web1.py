from flask import Flask,render_template,jsonify,request,redirect,session
import functools

app = Flask(__name__)

app.secret_key = 'ufrr8u57u8'

DATA_DICT = {
    1:{'name':'w',"age":22},
    2:{'name':'c',"age":20},
}

def auth(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):
        username = session.get('user')
        if not username:
            return redirect('/login')
        return func(*args,**kwargs)
    return inner

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user == 'w' and pwd == "123456":
        session['user'] = 'w'
        return redirect('/index')
    error = '账号或密码错误'
    return render_template('login.html',error=error)

@app.route('/index')
@auth
def index():
    data_dict = DATA_DICT
    return render_template('index.html',data_dict=data_dict)

@app.route('/edit',methods=['GET','POST'])
@auth
def edit():
    nid = request.args.get('nid')
    nid = int(nid)

    if request.method == "GET":
        info = DATA_DICT[nid]
        return render_template('edit.html',info=info)

    user = request.form.get('user')
    age = request.form.get('age')
    DATA_DICT[nid]['name'] = user
    DATA_DICT[nid]['age'] = age
    return redirect('/index')

@app.route('/delete/<int:nid>')
@auth
def delete(nid):
    del DATA_DICT[nid]
    return redirect('/index')

if __name__=='__main__':
    app.run()