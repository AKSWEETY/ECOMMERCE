import random

from flask import Flask, request, render_template, redirect, session

import os
import pymysql

from Mail import send_email

conn = pymysql.connect(host="localhost", user="root", password="root", db="E_commerce")
cursor = conn.cursor()

App_Root = os.path.dirname(os.path.abspath(__file__))
E_commerce_files_path = App_Root + "/static/E_commerce_files"
posted_files_image_path = App_Root + "/static/posted_files/images"
posted_files_audio_path = App_Root + "/static/posted_files/audio"
posted_files_video_path = App_Root + "/static/posted_files/video"
product_files_path = App_Root + "/static/product_files/images"

app = Flask(__name__)
app.secret_key = "E-commerce"
port = 7070

admin_username = "admin"
admin_password = "admin"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/user_login")
def user_login():
    return render_template("user_login.html")


@app.route("/user_registration")
def user_registration():
    return render_template("user_registration.html")


@app.route("/admin_login_action", methods=['post'])
def admin_login_action():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == admin_username and password == admin_password:
        session['role'] = 'admin'
        return redirect("/admin_home")
    else:
        return render_template("message.html", message="Invalid Login Credentials")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/add_view_location")
def add_view_location():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("/add_view_location.html", locations=locations)


@app.route("/add_view_location_action", methods=["post"])
def add_view_location_action():
    location_name = request.form.get("location_name")
    cursor.execute("insert into location(location_name) values('"+str(location_name)+"')")
    conn.commit()
    return redirect("/add_view_location")


@app.route("/add_sale_packages")
def add_sale_packages():
    return render_template("add_sale_packages.html")


@app.route("/add_sale_package_action")
def add_sale_package_action():
    package_title = request.args.get("package_title")
    no_of_customer_reach = request.args.get("no_of_customer_reach")
    package_price = request.args.get("package_price")
    validity_in_days = request.args.get("validity_in_days")
    cursor.execute("insert into sale_package(pacakge_title,no_of_customer_reach,package_price,validity_in_days)values('"+str(package_title)+"','"+str(no_of_customer_reach)+"','"+str(package_price)+"','"+str(validity_in_days)+"')")
    conn.commit()
    return render_template("admin_message.html", message="Package Added Successfully" )


@app.route("/view_sale_packages")
def view_sale_packages():
    cursor.execute("select * from sale_package" )
    sale_packages = cursor.fetchall()
    return render_template("view_sale_packages.html",sale_packages=sale_packages)


@app.route("/user_registration_action", methods=['post'])
def user_registration_action():
    otp = request.form.get("otp")
    otp2 = request.form.get("otp2")
    if otp != otp2:
        return render_template("message.html", message="Invalid Otp! Plz Try Again")
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address = request.form.get("address")
    gender = request.form.get("gender")
    profile_picture = request.files.get("profile_picture")
    path = E_commerce_files_path + "/" + profile_picture.filename
    profile_picture.save(path)
    cursor.execute("insert into user(name,email,phone,password,address,gender,profile_picture)values('"+str(name)+"','"+str(email)+"','"+str(phone)+"','"+str(password)+"','"+str(address)+"','"+str(gender)+"','"+str(profile_picture.filename)+"')")
    conn.commit()
    return render_template("message.html", message="User Registration Successfully")


@app.route("/mail_verification")
def mail_verification():
    return render_template("mail_verification.html")


@app.route("/mail_verification_action", methods=['post'])
def mail_verification_action():
    email = request.form.get("email")
    otp = random.randint(1000,10000)
    print(otp)
    count = cursor.execute("select * from user where email='"+str(email)+"' ")
    if count > 0:
        send_email("OTP For Login ","OTP For Login Verification :  "+str(otp)+"",email)
        return render_template("/otp_with_login.html",email=email,otp=otp)
    else:
        send_email("OTP For Registration ", "Use This " + str(otp) + " To Register Your Account", email)
        return render_template("/user_registration.html", email=email,otp=otp)


