# **Truckbook Backend Assignment (afghani)**
**Namma Metro** 
Bengaluru Metro Rail Corporation Limited (BMRCL), a joint venture of Government of India and the State Government of Karnataka, is the agency for building, operating and expanding the
Namma Metro network. The metro connects all prominent places in the city. The metro consists of 5 lanes each indicated by the color as shown in the below map.how to reach your destination with minimum time and cost.

**Objective:**
To develop RESTful APIs using that can be utilized by mobile and web applications. The applications will satisfy the following user stories:

● User should be able to login or sign up using his phone number (no OTP or verification code required).

● User should be able to see the list of all stations for each Line.

● User should be able to choose starting and ending stations, to get the cost and minimum possible time of journey. 


**To run the project:**
Go to project directory and then run:
1) python3 run_flasked_api.py
   
      OR
   
2) gunicorn run_flasked_api:app_wsgi --preload -b `0.0.0.0:5011`


**Create new docker image for the project**

1) $ `docker build -t <container_image_name> <destination_dir>` for e.g. `docker built -t truckbookDocker-v3 .`

2) $ `docker image`s # To check running docker images

3) $ `docker run -rm -it -d -p <port_of_choice>:5011 <container_image_name>`



**Database**: 
Postgres (local)

**Descriptions of APIs and endpoints:**
1. Sign-up with phone number and password on sign-up page `0.0.0.0:5011/signup`
2. Login by entering phone number and password post sign-up and generate authentication token on `0.0.0.0:5011/login`. Note authentication token remain active for next 1 hour.
3. Get information of all stations along with respective line on page `0.0.0.0:5011/fetch_stations`
4. Get information of all intersection stations on page `0.0.0.0:5011/fetch_intersections`
5. To get information about how to reach from your starting station to destination station with minimum time (in minutes) and respective ticket cost (in INR) visit page `0.0.0.0:5011/shortest_path`. 
   Please input valid source station and destination station to get desired result.
   