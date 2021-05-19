import os
import configparser
import time
import json
import tensorflow as tf
import requests

config = configparser.ConfigParser()
config.read('slave.config')

BASE_URL = config['MAIN']['MASTER_URL']

print('Downloading dataset...')
def load_dataset():
    (trainX, trainY), (testX, testY) = tf.keras.datasets.cifar10.load_data()
    trainY = tf.keras.utils.to_categorical(trainY)
    testY = tf.keras.utils.to_categorical(testY)
    trainX=trainX.astype('float32')
    testX=testX.astype('float32')
    trainX = trainX / 255.0
    testX = testX / 255.0
    return trainX, trainY, testX, testY

trainX, trainY, testX, testY = load_dataset()

def create_model(lr):
    model=tf.keras.applications.MobileNetV2(input_shape=(32, 32, 3),
        alpha=1.0,
        include_top=True,
        weights=None,
        input_tensor=None,
        pooling=None,
        classes=10,
        classifier_activation="softmax"
    )

    opt = tf.keras.optimizers.Adam(learning_rate=lr)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
    return model

while True:
    files = os.listdir()
    if 'settings.json' in files:
        config.set('MAIN', 'COMPUTING', '1')
        model_config = json.loads(open('settings.json', 'r').read())
        print('Parsed job:')
        print(model_config)
        print('Starting training...')
        learning_rate = model_config['configuration']['learning_rate']
        batch_size = model_config['configuration']['batch_size']
        epochs = model_config['configuration']['epoch']
        model = create_model(learning_rate)
        history = model.fit(trainX, trainY, batch_size=batch_size, epochs=epochs, validation_split=0.37, verbose=0)
        model_config['results'] = history
        requests.post(BASE_URL+'/post_results', json=model_config)
        os.remove('settings.json')
        config.set('MAIN', 'COMPUTING', '0')
    else:
        pass
    time.sleep(0.5)
    