@app.route("/otp_with_login")
def otp_with_login():
    return render_template("otp_with_login.html")


@app.route("/otp_with_login_action", methods=['post'])
def otp_with_login_action():
    otp = request.form.get("otp")
    otp2 = request.form.get("otp2")
    if otp != otp2:
        return render_template("message.html",message="Invalid Otp! Plz Try Again")
    else:
        email = request.form.get("email")
        cursor.execute("select * from user where email='"+str(email)+"'")
    user = cursor.fetchone()
    session['user_id'] = user[0]
    session['role'] = 'user'
    return redirect("/user_home")


@app.route("/user_home")
def user_home():
    cursor.execute("select * from user where user_id='"+str(session['user_id'])+"' ")
    user = cursor.fetchone()
    return render_template("user_home.html",user=user)


@app.route("/edit_user_profile")
def edit_user_profile():
    user_id = request.args.get('user_id')
    return render_template("edit_user_profile.html",user_id=user_id,get_user_details_by_user_id=get_user_details_by_user_id)


@app.route("/update_user_profile_action",methods=['post'])
def update_user_profile_action():
    user_id = request.form.get("user_id")
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address = request.form.get("address")
    cursor.execute("update user set name='" + str(name) + "', email = '" + str(email) + "', phone ='" + str(phone) + "', password='" + str(password) + "',address = '" + str(address) + "' where user_id='" + str(user_id) + "' ")
    conn.commit()
    return render_template("user_message.html", message="Your Profile Updated Successfully")


def get_user_details_by_user_id(user_id):
    cursor.execute("select * from user where user_id = '"+str(user_id)+"' ")
    users = cursor.fetchall()
    return users[0]


@app.route("/search_friends")
def search_friends():
    return render_template("search_friends.html")


@app.route("/send_friend_request")
def send_friend_request():
    user_id = request.args.get("user_id")
    cursor.execute("insert into friend_request(status,from_user_id,to_user_id)values('Requested','"+str(session['user_id'])+"', '"+str(user_id)+"') ")
    conn.commit()
    return {"message":"Friend request send Successfully"}


@app.route("/get_users")
def get_users():
    keyword = request.args.get("keyword")
    required_type = request.args.get("required_type")
    query = "select * from user"
    if keyword != None:
        query = "select * from user where (name like '%" + str(keyword) + "%' or email like '%" + str(keyword) + "%' or phone like '%" + str(keyword) + "%')  and user_id != '"+str(session['user_id'])+"'"

    if required_type != None:
        if required_type == "request_sent":
            query = "select * from user where user_id  in (select to_user_id from friend_request where from_user_id='"+str(session['user_id'])+"')  and user_id != '"+str(session['user_id'])+"'"
        elif required_type == "request_received":
            query = "select * from user where user_id in (select from_user_id from friend_request where to_user_id='"+str(session['user_id'])+"')  and user_id != '"+str(session['user_id'])+"'"
    cursor.execute(query)
    users = cursor.fetchall()
    conn.commit()
    return render_template("get_users.html",users=users,get_request_status_by_user_id=get_request_status_by_user_id)


@app.route("/requests")
def requests():
    cursor.execute("select * from friend_request where from_user_id='" + str(session['user_id']) + "' or to_user_id='" + str(session['user_id']) + "' ")
    requests = cursor.fetchall()
    return render_template("requests.html", int=int,requests=requests, get_from_user_by_friend_request=get_from_user_by_friend_request,get_to_user_by_friend_request=get_to_user_by_friend_request)


def get_to_user_id_in_requests(user_id):
    count = cursor.execute("select * from friend_request where from_user_id='"+str(session['user_id'])+"' and to_user_id='"+str(user_id)+"' and status= 'Requested' ")
    conn.commit()
    return count


