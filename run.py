import os
import subprocess

# Put your info between the ' '
os.environ['CALCENTRAL_USERNAME'] = 'your_username'
os.environ['CALCENTRAL_PASSWORD'] = 'your_password'

# your hostnames are the words after pollev.com/ 
# examples: pollev.com/your_hostname1, pollev.com/your_hostname2
os.environ['POLLEV_HOSTNAMES'] = 'your_hostname1, your_hostname2'

subprocess.run(['python', 'main.py'], env=os.environ)