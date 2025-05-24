from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
import os 
import pandas as pd  
import json

def edit(index,description,new_id="",name="",json_path="/Web/imform.json"):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if 0 <= index < len(data):
        data[index]['description'] = description
    else:
        new_id = new_id
        new_section = {
            "id": new_id,
            "name": name,
            "tag": name,
            "imageUrl": f"http://116.62.60.158/pic?key={new_id}",
            "description": description
        }
        data.append(new_section)
        print("成功：新增板块")
    
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return "成功"
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
                    #此处没有使用高级方法，以后修复
                    if username == YOUR_ADMIN:
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
        with open(r'./login.txt','r') as f:
            f.read()
            for i in a:
                usps=i.split(' ')
                if usps[0]==username:
                    return "注册失败，用户名已存在" 
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
    bird_list=[]
    path='/Web/fjbird/'
    pathlist=os.listdir(path)
    for j in pathlist:
        with open(f'/Web/fjbird/{j}','r',encoding='utf-8') as f:
            json=f.read()
        df = pd.read_json(json, orient='records')
        n=df['name']
        l=df['list']
        a=j.replace('.json','')
        listk=[a]
        for i in range(len(n)):
            lists=[n[i],l[i]]
            listk.append(lists)
        bird_list.append(listk)
    with open("l.txt",'w',encoding='utf-8') as f:
        f.write(str(bird_list))
    return render_template('sheet.html',bird=bird_list)  
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
    return render_template('imform.html',page=int(page),username=cookie,tag=tag,dec=dec,img=img,gs=len(tag)+5//6,id=id_,l=len(tag))
@app.route('/imform/<i>')
def bird_inet(i):
    with open(r'/Web/imform.json','r',encoding='utf-8') as f:
        json=f.read()
    df = pd.read_json(json, orient='records')
    tag=df['tag']
    dec=df['description']
    img=df['imageUrl']
    i=int(i)
    return render_template(f'imform_base.html',name=tag[i],dec=dec[i],img=img[i])
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
@app.route('/pica')
def get_image55():
    file=request.args.get("key")+'.jpg'
    image_path = os.path.join('pic/nav', file)
    print(image_path)
    return send_file(image_path, mimetype='image/jpg') 
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
def edit_web_admin():
    cookie_1 = request.cookies.get("ss")
    with open(r'/Web/imform.json','r',encoding='utf-8') as f:
        json=f.read()
    df = pd.read_json(json, orient='records')
    name=df['tag']
    dec=df['description']
    l=len(dec)
    if cookie_1 == 'admin':
        if request.method == 'POST':  
                description=[]
                for i in range(l):
                    try:
                        description.append([request.form[f"description_{i}"],i])
                    except:
                        pass
                try:
                    description.append([request.form[f"description_{l}"],l])
                    new_id=request.form["new_id"]
                    name=request.form["name"]
                except:
                    pass    
                for i in range(len(description)):
                    if(description[i][1]==l):
                        edit(l,description[i][0],new_id,name)
                    else:
                        edit(description[i][1],description[i][0])
        return render_template(f'admin_science.html',name=name,description=dec,l=l)
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
    return render_template('user.html',sig=sig,username=cookie,cookie=cookie2)
POSTS_DIR = '/Web/chat/'

@app.route('/chat', methods=['GET', 'POST'])
def chat_net():
    if request.method == 'POST':
        title = request.form.get('post-title')
        content = request.form.get('post-content')
        tags = request.form.get('post-tags').split(',') if request.form.get('post-tags') else []
        cookie = request.cookies.get("username")
        if cookie==None:
            return redirect('http://116.62.60.158/login', code=302)
        new_post = {
            "title": title,
            "author": cookie,
            "content": content,
            "image_url": "",  # 这里可以添加获取图片 URL 的逻辑
            "tags": [tag.strip() for tag in tags],
            "comments": [],
            "likes": 0
        }

        # 生成新的文件名
        post_count = len(os.listdir(POSTS_DIR))
        new_filename = os.path.join(POSTS_DIR, f"post_{post_count + 1}.json")

        # 保存新帖子为 JSON 文件
        with open(new_filename, 'w', encoding='utf-8') as f:
            json.dump(new_post, f, ensure_ascii=False, indent=4)

        return redirect(url_for('chat_net'))

    l = []
    pathlist = os.listdir(POSTS_DIR)
    for p in pathlist:
        file_path = os.path.join(POSTS_DIR, p)
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                l.append(data)
        except (json.JSONDecodeError, FileNotFoundError):
            continue

    return render_template('chat.html', posts=l)

@app.route('/like/<int:post_index>', methods=['POST'])
def like(post_index):
    pathlist = os.listdir(POSTS_DIR)
    file_path = os.path.join(POSTS_DIR, pathlist[post_index])

    try:
        with open(file_path, "r", encoding='utf-8') as f:
            post = json.load(f)
        post['likes'] += 1

        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(post, f, ensure_ascii=False, indent=4)
    except (json.JSONDecodeError, FileNotFoundError):
        pass

    return redirect(url_for('chat_net'))

@app.route('/comment/<int:post_index>', methods=['POST'])
def comment(post_index):
    pathlist = os.listdir(POSTS_DIR)
    file_path = os.path.join(POSTS_DIR, pathlist[post_index])
    content = request.form.get('comment-content')
    cookie = request.cookies.get("username")
    if cookie==None:
        return redirect('http://116.62.60.158/login', code=302)
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            post = json.load(f)
            new_comment = {
                "id": len(post['comments']),  # 简单生成评论 ID
                "author": cookie,
                "published_at": cookie,  # 这里可以添加获取当前时间的逻辑
                "content": content
            }
            post['comments'].append(new_comment)
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(post, f, ensure_ascii=False, indent=4)
    except (json.JSONDecodeError, FileNotFoundError):
        pass

    return redirect(url_for('chat_net'))
'''
@app.errorhandler(Exception)
def handle_exception(error):
    return render_template('error.html')
'''
if __name__ == '__main__':  
    os.system("clear")
    os.system("figlet LYFY   Web")
    app.run(host="0.0.0.0", debug=True, port=80)