@app.route("/cancel_request_from_user")
def cancel_request_from_user():
    user_id = request.args.get("user_id")
    cursor.execute("delete from friend_request  where from_user_id='"+str(session['user_id'])+"' and to_user_id='"+str(user_id)+"' ")
    conn.commit()
    return redirect("/search_friends")


def get_from_user_by_friend_request(friend_request_id):
    cursor.execute("select * from user where user_id='" + str(friend_request_id) + "' ")
    users=cursor.fetchall()
    return users[0]


def get_to_user_by_friend_request(friend_request_id):
    cursor.execute("select * from user where user_id='" + str(friend_request_id) + "' ")
    users=cursor.fetchall()
    return users[0]


@app.route("/accept_request")
def accept_request():
    user_id = request.args.get("user_id")
    query = ("update friend_request set status = 'Accepted'  where (from_user_id='"+str(session['user_id'])+"' and to_user_id='"+str(user_id)+"') or  (from_user_id='" + str(user_id) + "' and to_user_id='" + str(session['user_id']) + "') ")
    cursor.execute(query)
    conn.commit()
    return redirect("/requests")


def get_request_status_by_user_id(user_id):
    query = "select * from friend_request where (from_user_id='" + str(session['user_id']) + "' and to_user_id='" + str(user_id) + "') or  (from_user_id='" + str(user_id) + "' and to_user_id='" + str(session['user_id']) + "') "
    cursor.execute(query)
    friend_requests = cursor.fetchall()
    if len(friend_requests) == 0:
        return None
    else:
        return friend_requests[0]


@app.route("/un_friend")
def un_friend():
    user_id = request.args.get("user_id")
    cursor.execute("update friend_request set status = 'UnFriend'  where (from_user_id='"+str(session['user_id'])+"' and to_user_id='"+str(user_id)+"') or  (from_user_id='" + str(user_id) + "' and to_user_id='" + str(session['user_id']) + "') ")
    conn.commit()
    return redirect("/search_friends")


@app.route("/block")
def block():
    user_id = request.args.get("user_id")
    cursor.execute("update friend_request set status = 'Blocked'  where from_user_id='"+str(session['user_id'])+"' and to_user_id='"+str(user_id)+"' ")
    conn.commit()
    return redirect("/search_friends")


@app.route("/un_block")
def un_block():
    user_id = request.args.get("user_id")
    cursor.execute("update friend_request set status = 'UnBlock'  where from_user_id='"+str(session['user_id'])+"' and to_user_id='"+str(user_id)+"' ")
    conn.commit()
    return redirect("/search_friends")


@app.route("/groups")
def groups():
    query = "select * from user_groups where (user_id='"+str(session['user_id'])+"' or user_group_id  in(select user_group_id from group_members where user_id='"+str(session['user_id'])+"'))"
    cursor.execute(query)
    user_groups = cursor.fetchall()
    return render_template("groups.html",user_groups=user_groups)


@app.route("/add_group")
def add_group():
    return render_template("add_group.html")


@app.route("/add_group_action",methods=['post'])
def add_group_action():
    group_name = request.form.get("group_name")
    image = request.files.get("image")
    description = request.form.get("description")
    path = E_commerce_files_path + "/" + image.filename
    image.save(path)
    query = "insert into user_groups(group_name,image,description,user_id)values('"+str(group_name)+"','"+str(image.filename)+"','"+str(description)+"','"+str(session['user_id'])+"')"
    cursor.execute(query)
    conn.commit()
    user_group_id = cursor.lastrowid
    cursor.execute("insert into group_members(user_group_id,user_id)values('"+str(user_group_id)+"','"+str(session['user_id'])+"')")
    conn.commit()
    return render_template("add_group.html", message="Group created successfully")


@app.route("/delete_group")
def delete_group():
    user_group_id = request.args.get("user_group_id")
    cursor.execute("delete from group_members where user_group_id= '"+str(user_group_id)+"'")
    conn.commit()
    cursor.execute("delete from user_groups where user_group_id= '"+str(user_group_id)+"'")
    conn.commit()
    return redirect("/groups")


