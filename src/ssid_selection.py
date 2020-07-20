import inquirer, subprocess

def select_ssid():
    '''
    Lists the reachable SSIDs to the user and asks to select the one to be cracked
    '''
    p1 = subprocess.Popen(('sudo', 'iw', 'wlan0', 'scan'), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('grep', 'SSID'), stdout=subprocess.PIPE, stdin=p1.stdout)
    out, err = p2.communicate()
    rows = out.split(b'\n')
    ssids = [row.split(b':')[1] for row in rows if len(row) > 0]

    questions = [
      inquirer.List('size',
                   message="What size do you need?",
                    choices=ssids, #['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
                ),
    ]
    return inquirer.prompt(questions)['size'].decode().strip()

answer = select_ssid()
print(answer)
