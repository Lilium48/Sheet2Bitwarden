# Sheet2Bitwarden
Python-based project that copies and pastes usernames and passwords to a vault on Bitwarden. This project allows a user to seamlessly transition usernames and passwords over to bitwarden by using the Google API. 

Despite this, there are some prerequisities and understanding before you begin: 
# Notes/Prerequisites
Bitwarden has 2 different APIs: vault management & their public API. The Public API is only available for teams and enterprise level organizations. Users/Free Organizations do not have this access; however, we have a backup, the vault management, which we will use. 

The vault management api is a CLI that you install locally on an OS of your choice. Information on how to install and the api itself can be found here: https://bitwarden.com/help/cli/. Once you have this downloaded and ran, you can find out some information we will need for the script. 

The cli will tell you the folder id as that is not available in a codeless manner. Here is how to do it: 

Login into bw cli by either using your api or login.
``` bash
bw login
```
Once done, you can list the folder id for all folders for your account with the following command: 
``` bash
bw list folders
``` 
So, the other issue is how we communciate with this api. Since we are not using the public api endpoint of https://api.bitwarden.com/, we must use Bitwarden's built in serve command as an alternative. 

The Serve commmand spins up a local binding web server to a port and hostname of your choice. Once this is deployed, we can communciate with the API using RESTful requests. To spin this up, type in the following: 
``` bash 
bw serve --port 8088 --hostname localhost
```
Note: you can change port and hostname. If you run bw serve, Bitwarden binds it to port 8087. Once this is running, you can navigate to http://localhost:8088 to access this. It should say "Not Found" if successful. 

Now, you can move onto the Google API. 

First, you must create a "New Project" using the Google Console- link here: https://console.google.com- and register it. This is all free. 

Next, you must head over to "Service Accounts" and create a new key. Choose JSON and download the file. You will need to input the download path into the main script in order for it to read. 

Finally, head back to details and copy the Principal in the "Grant Access" and add it to the spreadsheet you would like to import over. 

You will need to do 2 final things before you are ready to go: 1. Install python 2. Double check and make sure that you have everything filled in on your config.ini and json_keyfile. 

# Running Sheet2Bitwarden
Once you filled in all the information you need, running Sheet2Bitwarden is as simple as running any python project. 

You will need to do the following: 

Open a new terminal and git clone Sheet2bitwarden using the following command: 
``` bash
git clone https://github.com/Kaede48/Sheet2Bitwarden.git
```
Next, 
```
cd Sheet2Bitwarden
```
Install the external packages needed: 
```
pip3 install -r requirements.txt
```
Run the python script: 
```
python Drive2Bitwarden.py
```

If everything is successful, you should see Script Execution Completed with all the users imported into the folder of your choice. 

# Closing Notes 
There is a lot more you can do with the Bitwarden Vault Management API than merely importing Usernames and Passwords. You can find more use cases with the serve server here: https://bitwarden.com/help/vault-management-api/. 

I recommend that you do this on a network that you trust since you will need to type your Bitwarden password into the config.ini file and safely store/delete all information once you finish. 