@app.route("/view_group")
def view_group():
    user_group_id = request.args.get("user_group_id")
    query = "select * from user_groups where user_group_id ='"+str(user_group_id)+"'  "
    cursor.execute(query)
    user_groups = cursor.fetchall()
    return render_template("view_group.html", user_groups=user_groups)


@app.route("/get_group_members_by_group_id")
def get_group_members_by_group_id():
    user_group_id = request.args.get("user_group_id")
    cursor.execute("select * from user_groups where user_group_id='"+str(user_group_id)+"' ")
    group_members = cursor.fetchall()
    query2 = "select * from user where user_id!='" + str(session['user_id']) + "' and  (user_id in(select from_user_id from friend_request where to_user_id='" + str(session['user_id']) + "' and status='Accepted' ) or (user_id in(select to_user_id from friend_request where from_user_id='" + str(session['user_id']) + "' and status='Accepted')))"
    cursor.execute(query2)
    friends = cursor.fetchall()
    conn.commit()
    return render_template("get_group_members_by_group_id.html", group_members=group_members,friends=friends,user_group_id=user_group_id)


@app.route("/add_to_group")
def add_to_group():
    user_id = request.args.get("user_id")
    user_group_id = request.args.get("user_group_id")
    query = "select * from group_members where user_group_id ='"+str(user_group_id)+"' and user_id ='"+str(user_id)+"'  "
    count = cursor.execute(query)
    if count > 0:
        return {"message":"This user already Exist in this group"}
    else:
        query = "insert into group_members(user_group_id,user_id)values('"+str(user_group_id)+"','"+str(user_id)+"')"
        cursor.execute(query)
        conn.commit()
        return {"message": "Added to group"}


@app.route("/get_in_group_members_by_group_id")
def get_in_group_members_by_group_id():
    user_group_id = request.args.get("user_group_id")
    query = "select * from group_members where user_group_id ='"+str(user_group_id)+"' "
    cursor.execute(query)
    group_members = cursor.fetchall()
    return render_template("get_in_group_members_by_group_id.html",group_members=group_members,get_user_id_in_group_members=get_user_id_in_group_members)


def get_user_id_in_group_members(in_group_member_id):
    query = "select * from user where user_id = '"+str(in_group_member_id)+"' "
    cursor.execute(query)
    group_member = cursor.fetchall()
    return group_member[0]


@app.route("/remove_from_group")
def remove_from_group():
    user_group_id = request.args.get("user_group_id")
    group_member_id = request.args.get("group_member_id")
    query = "delete from group_members  where  group_member_id='" + str(group_member_id) + "' "
    cursor.execute(query)
    conn.commit()
    return {"message":'User Removed From Group'}


@app.route("/post")
def post():
    query = ("select * from post where((privacy_type='private' and user_id='"+str(session['user_id'])+"')or(privacy_type='public' and user_id='"+str(session['user_id'])+"') )or(user_id='"+str(session['user_id'])+"' or (privacy_type='public' and (user_id in(select from_user_id from friend_request where to_user_id='"+str(session['user_id'])+"'))or(user_id in (select to_user_id from friend_request where from_user_id='"+str(session['user_id'])+"') )) )or(privacy_type ='group' and user_group_id in(select user_group_id from group_members where user_id='"+str(session['user_id'])+"') )")
    cursor.execute(query)
    posts = cursor.fetchall()
    return render_template("post.html",posts=posts,get_user_id_in_post=get_user_id_in_post,str=str,get_likes_count_by_post_id=get_likes_count_by_post_id,get_comment_count_by_post_id=get_comment_count_by_post_id,get_share_count_by_post_id=get_share_count_by_post_id,is_user_liked_the_post=is_user_liked_the_post)


