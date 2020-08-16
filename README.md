<p align="center">
<img src="WC-logo.png" width=200>
</p>

# WC (Wi-Fi Cracker)
### __WC (Wi-Fi Cracker)__ is a security audit tool used to check the strength of Wi-Fi passwords using a Raspberry Pi. It is able to tell if a WPA/WPA2 access point is using a weak passphrase by trying to guess it via dictionary-based attacks.

### Usage
Enter _src_ folder and run `python3 cracker.py` with super user permissions.

### Extensions
You can add any dictionary to be used for password cracking by adding a file in the _dictionaries_ folder
having one word per line. The first line may start with a _#_ followed by the description of the dictionary. This description is used inside the tool when choosing among distinct dictionaries. 

### Demo

A preview of the tool is shown below, or just take a look at the video on [Youtube](https://www.youtube.com/watch?v=wSc84_jT-cA&t=8s)

<img src="wc.gif" width="100%" >
