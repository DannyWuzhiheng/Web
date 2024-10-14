from flask import Flask, render_template, request, redirect, url_for, send_file, make_response

import os 

app = Flask(__name__)  
  
@app.route('/login', methods=['GET', 'POST'])  
def login_net():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password'] 
        with open(r'./login.txt','r') as f:
            a=f.read()
            a=a.split('\n')
            for i in a:
                usps=i.split(' ')
                if usps[0]==username and usps[1]==password:
                    resp = make_response(redirect('http://116.62.60.158/index', code=302))
                    resp.set_cookie("login",username)
                    if username == 'Administrator':
                        resp.set_cookie("ss",'admin')
                    else:
                        resp.set_cookie("ss",'user')
                    return resp
            else:
                return "登录失败"  
    return render_template('login.html')  
@app.route('/signup', methods=['GET', 'POST'])  
def signup_net():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password'] 
        rpassword = request.form['rpassword'] 
        with open(r'./login.txt','a') as f:
            if password==rpassword:
                f.write(f'\n{username} {password}')
                return redirect('http://116.62.60.158/login', code=302) 
            else:
                return "注册失败"        
    return render_template('signup.html')  
@app.route('/index')  
def main_net():  
    return render_template('index.html')  
@app.route('/join')  
def join_net():  
    return render_template('join.html')  
@app.route('/imform')  
def imform_net():  
    page=request.args.get("page")
    if page == None or page=='' or page == ' ':
        page=1
    return render_template('imform.html',page=int(page)) 
@app.route('/imform/<name>')
def bird_inet(name):
    return render_template(f'imform_{name}.html')
@app.route('/jinshan')
def get_image():
    image_path = os.path.join('pic', 'jinshan.png')
    return send_file(image_path, mimetype='image/png') 
@app.route('/feishu')
def get_image2():
    image_path = os.path.join('pic', 'feishu.png')
    return send_file(image_path, mimetype='image/png') 
@app.route('/pic')
def get_image3():
    file=request.args.get("key")+'.png'
    image_path = os.path.join('pic', file)
    print(image_path)
    return send_file(image_path, mimetype='image/png') 
@app.route('/')  
def net():  
    return redirect('http://116.62.60.158/login', code=302) 
@app.route('/pros')
def pros():
    cookie_1 = request.cookies.get("ss")
    if cookie_1 == 'admin':
        return render_template(f'admin.html')
    else:
        return "您没有权限"

@app.errorhandler(Exception)
def handle_exception(error):
    return render_template('error.html')

if __name__ == '__main__':  
    app.run(host="0.0.0.0", debug=True, port=80)
