# For easy setup of owo-dusk.
import os
import sys
import subprocess

os.system('cls') if os.name == 'nt' else os.system('clear')
print('welcome to OwO-Dusk\nThis setup will guide you through with the setup of OwO-Dusk\nThankyou for your trust in OwO-Dusk')

"""while True:
    user_input = input("[?]Do you want help setting this up from scratch? (Y/N):-\n").lower()
    if user_input in ["y", "n"]:
        scratchSetup = True if user_input == "y" else False
        break
    else:
        print("[!]Please enter 'Y' or 'N'.")"""
scratchSetup = True
if scratchSetup:
    print('[0]Alright, got it!')

    #---INSTALL REQUIREMENTS--#
    print('[0]attempting to install requirements.txt')
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print('[0]Installed modules successfully!')
    except Exception as e:
        print("[x]error when trying to install requirements:-\n",e)

    print()
    print()

    #---CHECK VERSIONS---#
    print('[0]attempting to check versions')
    try:
        import requests
        print('[0]--imported requests module')
        #ver_check_url = "https://raw.githubusercontent.com/EchoQuill/owo-dusk/main/version.txt"
        ver_check = requests.get("https://raw.githubusercontent.com/EchoQuill/owo-dusk/main/version.txt").text.strip()
        print(f'[0]--recieved current latest version for owo-dusk on github - v{ver_check}')
        with open("version.txt", "r") as file:
            version = file.readline().strip()
        print(f'[0]current version of owo-dusk - {version}')
        if int(ver_check.replace(".","")) > int(version.replace(".","")):
            print('[0]seems like there is a new version for OwO-dusk available in GitHub')
            while True:
                o = input('Would you like to stop the installation process or continue?\n(continue = c / stop = s):\n').lower()
                
                if o in ["c", "s"]:
                    if o == "s":
                        print("[0]Stopping the installation process...")
                        sys.exit(0)
                    else:
                        print("[0]Continuing the installation process...")
                        break
                else:
                    print("[!]Please enter 'C' for continue or 'S' for stop.")
    except Exception as e:
        print("[x]error when trying to check versions:-\n",e)

    #---EDIT TOKENS.TXT---#
    print('[0]attempting to edit tokens.txt')
    try:
        """
        open('filename.txt', x)
        where if x is a then it adds while while preserving its content
        and if its w it basically selects all text...? and removes it i guess.
        -------------------------------
        'r': Read (default mode)
        'w': Write
        'a': Append
        'r+': Read and write
        """
        with open('tokens.txt', 'w') as t:
            pass
        import discord
        import asyncio
        async def validate_token(token):
            global validtoken
            try:
                client = discord.Client()

                @client.event
                async def on_ready():
                    print(f"[0] recieved token for - {client.user.name}({client.user.id})")
                    await asyncio.sleep(0.1)
                    await client.close()  # Close the client after successful login
                    return True

                await client.start(token)

            except discord.LoginFailure:
                print("[x]Invalid token provided. Please check and try again.")
                return False
            except Exception as e:
                print(f"[x]An error occurred:\n{e}")
                return False

        while True:
            token_count = input('[0]how many accounts do you want run with owo-dusk? :\n')
            try:
                token_count = int(token_count)
                break
            except ValueError:
                print('[x]please enter valid integer!')
            except Exception as e:
                print(f'[x]An error occured:-\n {e}')
        for i in range(token_count):
            while True:
                print(f'[0]token [{i+1}/{token_count}]')
                while True:
                    tokeninput = input(f'please enter your token for account #{i+1} :\n')
                    if "." in tokeninput:
                        break
                    else:
                        print('[x]invalid token!')
                while True:
                    channelinput = input(f'please enter channel id for account #{i+1} :\n')
                    try:
                        channelinput = int(channelinput)
                        break
                    except ValueError:
                        print('[x]please enter a valid integer for channelid')
                    except Exception as e:
                        print(f'[x]error while attempting to retrieve channel id -\n{e}')
                #validtoken=False
                try:
                    validtoken,validchannel=asyncio.run(validate_token(tokeninput))
                except Exception as e:
                    print(f"[x] Error validating token for account #{i+1}:\n{e}")
                if validtoken:
                    if validchannel[0]:
                        print(f'[0]valid channel with name {validchannel[1]}')
                        break
                    else:
                        print('[x]Failed to get channel id, please try again.')
            with open('tokens.txt') as t:
                t.write(f"{tokeninput} {channelinput}\n")
    except Exception as e:
        print(f'[x]error when attempting to edit tokens.txt - {e}')










"""else:
    y = input('''what would you like to do then?
1) install requirements.
2) check config.json
3) ''')"""
            