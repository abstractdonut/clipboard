**Description**

A little script I wrote to quickly share text between different computers using keyboard shortcuts.

**Setup**

The `pynput`, `pyperclip`, and `boto3` libraries are required.

```console
pip3 install pynput
pip3 install pyperclip
pip3 install boto3
```

`pyperclip` might need extra steps, I had to install `xclip` to get working on Ubuntu. 

It uses a single hardcoded AWS S3 file to communicate between different instances. To set this up, create an AWS account, create a bucket, then create a file to designate as a communication file for the script to access. Change lines 7 through 10 of `clipboard.py` to give it access to your S3 file. You will need an AWS access key ID, an AWS secret access key, a bucket name, and a file path relative to the bucket.

See [here](https://pyperclip.readthedocs.io/en/latest/).


**Usage**

Run the script with

```console
python3 clipboard.py
```

It will begin listening for certain key combinations.

If it registers 'Alt r', it will read the contents of the S3 file into your clipboard.

If it registers 'Alt w', it will write the contents of the clipboard to the S3 file. This operation *overwrites* your file's contents.

If it registers 'Esc', the program will terminate.

I noticed that recording the keypresses correctly depends on the window focus. For example, if the focus is still on the terminal window, no keypresses are recorded. I'm not sure what causes this. I've found that it works from my browser, which is my personal use case. If you have any suggestions for improvement please send them to me.
