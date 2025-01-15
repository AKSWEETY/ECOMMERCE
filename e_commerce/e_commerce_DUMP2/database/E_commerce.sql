drop database E_commerce;
create database E_commerce;
use E_commerce;  

create table admin(
username varchar(255) not null,
password varchar(255) not null
);

create table location(
location_id  int auto_increment primary key,
location_name varchar(255) not null
);

create table sale_package(
sale_package_id  int auto_increment primary key,
pacakge_title varchar(255) not null,
no_of_customer_reach varchar(255) not null,
package_price varchar(255) not null,
validity_in_days varchar(255) not null
);



create table user(
user_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null unique,
phone varchar (255)  not null unique,
password varchar(255)not null ,
address varchar(255)not null,
gender varchar(255)not null,
profile_picture varchar(255)not null
);

create table friend_request(
friend_request_id int auto_increment primary key,
status varchar(255)not null,
requested_on datetime not null default current_timestamp,
from_user_id int,
to_user_id int,
foreign key(from_user_id) references user(user_id),
foreign key(to_user_id) references user(user_id)
);

create table product(
product_id int auto_increment primary key,
product_name varchar(255) not null,
price varchar(255) not null ,
picture varchar (255)  not null ,
quantity varchar(255)not null ,
description varchar(255)not null,
sale_package_id int,
user_id int,
location_id int,
foreign key (sale_package_id) references sale_package(sale_package_id),
foreign key (user_id) references user(user_id),
foreign key (location_id) references location(location_id)
);

create table user_groups(
user_group_id int auto_increment primary key,
group_name varchar(255) not null,
image varchar(255) not null,
description varchar(255) not null,
created_on datetime not null default current_timestamp,
user_id int,
foreign key(user_id) references user(user_id)
);


create table group_members(
group_member_id int auto_increment primary key,
user_group_id int,
user_id int,
foreign key(user_group_id) references user_groups(user_group_id),
foreign key(user_id) references user(user_id)
);



create table chat(
	chat_id int auto_increment primary key,
    sender_id int,
    receiver_id  int,
    message varchar(255),
    isSenderRead varchar(255),
	isReceiverRead varchar(255),
    date varchar(255)
);


create table post(
post_id int auto_increment primary key,
image varchar(255),
audio varchar(255),
video varchar(255),
description varchar(255) not null,
posted_on  datetime not null default current_timestamp,
privacy_type varchar(255) not null,
user_group_id int,
user_id int,
foreign key(user_group_id) references user_groups(user_group_id),
foreign key(user_id) references user(user_id)
);




create table likes(
like_id int auto_increment primary key,
liked_on datetime not null default current_timestamp,
user_id int,
post_id int,
foreign key(post_id) references post(post_id),
foreign key(user_id) references user(user_id)
);






create table share(
share_id int auto_increment primary key,
shared_on datetime not null default current_timestamp,
shared_by_user_id int,
shared_to_user_id int,
post_id int,
foreign key(post_id) references post(post_id),
foreign key(shared_by_user_id) references user(user_id),
foreign key(shared_to_user_id) references user(user_id)

);




create table comment(
comment_id int auto_increment primary key,
comment varchar(255) not null,
commented_on datetime not null default current_timestamp,
user_id int,
post_id int,
foreign key(post_id) references post(post_id),
foreign key(user_id) references user(user_id)

);




create table orders(
order_id int auto_increment primary key,
quantity varchar(255) not null,
date datetime not null default current_timestamp,
status  varchar(255) not null,
user_id int,
product_id int,
foreign key(user_id) references user(user_id),
foreign key(product_id) references product(product_id)

);

create table payments(
payment_id int auto_increment primary key,
date datetime not null default current_timestamp,
totai_price varchar(255) not null,
holder_name varchar(255) not null,
card_type varchar(255) not null,
card_number varchar(255) not null,
cvv_number varchar(255) not null,
expire_date varchar(255) not null,
status varchar(255) not null,
order_id int,
foreign key (order_id) references orders(order_id)
);



