import paho.mqtt.client as mqtt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode

# MQTT settings
broker = "81.31.170.39"
port = 1883
topic = "Test"

# AES settings
key = b"Hardwar_Is_love "  # 16 bytes for AES-128, 24 bytes for AES-192, 32 bytes for AES-256
cipher = AES.new(key, AES.MODE_EAX)

# Connect to the MQTT broker
client = mqtt.Client()
client.connect(broker, port)

# Encrypt and publish the message
message = "Hello, MQTT with AES!"
nonce = cipher.nonce  # Unique nonce for each message
ciphertext, tag = cipher.encrypt_and_digest(message.encode("utf-8"))

# Combine the nonce, ciphertext, and tag for transmission
payload = b64encode(nonce + ciphertext + tag).decode("utf-8")
client.publish(topic, payload)
client.disconnect()
