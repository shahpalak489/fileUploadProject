# fileUploadProject


<b> Prerequisites:</b>

python version: 3.7.4

Framework: Flask


<b>Getting started:</b>

To download the code repository for the first time:

git clone https://github.com/shahpalak489/fileUploadProject.git

cd fileUploadProject

python -m venv env

source env/Scripts/activate

pip install -r requirements.txt



<b>To run the development environment:</b>

python run.py

Browser: http://127.0.0.1:5005



<b>Description:</b>

Here is the description about the application.

There are total 3 sections.

1)
--> User can view the list of id and name of the companies that are already in the database.

--> User can add a new company to the database.

--> User can not add companies that are already in the database.

--> User can see updated list of companies in following table. 


2)
--> User can upload a file with the required columns like cid, cname, share_price, share_price_dt and comments.

--> File format should be CSV or TXT.

--> When user clicks on upload button, on successful upload user can view uploaded data in below table. 

--> There are multiple validations implemented.

--> if uploaded file doesn’t meet required criteria user will see toast with error message.

3)
--> User can view the latest uploadded data from the database.
