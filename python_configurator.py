
##Importing the necessary modules
import os, subprocess
from pyfiglet import Figlet

##General config
clearScreen = lambda: os.system('clear')  
custom_fig = Figlet(font='slant') ##Define the font pyfiglet will use later

clearScreen()
print(custom_fig.renderText('Nginx Configurator'))
print('Choose your option')
print('*'*15)
print("1)Install Nginx\n2)Create a Server Block\n3)Configuration")
print('*'*15)

option = int(input())
clearScreen()

if option == 1:
    os.system('apt update')
    os.system('apt install nginx')

if option == 2:
    print()
    print('What type of server block do you want to create?')
    print('*'*15)
    print("1)Main domain\n2)Sub-domain")
    print('*'*15)

    svBlock_type = int(input())
    clearScreen()

    if svBlock_type == 1:
        domain_name = input('Your domain name(example.com): ').lower()

        os.system('mkdir -p /var/www/'+domain_name)
        os.system('chown -R $USER:$USER /var/www/'+domain_name)

        sample_page = open('/var/www/'+domain_name+"/index.html", "w+")
        sample_page.write('''<html>
            <head>
                <title>Welcome to {domain}!</title>
            </head>
            <body>
                <h1>Success!  The {domain} server block is working!</h1>
            </body>
        </html>'''.format(domain=domain_name))
        sample_page.close()

        exampleCFG_file = open('cfg/sv_template', "rt")
        cfg_file = open("/etc/nginx/sites-available/{domain}".format(domain=domain_name),"wt")

        for line in exampleCFG_file:
            cfg_file.write(line.replace('example_domain', domain_name))
        
        exampleCFG_file.close()
        cfg_file.close()
        os.system('ln -s /etc/nginx/sites-available/{domain} /etc/nginx/sites-enabled/'.format(domain=domain_name))
        os.system('systemctl restart nginx')

    elif svBlock_type == 2:
        domain_name = input('Your domain name(example.com): ').lower()
        subDomain_name = input('Your sub-domain(cdn/dash...): ').lower()
        subDomain_name = subDomain_name+'.'

        os.system('mkdir -p /var/www/'+subDomain_name+domain_name)
        os.system('chown -R $USER:$USER /var/www/'+subDomain_name+domain_name)

        sample_page = open('/var/www/'+subDomain_name+domain_name+"/index.html", "w+")
        sample_page.write('''<html>
            <head>
                <title>Welcome to {domain}!</title>
            </head>
            <body>
                <h1>Success!  The {domain} server block is working!</h1>
            </body>
        </html>'''.format(domain=subDomain_name+domain_name))
        sample_page.close()

        exampleCFG_file = open('cfg/sv_subdomain_template', "rt")
        cfg_file = open("/etc/nginx/sites-available/"+subDomain_name+domain_name, "wt")

        for line in exampleCFG_file:
            cfg_file.write(line.replace('example_domain', subDomain_name+domain_name))

        exampleCFG_file.close()
        cfg_file.close()
        os.system('ln -s /etc/nginx/sites-available/{domain} /etc/nginx/sites-enabled/'.format(domain=subDomain_name+domain_name))
        os.system('systemctl restart nginx')
    
    input("Server Block added successfuly, press any key to exit")

if option == 3:
    clearScreen()
    print()
    print('Choose your option')
    print('*'*15)
    print("1)Manage Server Blocks")
    print('*'*15)

    localOption = int(input())
    clearScreen()

    if(localOption) == 1:
        raw_svBlocks = subprocess.run(("ls /etc/nginx/sites-enabled/"), shell=True, capture_output=True).stdout
        count_svBlocks = raw_svBlocks.decode("utf-8")
        count_svBlocks = count_svBlocks.split("\n")
        count_svBlocks.pop()  ##Delete the last element of the list
        
        for blocks in range(len(count_svBlocks)):
            blocks_number = blocks + 1
            print(blocks_number, end="")
            print(") "+count_svBlocks[blocks])

        input()

else:
    clearScreen()
    print("See you later👋")