@app.route("/add_post")
def add_post():
    return render_template("add_post.html")


@app.route("/add_post_action", methods=['post'])
def add_post_action():
    image = request.files.get("image")
    audio = request.files.get("audio")
    video = request.files.get("video")
    description = request.form.get("description")
    privacy_type = request.form.get("privacy_type")
    group_id = request.form.get("group_id")
    print(group_id)
    if image.filename != "":
        path = posted_files_image_path + "/" + image.filename
        image.save(path)
    if audio.filename != "":
        path2 = posted_files_audio_path + "/" + audio.filename
        audio.save(path2)
    if video.filename != "":
        path3 = posted_files_video_path + "/" + video.filename
        video.save(path3)
    user_id = session['user_id']
    if group_id == None:
        query = " insert into post(image,audio,video,description,privacy_type,user_id)values('"+str(image.filename)+"','"+str(audio.filename)+"','"+str(video.filename)+"','"+str(description)+"','"+str(privacy_type)+"','"+str(user_id)+"') "
        cursor.execute(query)
        conn.commit()
    else:
        query = "insert into post(image,audio,video,description,privacy_type,user_group_id,user_id)values('" + str(image.filename) + "','" + str(audio.filename) + "','" + str(video.filename) + "','" + str(description) + "','" + str(privacy_type) + "','" + str(group_id) + "','" + str(user_id) + "') "
        cursor.execute(query)
        conn.commit()
    return render_template("add_post.html", message="Post Added successfully")


def get_user_id_in_post(post_id):
    cursor.execute("select * from user where user_id='" + str(post_id) + "' ")
    users = cursor.fetchall()
    return users[0]


@app.route("/add_comment")
def add_comment():
    post_id = request.args.get('post_id')
    comment = request.args.get('comment')
    user_id = session['user_id']
    conn.commit()
    cursor.execute("insert into comment(comment,user_id,post_id)values('"+str(comment)+"','"+str(user_id)+"','"+str(post_id)+"') ")
    conn.commit()
    return redirect("/post")


@app.route("/add_like")
def add_like():
    post_id = request.args.get('post_id')
    count = cursor.execute("select * from likes where post_id='"+str(post_id)+"' and user_id = '"+str(session['user_id'])+"'  ")
    cursor.fetchall()
    if count > 0:
        cursor.execute("delete from likes where post_id='"+str(post_id)+"' and user_id = '"+str(session['user_id'])+"' ")
        conn.commit()
    else:
        cursor.execute("insert into likes(user_id,post_id)values('"+str(session['user_id']) + "','"+str(post_id) + "') ")
        conn.commit()
    count = cursor.execute("select * from likes where post_id='"+str(post_id)+"'")
    cursor.fetchall()
    conn.commit()
    return render_template("add_like.html", count=count,post_id=post_id,is_user_liked_the_post=is_user_liked_the_post)


def is_user_liked_the_post(post_id):
    count = cursor.execute("select * from likes where post_id='"+str(post_id)+"' and user_id = '"+str(session['user_id'])+"' ")
    if count > 0:
        return True
    else:
        return False


@app.route("/get_comments")
def get_comments():
    post_id = request.args.get('post_id')
    cursor.execute("select * from comment where post_id='" + str(post_id) + "'  ")
    comments = cursor.fetchall()
    return render_template("get_comments.html",comments=comments,post_id=post_id,get_user_id_in_comment=get_user_id_in_comment)


@app.route("/share_to")
def share_to():
    post_id = request.args.get('post_id')
    print(post_id)
    user_id = session['user_id']
    cursor.execute("insert into comment(user_id,post_id)values('"+str(user_id)+"','"+str(post_id)+"') ")
    conn.commit()
    return render_template("get_shares.html")


