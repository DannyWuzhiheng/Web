from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
import os 
import pandas as pd  

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
                    resp.set_cookie("username",username)
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
        sig=request.form['signature'] 
        with open(r'./login.txt','a') as f:
            if password==rpassword:
                f.write(f'\n{username} {password} {sig}')
                os.system(f"cp pic/user/main.png pic/user/upload/{username}.png")
                return redirect('http://116.62.60.158/login', code=302) 
            else:
                return "注册失败"        
    return render_template('signup.html')  
@app.route('/index')  
def main_net():  
    cookie = request.cookies.get("username")
    if cookie==None:
        cookie = "您未登录"
    return render_template('index.html',username=cookie)  
@app.route('/join')  
def join_net():  
    return render_template('join.html')  
@app.route('/sheet')  
def bird_sheet():  
    return render_template('sheet.html')  
@app.route('/imform')  
def imform_net():  
    page=request.args.get("page")
    if page == None or page=='' or page == ' ':
        page=1
    cookie = request.cookies.get("username")
    if cookie==None:
        cookie = "您未登录"
   
    with open(r'/Web/imform.json','r',encoding='utf-8') as f:
        json=f.read()
    df = pd.read_json(json, orient='records')
    id_=df['id']
    tag=df['tag']
    img=df['imageUrl']
    dec=df['description']
    return render_template('imform.html',page=int(page),username=cookie,tag=tag,dec=dec,img=img,gs=len(tag)+5//6,id=id_) 
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
@app.route('/usrpic')
def get_image4():
    file=request.args.get("key")+'.png'
    image_path = os.path.join('pic/user/upload', file)
    print(image_path)
    return send_file(image_path, mimetype='image/png') 
@app.route('/')  
def net():  
    return redirect('http://116.62.60.158/login', code=302) 

@app.route('/admin')
def admin():
    cookie_1 = request.cookies.get("ss")
    if cookie_1 == 'admin':
        return render_template(f'admin.html')
    else:
        return "您没有权限"
@app.route('/admin/science',methods=['GET', 'POST'])
def edit_1():
    cookie_1 = request.cookies.get("ss")
    if cookie_1 == 'admin':
        if request.method == 'POST':  
            pass
        return render_template(f'admin_sci.html')
    else:
        return "您没有权限"
@app.route('/admin/birds')
def edit_2():
    cookie_1 = request.cookies.get("ss")
    if cookie_1 == 'admin':
        if request.method == 'POST':  
            pass
        return render_template(f'admin_bird.html')
    else:
        return "您没有权限"
@app.route('/user')
def user_net():
    cookie = request.cookies.get("username")
    cookie2 = request.cookies.get("ss")
    if cookie==None:
        return redirect('http://116.62.60.158/login', code=302) 
    with open("login.txt","r",encoding='utf-8') as f:
        a=f.read()
        a=a.split('\n')
        for i in a:
            m=i.split(' ')
            if m[0]==cookie:
                sig=m[2]
    return render_template(f'user.html',sig=sig,username=cookie,cookie=cookie2)

@app.errorhandler(Exception)
def handle_exception(error):
    return render_template('error.html')

if __name__ == '__main__':  
    os.system("clear")
    os.system("figlet LYFY   Web")
    app.run(host="0.0.0.0", debug=True, port=80)