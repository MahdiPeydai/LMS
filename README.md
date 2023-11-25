# LMS
LMS is a website that you can sell courses with different categories from different instructors.
<br>
In admin panel you can create,update and delete users. you can set groups for them and set permission for each group.
you can manage instructors and their courses. also you can set courses in different categories.
<br>
Users in web site can search for courses and filter their category,level,price and duration. Alos they can see instructors and their profile. 
Users also have a dashboard that they can manage their profile and can see their courses. Instructors can see the report of their courses.

# Development
- Django framework
- Docker
- MySQL database
- Redis
- Nginx
- Webpack


# How To Run
This application works on Docker and first you need to install < Docker Desktop >
<br>
after cloning the repo create a .env file in project directory and set these configs in it:
- SECRET_KEY
- MYSQL_ROOT_PASSWORD
- MYSQL_DATABASE
<br>
<br>
then you have to go to project directory and run docker-compose:
<br>
<br>
<code>$ docker compose build</code>
<br>
<br>
afte, to run the containers:
<br>
<br>
<code>docker compose up</code>
<br>
<br>
after containers ran successfully you need first to initialize migrations on database. To do this you need to exec mysql container and create a database:
<br>
<br>
<code>$ docker exec -it onlinelearning-mysql-1 mysql -u root -p</code>
<br>
<br>
then set database name in .env file.<br>
after that you need to exec django_app container and do migrations:
<br>
<br>
<code>$ docker exec -it onlinelearning-mysql-1 sh</code><br> 
<code>$ python3 manage.py makemigrations</code><br> 
<code>$ python3 manage.py migrate</code>
<br>
<br>
after bundle the asset files(still in django_app container):
<br>
<br>
<code>$ npm install</code>
<code>$ npm run build</code>
<br>
<br>
then you need to collect static files from apps to static folder(still in django_app container):
<br>
<br>
<code>$ python3 manage.py collectstatic</code>
<br>
(maybe you should restart nginx container to apply changes)
<br>
<br>
after you need to create a superuser for admin and it's done.
(i prefer to create admin group with all permission instead of superuser)

# Enjoy