@app.route("/get_shares")
def get_shares():
    post_id = request.args.get('post_id')
    cursor.execute("select * from share where post_id='" + str(post_id) + "'  ")
    shares = cursor.fetchall()
    user_id = session['user_id']
    cursor.execute("select * from user where  user_id in(select to_user_id from friend_request where from_user_id='" + str(user_id) + "' and status!='Requested') or user_id in(select from_user_id from friend_request where to_user_id='" + str(user_id) + "' and  status!='Requested') ")
    friends = cursor.fetchall()
    print("hello")
    return render_template("get_shares.html",shares=shares,friends=friends,post_id=post_id)


@app.route("/shared_to_friend_action")
def shared_to_friend_action():
    friend_id = request.args.get('friend_id')
    post_id = request.args.get('post_id')
    user_id = session['user_id']
    cursor.execute("insert into share(shared_by_user_id,shared_to_user_id,post_id)values('"+str(user_id)+"','"+str(friend_id)+"','"+str(post_id)+"')")
    conn.commit()
    print("ram")
    return redirect("/post")


def get_user_id_in_comment(user_id):
    query = "select * from user where user_id='"+str(user_id)+"' "
    cursor.execute(query)
    users = cursor.fetchall()
    return users[0]


@app.route("/product")
def product():
    cursor.execute(" select * from product ")
    products = cursor.fetchall()
    return render_template("product.html",products=products,get_user_id_by_product=get_user_id_by_product)


@app.route("/add_product")
def add_product():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("add_product.html", locations=locations,str=str)


@app.route("/add_product_action",methods=['post'])
def add_product_action():
    location_id = request.form.get("location_id")
    product_name = request.form.get("product_name")
    price = request.form.get("price")
    picture = request.files.get("picture")
    quantity = request.form.get("quantity")
    description = request.form.get("description")
    path = product_files_path + "/" + picture.filename
    picture.save(path)
    cursor.execute("insert into product(product_name,price,picture,quantity,description,user_id,location_id)values('" + str(product_name) + "','" + str(price) + "','" + str(picture.filename) + "','" + str(quantity) + "','"+str(description)+"','" + str(session['user_id']) + "','"+str(location_id)+"')")
    conn.commit()
    product_id = cursor.lastrowid
    cursor.execute("select * from sale_package")
    packages = cursor.fetchall()
    return render_template("view_sale_packages.html",product_id=product_id,packages=packages)


@app.route("/payments")
def payments():
    product_id = request.args.get("product_id")
    package_id = request.args.get("package_id")
    price = request.args.get("price")
    return render_template("payments.html",product_id=product_id,package_id=package_id,price=price)


def get_user_id_by_product(user_id):
    cursor.execute("select * from user where user_id ='"+str(user_id)+"' ")
    users = cursor.fetchall()
    return users[0]


@app.route("/payment_action", methods=['post'])
def payment_action():
    product_id = request.form.get("product_id")
    package_id = request.form.get("package_id")
    price = request.form.get("price")
    card_type = request.form.get("card_type")
    card_number = request.form.get("card_number")
    holder_name = request.form.get("holder_name")
    cvv_number = request.form.get("cvv_number")
    expire_date = request.form.get("expire_date")
    cursor.execute("insert into payments(totai_price,holder_name,card_type,card_number,cvv_number,expire_date,status) values('"+str(price)+"','"+str(holder_name)+"','"+str(card_type)+"','"+str(card_number)+"','"+str(cvv_number)+"','"+str(expire_date)+"','Payment Successfully')")
    conn.commit()
    cursor.execute("update product set sale_package_id='"+str(package_id)+"' where product_id = '"+str(product_id)+"' ")
    conn.commit()
    return render_template("user_message.html", message="Payment Successfully")


