import pyperclip
from pynput import keyboard

import boto3

# Set your AWS access key ID and secret access key
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
bucket = "globalclipboard"
objkey = "comm_chan"

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)



def read_s3_file(bucket_name=bucket, object_key=objkey):
    
    try:
    
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')
        return content

    except Exception as e:
        
        print(f"Error: {e}")



def overwrite_s3_file(content, bucket_name=bucket, object_key=objkey):
    try:
        
        s3.put_object(Body=content.encode('utf-8'), Bucket=bucket_name, Key=object_key)
        print(f"File '{object_key}' in bucket '{bucket_name}' overwritten successfully.")

    except Exception as e:
        
        print(f"Error: {e}")



# Need to keep track of modifier keys separately.
# See https://github.com/moses-palmer/pynput/issues/20
alt_pressed = False


def on_press(key):
    
    global alt_pressed
        
    
    if key == keyboard.Key.alt:
        alt_pressed = True
    
    
    # Check if the read combination has been pressed.
    try:
        
        if alt_pressed and key.char.lower() == 'r':
            
            clipboard_content = read_s3_file()
            pyperclip.copy(clipboard_content)
        
        if alt_pressed and key.char.lower() == 'w':
            
            clipboard_content = pyperclip.paste()
            overwrite_s3_file(clipboard_content)
    
    except AttributeError:
        
        pass



def on_release(key):
    
    global alt_pressed    
    
    if key == keyboard.Key.alt:
        alt_pressed = False
    
    
    if key == keyboard.Key.esc:
        print("Stop event detected.")
        return False



if __name__ == "__main__":
    
    print("Listening for keyboard activity...")
    print("Press 'Alt + r' to read from the global clipboard into your clipboard.")
    print("Press 'Alt + w' to write the contents of your clipboard into the global clipboard.")
    print("Press 'Esc' to exit.")
    
    
    # Create a listener for keyboard events
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
