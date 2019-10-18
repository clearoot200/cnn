import glob
import numpy as np
from keras import optimizers,regularizers
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.utils.np_utils import to_categorical
from keras.utils import np_utils
from keras.preprocessing import image
from keras.preprocessing.image import array_to_img, img_to_array, load_img, ImageDataGenerator
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras import backend as K
from PIL import Image

# 画像のサイズ
imageLength = 64
imageDimension = 3
imageSize = (imageLength, imageLength)
# 増やす画像の数
augmentation = 30

# 画像データを格納するリスト
inputData = []
labelData = []

dataGenerator = ImageDataGenerator(
            rotation_range=35,
            width_shift_range=0.05,
            height_shift_range=0.05,
            # shear_range=0.95,
            zoom_range=0.1,
            horizontal_flip=True,
            channel_shift_range=20
          )

# モデルの各係数
convFilter = 32      # CNNのフィルタ数
kernel = 3               # フィルタのサイズ
pool = (2,2)           # poolのサイズ
dropout = 0.25     # ドロップアウト率
neuron = 15          # ニューロン数
output = 3             # 分類するクラスの数
learningRate = 0.0075 # 学習係数
        
# 学習の係数
epoch = 10 # エポック数
batch = 32 #バッチサイズ

# データを読み込むクラス
class ImageSet:
    def __init__(self, filePath, labelNum):
        self.filePath = filePath #データのファイルパス
        self.labelNum = labelNum #ラベル の番号
        self.dataSet = []
        self.labelSet = []
        
    def getDataSet(self):
        return self.dataSet
    
    def getLabelSet(self):
        return self.labelSet
    
    # 画像をロードするメンバ関数
    def loadImage(self):
        for image in glob.glob(self.filePath):
            self.imageData = img_to_array(load_img(image, target_size=imageSize))
            self.dataSet.append(self.imageData)
            self.labelSet.append(self.labelNum)
     
    # 画像を増やすメンバ関数
    def dataAugmentation(self, augmentationNum):
        if augmentationNum <= 0:
            return
        
        self.dataSetBeforeAugmentation = self.dataSet[:]
        for image in self.dataSetBeforeAugmentation:
            self.imageData = image.reshape((1,) + image.shape)
            
            self.i = 0
            for augmentationData in dataGenerator.flow(self.imageData, batch_size=1):
                self.dataSet.append(augmentationData.reshape(augmentationData.shape[1],augmentationData.shape[2],augmentationData.shape[3]))
                self.labelSet.append(self.labelNum)
                self.i = self.i + 1
                if (self.i % augmentationNum) == 0:
                    break

# 学習モデルを定義するクラス
class NeuralNetwork:
    def __init__(self, convFilter, kernel, pool, dropout, neuron, output, inputShape,learningRate, epoch, batch, inputTrain, labelTrain, inputTest, labelTest):
        # モデルの各係数
        self.filter = convFilter
        self.kernel = kernel
        self.pool = pool
        self.dropout = dropout
        self.neuron = neuron
        self.output = output
        self.inputShape = inputShape
        self.learningRate = learningRate
        
        # 学習の係数
        self.epoch = epoch
        self.batch = batch
        
        #学習データ
        self.inpuTrain = inputTrain
        self.labelTrain = labelTrain
        self.inpuTest = inputTest
        self.labelTest = labelTest
    
    # モデルの定義
    def createModel(self):
        self.model = Sequential()
        
        # 畳み込み
        self.model.add(Conv2D(self.filter, kernel_size=self.kernel,padding='same',activation='relu',input_shape=self.inputShape))
        self.model.add(Conv2D(self.filter, kernel_size=self.kernel,padding='same',activation='relu'))
        self.model.add(MaxPooling2D(pool_size=pool))
        self.model.add(Dropout(0.5))
        self.model.add(Flatten())
            
        #  中間層
        self.model.add(Dense(self.neuron, activation='relu'))
        self.model.add(Dropout(self.dropout))
        self.model.add(Dense(self.neuron, activation='relu'))
        self.model.add(Dropout(self.dropout))

        # 出力層
        self.model.add(Dense(self.output, activation='softmax'))

        adagrad = optimizers.Adagrad(lr=self.learningRate)
        self.model.compile(optimizer=adagrad, loss='categorical_crossentropy',metrics=['accuracy'])
   
    # 学習の実行
    def learning(self):
        self.result = self.model.fit(inputTrain, labelTrain, epochs=self.epoch,batch_size=self.batch,validation_data=(inputTest, labelTest))
     
    # 損失関数のグラフ表示
    def showLossGraph(self):
        plt.plot(range(1, self.epoch+1), self.result.history['loss'], label="training")
        plt.plot(range(1, self.epoch+1), self.result.history['val_loss'], label="test")
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()
    
    # 正解率のグラフ表示
    def showActGraph(self):
        plt.plot(range(1, self.epoch+1), self.result.history['acc'], label="training")
        plt.plot(range(1, self.epoch+1), self.result.history['val_acc'], label="test")
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    # 画像の読み込み
    servalData = ImageSet("File Path", 0)
    lionData = ImageSet("File Path", 1)
    cheetahData = ImageSet("File Path", 2)

    servalData.loadImage()
    lionData.loadImage()
    cheetahData.loadImage()

    servalData.dataAugmentation(augmentation)
    lionData.dataAugmentation(augmentation)
    cheetahData.dataAugmentation(augmentation)

    inputData = inputData + servalData.getDataSet() + lionData.getDataSet() + cheetahData.getDataSet()
    labelData = labelData + servalData.getLabelSet() + lionData.getLabelSet() + cheetahData.getLabelSet()

    # nparrayに変換
    inputData = np.asarray(inputData)
    labelData = np.asarray(labelData)

    # データの正規化
    inputData = (inputData - np.min(inputData))/(np.max(inputData)-np.min(inputData))
    # ラベルの変換
    labelData = np_utils.to_categorical(labelData)

    # データを訓練用とテスト用に分割
    inputTrain, inputTest, labelTrain, labelTest = train_test_split(inputData, labelData,train_size=0.8)

    # kerasで扱うため形式の変換
    if K.image_dim_ordering() == 'th':
        inputTrain = inputTrain.reshape(inputTrain.shape[0], imageDimension, imageLength, imageLength)
        iinputTest = inputTest.reshape(inputTest.shape[0], imageDimension, imageLength, imageLength)
        inputShape = (imageDimension, imageLength, imageLength)
    else:
        inputTrain = inputTrain.reshape((inputTrain.shape[0], imageLength, imageLength, imageDimension))
        inputTest = inputTest.reshape((inputTest.shape[0], imageLength, imageLength, imageDimension))
        inputShape = (imageLength, imageLength, imageDimension)

    # ディープラーニングの実行
    neuralNetwork = NeuralNetwork(convFilter, kernel, pool, dropout, neuron, output, inputShape,learningRate, epoch, batch, inputTrain, labelTrain, inputTest, labelTest)

    neuralNetwork.createModel()
    neuralNetwork.learning()

    # 結果をグラフで表示
    neuralNetwork.showLossGraph()
    neuralNetwork.showActGraph()