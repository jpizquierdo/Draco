import paho.mqtt.client as mqtt
import time


def on_message(client, userdata, message):
    print(
        f"received message: {message.payload} from {message.topic}"
    )  # str(message.payload.decode("utf-8"))


mqttBroker = "192.168.1.153"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker)
client.on_message = on_message

client.loop_start()

client.subscribe("home/watering/available")
client.subscribe("home/watering/waterpump")
client.subscribe("home/watering/valve1")
client.subscribe("home/watering/valve2")
client.subscribe("home/watering/valve3")
client.subscribe("home/watering/holidays")

time.sleep(90)
client.loop_stop()
