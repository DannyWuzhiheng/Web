from flask import Flask, render_template, request, redirect, url_for, send_file
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
                    return redirect('http://116.62.60.158/index', code=302) 
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
@app.route('/jinshan')
def get_image():
    image_path = os.path.join('pic', 'jinshan.png')
    return send_file(image_path, mimetype='image/png') 
@app.route('/feishu')
def get_image2():
    image_path = os.path.join('pic', 'feishu.png')
    return send_file(image_path, mimetype='image/png') 
if __name__ == '__main__':  
    app.run(host="0.0.0.0", debug=True, port=80)