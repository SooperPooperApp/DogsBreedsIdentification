import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.inception_v3 import preprocess_input  # process_input

import numpy as np

class BreedModel:
    def loadModel(self, fileName):
        self.model = tf.keras.models.load_model(fileName)

    def loadBreed(self, fileName):
        class_file = open(fileName, "r")
        for line in class_file:
            line = line.strip()
            values = [line,1]
            self.label_list.append(values)

    def loadRateBreed(self,fileName):
        class_file = open(fileName, "r")
        for line in class_file:
            line = line.strip().split(',')
            self.label_list.append(line)

    def predict(self, img):
        # output result
        result = {'ErrCode': 0, 'ErrReason': '', 'Size': 0, 'Dogs': []}

        img = img.resize((224, 224))

        try:
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = np.expand_dims(img_array, 0)
            img_array = preprocess_input(img_array)

            predict = self.model.predict(img_array)
        except Exception:
            result['ErrorCode'] = 2001
            result['ErrReason'] = 'Need 3 chanel image'
            return result

        # sort by asc
        top = np.argsort(predict, 1)
        # truncate last result
        top = top[0][-self.dogs_size:]


        items = []
        item = {'Code': 0, 'Breed': '', 'Prob': 0, 'Rate': 1}
        for i in reversed(top):
            item['Code'] = i
            item['Breed'] = self.label_list[i][0]
            item['Rate'] = self.label_list[i][1]
            item['Prob'] = predict[0][i]
            items.append(item.copy())

        result["Size"] = len(items)
        result["Dogs"] = items
        return result

    model = 0
    label_list = []
    dogs_size = 3