@app.route("/Buy_now")
def Buy_now():
    quantity = request.args.get("quantity")
    product_id = request.args.get("product_id")
    product_price = request.args.get("product_price")
    price =int(product_price)*int(quantity)
    cursor.execute("insert into orders(quantity,status,user_id,product_id)values('"+str(quantity)+"', 'Ordered' ,'"+str(session['user_id'])+"','"+str(product_id)+"')")
    conn.commit()
    order_id = cursor.lastrowid
    return render_template("product_buy_payments.html",price=price,product_id=product_id,order_id=order_id)


@app.route("/product_buy_payments_action",methods=['post'])
def product_buy_payments_action():
    product_id = request.form.get("product_id")
    order_id = request.form.get("order_id")
    price = request.form.get("price")
    card_type = request.form.get("card_type")
    card_number = request.form.get("card_number")
    holder_name = request.form.get("holder_name")
    cvv_number = request.form.get("cvv_number")
    expire_date = request.form.get("expire_date")
    cursor.execute("insert into payments(totai_price,holder_name,card_type,card_number,cvv_number,expire_date,status,order_id) values('" + str(price) + "','" + str(holder_name) + "','" + str(card_type) + "','" + str(card_number) + "','" + str(cvv_number) + "','" + str(expire_date) + "','Payment Successfully','"+str(order_id)+"')")
    conn.commit()
    return render_template("user_message.html", message="Payment Successfully")


@app.route("/orders")
def orders():
    cursor.execute("select * from orders where user_id='"+str(session['user_id'])+"' ")
    orders = cursor.fetchall()
    return render_template("orders.html",orders=orders,get_product_id_in_orders=get_product_id_in_orders,get_user_id_by_product=get_user_id_by_product)


def get_product_id_in_orders(product_id):
    cursor.execute("select * from product where product_id='"+str(product_id)+"' ")
    products = cursor.fetchall()
    return products[0]


def get_user_id_in_orders(order_id):
    cursor.execute("select * from user where user_id='"+str(order_id)+"' ")
    users = cursor.fetchall()
    return users[0]


@app.route("/view_payments")
def view_payments():
    order_id = request.args.get("order_id")
    cursor.execute("select * from payments where order_id='"+str(order_id)+"' ")
    payments = cursor.fetchall()
    return render_template("view_payments.html",payments=payments)


@app.route("/cancel_order")
def cancel_order():
    order_id = request.args.get("order_id")
    cursor.execute("update orders set status='Order Cancelled' where order_id = '" + str(order_id) + "' ")
    conn.commit()
    return render_template("user_message.html",message="Order Cancelled Successfully")


@app.route("/my_orders")
def my_orders():
    cursor.execute("SELECT * FROM orders where product_id in (select product_id from product where user_id = '"+str(session['user_id'])+"') ")
    orders = cursor.fetchall()
    return render_template("my_orders.html",orders=orders,get_product_id_in_orders=get_product_id_in_orders,get_user_id_in_orders=get_user_id_in_orders)


@app.route("/dispatch_order")
def dispatch_order():
    order_id = request.args.get("order_id")
    cursor.execute("update orders set status='Order Dispatched' where order_id = '" + str(order_id) + "' ")
    conn.commit()
    return render_template("user_message.html",message="Order Dispatched Successfully")


@app.route("/order_delivered")
def order_delivered():
    order_id = request.args.get("order_id")
    cursor.execute("update orders set status='Order Delivered' where order_id = '" + str(order_id) + "' ")
    conn.commit()
    return render_template("user_message.html",message="Order Delivered Successfully")


def get_likes_count_by_post_id(post_id):
    count = cursor.execute("select * from likes where post_id='" + str(post_id) + "'  ")
    cursor.fetchall()
    return count


def get_comment_count_by_post_id(post_id):
    count = cursor.execute("select * from comment where post_id='" + str(post_id) + "'  ")
    cursor.fetchall()
    return count


def get_share_count_by_post_id(post_id):
    count = cursor.execute("select * from share where post_id='" + str(post_id) + "'  ")
    cursor.fetchall()
    return count


