
'''
MODEL.PY
FUNCTIONS:
    create_final_layers(base_model, img_size,labels=None, optimizer=None,
     learning_rate=0.001, dropout_rate=0.5, num_gpus=1) 
        : returns completed model to train on 
    select_optimizer(optimizer=None, learning_rate=0.001) 
        : returns optomizer designated 
    load_base_model(model_name, input_shape=None, fine_tuning=None) 
        : returns base_model based model_name & img_size (h/w of image in current model 
    fine_tune_model(model, fine_tuning) 
        : sets given number of end CNN layers to not trainable   
    create_own_base_model(input_shape, pooling='avg') 
        : returns a Model() instance in Keras 
'''

import keras
from keras.layers import Input, Dense, Activation, Dropout
from keras.layers import ZeroPadding2D, MaxPooling2D, AveragePooling2D, Conv2D, BatchNormalization, Flatten
from keras.models import Model
from keras.utils.training_utils import multi_gpu_model
import time
from tensorflow.python.client import device_lib
#from tools.kt_utils import get_available_gpus
#from model import load_base_model


def create_final_layers(base_model, img_size,labels=None, optimizer=None,
                        learning_rate=0.001, dropout_rate=0.5,
                        num_gpus=1):

    """
    Inputs:
       base_model: Keras.application, this is the CNN 
                   that we will be adding too. 
       img_size: height and width to rescale our images to
       optimizer: string name of the keras optimizer to use
       learning_rate: float that determines how fast our model learns
       dropout_rate: the percent of nodes in our dropout layer to drop
    Returns:
        returns the completed model that we should then train on
    """
    
    input_shape=(img_size, img_size, 3)
    input = Input(shape=input_shape)
    output_conv = base_model(input)

    x = Dense(4096, activation='relu',
              name = 'fc_dense1')(output_conv)
    x = Dropout(dropout_rate, name='fc_dropout1')(x)
    x = Dense(2048, activation='relu',
              name = 'fc_dense2')(x)
    
    is_binary = False
    '''
    if labels == None or len(labels) == 2:
        x = Dense(1, activation='sigmoid', name='predictions')(x)
        is_binary = True
    else:
    '''
    x = Dense(len(labels), activation='softmax', name='predictions')(x)

    model = Model(inputs=input, outputs=x)

    optimizer = select_optimizer(optimizer=optimizer,
                                 learning_rate=learning_rate)

    #print("optimizer: ", str(optimizer.get_config()))
    # spread our work across num_gpus
    start = time.time()
    '''
    if num_gpus <= get_available_gpus() and num_gpus > 1:
        model = multi_gpu_model(model, gpus=num_gpus)
        print("time to spread model across multiple gpus: ", str(time.time() -
                                                                 start))
    '''
    if is_binary:
        loss = 'binary_crossentropy'
    else:
        loss = 'categorical_crossentropy'
        
    #model.compile(optimizer=optimizer, loss=loss,
                  #metrics=['accuracy'])

    return model


def select_optimizer(optimizer=None, learning_rate=0.001):
    # print("passed learning_rate: ", str(learning_rate))
    if optimizer is None:
        optimizer = keras.optimizers.Adam(lr=learning_rate)
    elif optimizer == 'sgd':
        optimizer = keras.optimizers.SGD(lr=learning_rate)
    elif optimizer == 'adam':
        optimizer = keras.optimizers.Adam(lr=learning_rate)
    elif optimizer == 'RMSProp':
        optimizer = keras.optimizers.RMSprop(lr=learning_rate)
    elif optimizer == 'adagrad':
        optimizer = keras.optimizers.Adagrad(lr=learning_rate)
    elif optimizer == 'adadelta':
        optimizer = keras.optimizers.Adadelta(lr=learning_rate)
    elif optimizer == 'adamax':
        optimizer = keras.optimizers.Adamax(lr=learning_rate)
    elif optimizer == 'nadam':
        optimizer = keras.optimizers.Nadam(lr=learning_rate)
    else:
        print("optimizer name not recognized")
        
    return optimizer


