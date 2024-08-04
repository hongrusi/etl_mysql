# etl_mysql

## The main purpose 
The main purpose of this ETL pipeline is to fetch data from API, transform it usihng python and then load into a MySQL database hosted on AWS.  
VPC configuration is crucial if MySQL instance is private. This involves setting up a EC2 instance in public subnect, a private RDS in private subnet, and respective security groups inbound and outbound rules. Whether a subnet is public or private, this is purely dependednt on the associated route table. If it does allow route to Destination 0.0.0.0/0 (Target Internet Gateway), the subnect is public. The Net Access Control List and Internet Gateway should also be set up correctly and attached to the VPC. 

![etl overview](images/architecture.png)

- **Extract**: Pulling data from an external API, specifically fetching a list of universities in the United States.
- **Transform**: Manipulating the extracted data using the pandas library. This includes filtering the data to only include universities in California and converting certain list fields into comma-separated strings.
- **Load**: Saving the transformed data into a MySQL database which is hosted in Amazon RDS.

## Important note
### 1. **Amazon RDS set up**:   

**Assuming RDS instance is public accessible**
- Ensure RDS instance is in a public subnet (i.e. associated with a route to the Internet Gateway).
- The "Publicly Accessible" option must be set to "Yes" (it automatically assigned public IP address to the instance).
- The Security Group must allow inbound and outbound traffic on the MySQL port from 'My IP address'
- The NACL must allow both inbound and outbound traffic for the MySQL port and ephemeral ports.  


**Assuming RDS instance is NOT public accessible** 
- Ensure RDS instance is in a private subnet (i.e. does not associated with a route to the Internet Gateway).
- The "Publicly Accessible" option must be set to "No"  
- The Security Group of RDS includes:   
-- Inbound rules:
Allow MySQL (port 3306) from EC2 Security Group  
-- Outbound rules:
Allow all outbound traffic (0.0.0.0/0)  
(if you allow an inbound connection, the corresponding outbound traffic for that connection is automatically allowed, regardless of the outbound rules. This is called Security Group Stateful Nature)
- Set up a public EC2 instance (bastion Host) in a public subnet (associated with a route to the Internet Gateway)
- The Security Group of EC2 includes:  
-- Inbound rules:
Allow SSH (port 22) from 'MyIP' address  
-- Outbound rules:
Allow MySQL (port 3306) to RDS Security Group; Allow all outbound traffic (0.0.0.0/0)


for simplicity, allow public access to MySQL, and configure inbound and outbound rules of Security Group in VPC.  
1.1 set Inbound & Outbound rules as follow, Type = MySQL/Aurora, and Source = MyIP   

2. **Connect to MySQL Database via MySQL Workbench**： 
Assuming RDS instance is public accessible (public IP address)  
click + sign, in the pop up window, select connection method as Standard TCP (only if instance has public IP address) .  
Hostname is the Endpoint of RDS.
<img src="images/workbench.png" alt="Screenshot of the project" width="500" style="display: block; margin-left: 0;">

3.**Connect to MySQL Database in Python**: use the sqlalchemy library. Database credentials and connection paramters are contained in .env files. To avoid exposing credential, use .gitignore file to specify .env so that .env will not be committed.    


4. **Required pacakges**: ensure all necessary libraries are installed
    pip install requests pandas sqlalchemy pymysql python-dotenv
- os for operating system operations
- requests for making HTTP requests
- pandas for data manipulation
- sqlalchemy for database operations
- dotenv for loading environment variables
5. **Stop and Delete RDS** Don't forget to delete RDS after the project. It charges fees.