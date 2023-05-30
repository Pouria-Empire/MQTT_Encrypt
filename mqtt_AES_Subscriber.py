import paho.mqtt.client as mqtt
from Crypto.Cipher import AES
from base64 import b64decode

# MQTT settings
broker = "188.40.23.247"
port = 1883
topic = "Test"

# AES settings
key = b"Hardwar_Is_love "  # 16 bytes for AES-128, 24 bytes for AES-192, 32 bytes for AES-256

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)

def on_message(client, userdata, msg):
    encrypted_payload = b64decode(msg.payload)

    # Extract the nonce, ciphertext, and tag from the encrypted payload
    nonce = encrypted_payload[:16]
    ciphertext = encrypted_payload[16:-16]
    tag = encrypted_payload[-16:]

    # Decrypt the message
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)
        print("Decrypted message:", decrypted_message.decode("utf-8"))
    except ValueError:
        print("Incorrect decryption")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_forever()