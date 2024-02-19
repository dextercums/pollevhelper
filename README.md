# pollevhelper
We know using pollev is very difficult: **pollevhelper** helps you respond to polls on pollev!

**pollevhelper** was developed in python3.11
## Usage
if you don't have python, download [python](https://www.python.org/downloads/) (the most recent version is fine)

Open terminal / command prompt

```
git clone https://github.com/dextercums/pollevhelper.git
cd pollevhelper
pip install -r requirements.txt
```

Open `run.py` which is located inside the pollevhelper folder   

Add your calcentral username, calcentral password, and pollev host names within the apostrophes  
For example, if your pollev link was pollev.com/dexter , then it would look like this 
```
    os.environ['CALCENTRAL_USERNAME'] = 'your_username'
    os.environ['CALCENTRAL_PASSWORD'] = 'your_password'
    os.environ['POLLEV_HOSTNAMES'] = 'dexter'
```

Then to run the helper:
```
python run.py
```

The helper will open a browser so you can see everything that it does.  

The first time you use the helper, you have to do 2 factor authentication for CalCentral.  

The helper will automatically close after two hours. or you can close it manually 



## Dependencies
[playwright](https://pypi.org/project/playwright/)