@app.route("/get_group")
def get_group():
    cursor.execute("select * from user_groups where user_id='" + str(session['user_id'])+"' ")
    groups = cursor.fetchall()
    return {"groups":groups}


@app.route("/home")
def home():
    user_id = session['user_id']
    count = cursor.execute("select * from user where  user_id in(select to_user_id from friend_request where from_user_id='" + str(user_id) + "' and status!='Requested') or user_id in(select from_user_id from friend_request where to_user_id='" + str(user_id) + "' and  status!='Requested') ")
    friends = cursor.fetchall()
    conn.commit()
    return render_template("home.html", friends=friends)


@app.route("/chat")
def chat():
    receiver_id = request.args.get('receiver_id')
    return render_template("home.html", receiver_id=receiver_id)


@app.route("/get_messages")
def get_messages():
    other_customer_id = request.args.get('other_customer_id')
    user_id = session['user_id']
    count = cursor.execute("select * from chat where (sender_id='" + str(user_id) + "' and receiver_id='"+str(other_customer_id)+"') or (sender_id='" + str(other_customer_id) + "' and receiver_id='"+str(user_id)+"') ")
    messages = cursor.fetchall()
    conn.commit()
    return {"messages": messages}


@app.route("/get_message")
def get_message():
    other_customer_id = request.args.get('other_customer_id')
    user_id = session['user_id']
    conn2 = pymysql.connect(host="localhost", user="root", password="root", db="E_commerce")
    conn2.commit()
    cursor2 = conn2.cursor()
    count = cursor2.execute("select * from chat where (sender_id='" + str(user_id) + "' and receiver_id='"+str(other_customer_id)+"' and isSenderRead='unread') or (sender_id='" + str(other_customer_id) + "' and receiver_id='"+str(user_id)+"' and isReceiverRead='unread')")
    messages = cursor2.fetchall()
    for message in messages:
        if message[1] == user_id:
            cursor2.execute("update chat set isSenderRead='read' where chat_id='" + str(message[0]) + "'")
            conn2.commit()
        elif message[2] == user_id:
            cursor2.execute("update chat set isReceiverRead='read' where chat_id='" + str(message[0]) + "'")
            conn2.commit()
    conn2.commit()
    return {"messages": messages}


@app.route("/send_messages")
def send_messages():
    other_customer_id = request.args.get('other_customer_id')
    user_id = session['user_id']
    message = request.args.get('message')
    cursor.execute("insert into chat(sender_id,receiver_id,message,isSenderRead, isReceiverRead,date) values('"+str(user_id)+"', '"+str(other_customer_id)+"', '"+str(message)+"', 'unread','unread', now())")
    conn.commit()
    return {"status": "ok"}


@app.route("/set_as_read_receiver")
def set_as_read_receiver():
    other_customer_id = request.args.get('other_customer_id')
    user_id = session['user_id']
    conn2 = pymysql.connect(host="localhost", user="root", password="root", db="E_commerce")
    conn2.commit()
    cursor2 = conn2.cursor()
    count = cursor2.execute("update chat set isReceiverRead='read' where sender_id='" + str(other_customer_id) + "' and receiver_id='"+str(user_id)+"'")
    conn2.commit()
    return {"status": "ok"}


@app.route("/set_as_read_sender")
def set_as_read_sender():
    other_customer_id = request.args.get('other_customer_id')
    user_id = session['user_id']
    conn2 = pymysql.connect(host="localhost", user="root", password="root", db="E_commerce")
    conn2.commit()
    cursor2 = conn2.cursor()
    count = cursor2.execute("update chat set isSenderRead='read' where sender_id='" + str(user_id) + "' and receiver_id='"+str(other_customer_id)+"'")
    conn2.commit()
    print("update chat set isSenderRead='read' where sender_id='" + str(user_id) + "' and receiver_id='"+str(other_customer_id)+"'")
    return {"status": "ok"}


app.run(debug=True, port=port, host="0.0.0.0")