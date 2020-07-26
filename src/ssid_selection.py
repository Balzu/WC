import inquirer, subprocess, os

def select_wireless_interface():
    '''
    Select the Wireless Network Interface to be used to crack the wireless Access Points
    '''
    p1 = subprocess.Popen(('sudo', 'iw', 'dev'), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('grep', 'Interface'), stdout=subprocess.PIPE, stdin=p1.stdout)
    out, err = p2.communicate()
    rows = out.decode().split('\n')
    wnics = [row.split('Interface')[1] for row in rows if len(row) > 0]
    return ask_question('interface', wnics)

def select_ssid(interface):
    '''
    Lists the reachable SSIDs to the user and asks to select the one to be cracked
    :param interface: Name of the interface to be used to produce the list of SSIDs
    '''
    p1 = subprocess.Popen(('sudo', 'iw', interface, 'scan'), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('grep', 'SSID'), stdout=subprocess.PIPE, stdin=p1.stdout)
    out, err = p2.communicate()
    rows = out.decode().split('\n')
    ssids = [row.split(':')[1] for row in rows if len(row) > 0]
    return ask_question('SSID', ssids)

def select_dictionaries():
    '''
    Select one of more dictionaries whose words will be used as passphrase
    to authenticate with the chosen Access Point
    '''
    dictionaries = os.listdir('../dictionaries')

def ask_question(word, alternatives, qtype='list'):
    '''
    Asks a question to the user and returns the result
    :param word: Meaning of the question
    :param alternatives: List of alternatives
    :param qtype: The type of the question: [ list | checkbox ]
    :return The asnwer to the question as a string
    '''
    if qtype == 'checkbox':
        questions = [
        inquirer.Checkbox(word,
                       message="Select the {} to be cracked".format(word),
                       choices=alternatives,                 ),
        ]
    else:
        questions = [
        inquirer.List(word,
                       message="Select the {} to be cracked".format(word),
                       choices=alternatives,                 ),
        ]
    return inquirer.prompt(questions)[word].strip()

interface = select_wireless_interface()
answer = select_ssid(interface)
print(answer)