def load_base_model(model_name, input_shape=None, fine_tuning=None):
    '''
    Inputs
        model_name : The name of the model we wish to implement
        input_shape : the tensor shape of the image we wish to use on our model
    Returns
        base_model : The model created based on our model_name 
        img_size : the height and width of our image used in our current model
    '''

    if input_shape is not None:
        img_size = input_shape[0]
        
    if model_name == 'InceptionV3':
        if input_shape == None:
            img_size = 227
            input_shape = (img_size, img_size, 3)
        base_model = keras.applications.inception_v3.InceptionV3(weights='imagenet',
                                 include_top = False,
                                 input_shape=input_shape,
                                 pooling = 'avg')

    elif model_name == 'ResNet50':
        if input_shape == None:
            img_size = 224
            input_shape = (img_size, img_size, 3)
        base_model = keras.applications.resnet50.ResNet50(weights='imagenet',
                              include_top = False,
                              input_shape = input_shape,
                              pooling = 'avg')

    elif model_name == 'VGG16':
        if input_shape == None:
            img_size = 224
            input_shape = (img_size, img_size, 3)
        base_model = keras.applications.vgg16.VGG16(weights='imagenet',
                           include_top = False,
                           input_shape = input_shape,
                           pooling = 'avg')

    elif model_name == 'VGG19':
        if input_shape == None:
            img_size = 224
            input_shape = (img_size, img_size, 3)
        base_model = keras.applications.vgg19.VGG19(weights='imagenet',
                           include_top=False,
                           input_shape=input_shape,
                           pooling='avg')

    elif model_name == 'InceptionResNetV2':
        if input_shape == None:
            img_size = 299
            input_shape = (img_size, img_size, 3)
        base_model = keras.applications.inception_resnet_v2.InceptionResNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=input_shape,
            pooling='avg')

    elif model_name == 'Xception':
        if input_shape == None:
            img_size = 299
            input_shape=(img_size, img_size, 3)
        base_model = keras.applications.xception.Xception(weights='imagenet',
                              include_top = False,
                              input_shape=input_shape,
                              pooling = 'avg')

    elif model_name == 'SSUGeosciences':
        if input_shape == None:
            img_size = 299
            input_shape=(img_size, img_size, 3)
        base_model = create_own_base_model(input_shape=input_shape,
                                           pooling = 'avg')
    else:
        print("model name not recognized.")
        return

    # remove the final layer used by the CNN to then be able to append our own
    # fully connected layers
    base_model.layers.pop()
    
    print(base_model.name, ' base model with input shape',
          base_model.input_shape, ' loaded')

    fine_tune_model(base_model, fine_tuning)        
    return base_model, img_size

def fine_tune_model(model, fine_tuning):
    if fine_tuning is None:
        return

    count = 1
    for layer in reversed(model.layers):
        # exlclude all layers that are not trainable
        if layer.count_params() > 0:
            if count in fine_tuning:
                layer.trainable = True
            else:
                layer.trainable = False
            count += 1
            
    return
            
def create_own_base_model(input_shape, pooling='avg'):
    '''
    This is the ssu_geosciences CNN created specifically for this project.
    
    Arguments:
        input_shape -- shape of the images of the dataset
        pooling --(string) the type of pooling to be done. Average / Max etc 
    Returns:
        model -- a Model() instance in Keras
    References:
        Link to the resnet50 implementation in the same manner we would like emulate
        https://github.com/keras-team/keras/blob/master/keras/applications/resnet50.py
    '''

    # define the channel we use for our images
    bn_axis = 3 # we use the third param or channel_last format
    
    
    # Define the input placeholder as a tensor with shape input_shape. Think of this as your input image!
    X_input = Input(input_shape)

    # Zero-Padding: pads the border of X_input with zeros
    X = ZeroPadding2D((3,3))(X_input)

    # CONV -> BN -> RELU Block applied to X
    X = Conv2D(32, (7,7), strides = (1,1), name = 'conv0')(X)
    X = BatchNormalization(axis=bn_axis, name='bn0')(X)
    X = Activation('relu')(X)

    # pooling 
    if pooling == 'max':
        X = GlobalMaxPooling2D((2,2), name='max_pool')(X)
    elif pooling == 'avg':
        X = GlobalAveragePooling2D((2,2), name='avg_pool')(X)

    # FLATTEN X (means convert it to a vector)
    X = Flatten()(X)

    model = Model(inputs = X_input, outputs = X, name = 'SSUGeosciencesModel')
    
    return model
            
        
