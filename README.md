# **TruckbookBackendAssignment_githubrepo**
Namma Metro (Bangalore Metro), how to reach your destination with minimum time and cost.
To run the project:
Go to project directory and then run:
1) python3 run_flasked_api.py
      OR
2) gunicorn run_flasked_api:app_wsgi --preload -b `0.0.0.0:5011`

**Create new docker image for the project**

1) $ docker built -t <container_image_name> <destination_dir> for e.g. >>>  docker built -t truckbookDocker-v3 .

2) $ docker images # To check running docker images

3) $ docker run -rm -it -d -p <port_of_choice>:5011 <container_image_name>



**Database**: 
Postgres (local)


1. Sign-up with phone number and password on sign-up page `0.0.0.0:5011/signup`
2. Login by entering phone number and password post sign-up and generate authentication token on `0.0.0.0:5011/login`. Note authentication token remain active for next 1 hour.
3. Get information of all stations alongwith respective line on page `0.0.0.0:5011/fetch_stations`
4. Get information of all intersection stations on page `0.0.0.0:5011/fetch_intersections`
5. To get information about how to reach from your starting station to destination station with minimum time and respective ticket cost visit page `0.0.0.0:5011/shortest_path`. 
   Please input source station and destination.