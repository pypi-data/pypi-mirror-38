#coding=utf-8

try:
    from hyperparameter_hunter import Environment, CrossValidationExperiment, BayesianOptimization, RandomForestOptimization
except:
    pass

try:
    from hyperparameter_hunter import Real, Integer, Categorical
except:
    pass

try:
    from hyperparameter_hunter.utils.learning_utils import get_breast_cancer_data
except:
    pass

try:
    import os.path
except:
    pass

try:
    from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
except:
    pass

try:
    from keras.layers import Dense, Activation, Dropout
except:
    pass

try:
    from keras.models import Sequential
except:
    pass

try:
    from keras.wrappers.scikit_learn import KerasClassifier
except:
    pass



def build_fn(input_shape=(10, ), params=None):
    model = Sequential(
        [
            Dense(
                params['Dense'],
                kernel_initializer="uniform",
                input_shape=input_shape,
                activation="relu",
            ),
            Dropout(params['Dropout']),
            Dense(1, kernel_initializer="uniform", activation=params['activation']),
        ]
    )
    model.compile(
        optimizer=params['optimizer'], loss="binary_crossentropy", metrics=["accuracy"]
    )
    return model
