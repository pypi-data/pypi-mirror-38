import tensorflow as tf

class _Encoder(tf.keras.Model):

    def __init__(self, filter, kernelSize, dataFormat, stage):
        super().__init__(name='')
        batchNormAxis = 1 if dataFormat == 'channels_first' else 3
        self.encoderConv = tf.keras.layers.Conv2D(filters=filter, kernel_size=kernelSize, data_format=dataFormat, use_bias=False, name='Encoder_Conv_{}'.format(stage))
        self.encoderBatchNorm = tf.keras.layers.BatchNormalization(axis=batchNormAxis, name='Encoder_Batch_Norm_{}'.format(stage))
        self.encoderAct = tf.keras.layers.Activation('sigmoid', name='Encoder_Act_{}'.format(stage))

    def call(self, inputTensor, training=False):
        convInput = self.encoderConv(inputTensor)
        batchNormInput = self.encoderBatchNorm(convInput, training=training)
        return self.encoderAct(batchNormInput)

class _Decoder(tf.keras.Model):

    def __init__(self, filter, kernelSize, dataFormat, stage):
        super().__init__(name='')
        batchNormAxis = 1 if dataFormat == 'channels_first' else 3
        self.decoderDeconv = tf.keras.layers.Conv2DTranspose(filters=filter, kernel_size=kernelSize, data_format=dataFormat, use_bias=False, name='Decoder_Deconv_{}'.format(stage))
        self.decoderBatchNorm = tf.keras.layers.BatchNormalization(axis=batchNormAxis, name='Decoder_Batch_Norm_{}'.format(stage))
        self.decoderAct = tf.keras.layers.Activation('sigmoid', name='Decoder_Act_{}'.format(stage))

    def call(self, inputTensor, training=False):
        deconvInput = self.decoderDeconv(inputTensor)
        batchNormInput = self.decoderBatchNorm(deconvInput, training=training)
        return self.decoderAct(batchNormInput)

class AngelEncoder(tf.keras.Model):

    def __init__(self, dataFormat=None, name=None, trainable=True, endoLayer=None, kernelSizes=None, filters=None, optimiser=None, isSparse = False):
        """
        """
        super().__init__(name='')
        self.__endoLayer = endoLayer
        if endoLayer is None:
            raise ValueError('Please specify number of layers')
        if type(endoLayer) is not int:
            raise TypeError('Unknown data type. Valid values: Integer')
        validKernelSizes = ('Integer', 'Tuple', 'List of tuples')
        if kernelSizes is None:
            raise TypeError('Please specify kernel sizes. Valid format: {}'.format(validKernelSizes))
        else:
            if tuple is type(kernelSizes):
                if len(kernelSizes) == 2:
                    kernelSizes = tuple([kernelSizes]*endoLayer)
                else:
                    raise ValueError('Invalid tuple format. Only pairwise tuple allowed')
            elif list is type(kernelSizes):
                if type(kernelSizes[-1]) is tuple:
                    if len(kernelSizes) == endoLayer:
                        kernelSizes = tuple(kernelSizes)
                    else:
                        raise ValueError('Invalid kernel sizes\' depth. {} kernel sizes\' depth vs {} layers'.format(len(kernelSizes), endoLayer))
                else:
                    raise TypeError('Valid kernel sizes\' format: {}'.format(validKernelSizes))
            elif int is type(kernelSizes):
                kernelSizes = tuple([kernelSizes, kernelSizes]*endoLayer)
            else:
                raise TypeError('Unknown kernel sizes\' format. Valid format: {}'.format(validKernelSizes))

        validFilters = ('Integer', 'List of integers')
        if filters is None:
            raise TypeError('Please specify number of filters. Valid format: {}'.format(validFilters))
        else:
            if int is type(filters):
                filters = (1, ) + tuple([filters]*endoLayer)
            elif list is type(filters):
                if len(filters) == endoLayer:
                    filters = (1, ) + tuple(filters)
                elif len(filters) == endoLayer + 1:
                    filters = tuple(filters)
                else:
                    raise ValueError('Invalid filters\' number. {} filters\' number vs {} layers'.format(len(filters), endoLayer))
            else:
                raise TypeError('Unknown filters\' format. Valid format: {}'.format(validFilters))

        validDataFormat = ('channels_first', 'channels_last')
        if dataFormat not in validDataFormat:
            raise TypeError('Unknown data format: {}. Valid values: {}'.format(dataFormat, validDataFormat))

        assert len(kernelSizes) == len(filters), 'Unknown internal error. Unmatched filters and kernel size length'

        if self.__optimiser is None:
            raise ValueError('Please specify optimiser for the first run')

        self.__optimiser = optimiser
        self.__isSparse = isSparse

        def __encoder(filter, kernelSize, dataFormat, stage):
            return _Encoder(filter, kernelSize, dataFormat, stage)

        def __decoder(filter, kernelSize, dataFormat, stage):
            return _Decoder(filter, kernelSize, dataFormat, stage)

        self.__endoEncoders = tf.contrib.checkpoint.List()
        for layer, (filter, kernelSize) in enumerate(zip(filters[1:], kernelSizes)):
            self.__endoEncoders.append(__encoder(filter=filter,
            kernelSize=kernelSize, dataFormat=dataFormat, stage=layer+1))

        self.__endoDecoders = tf.contrib.checkpoint.List()
        for layer, (filter, kernelSize) in enumerate(zip(reversed(filters[:-1]), reversed(kernelSizes))):
            self.__endoDecoders.append(__decoder(filter=filter,
            kernelSize=kernelSize, dataFormat=dataFormat, stage=layer+1))
        # TODO integrate exo layers

    def __forwardPass(self, inputTensors, training, bottleneckInj=False):
        if not bottleneckInj:
            endoData = [inputTensors]
            for layer in self.__endoEncoders:
                endoData.append(layer(endoData[-1], training=training))
            encEndoData = endoData[-1]
        else:
            endoData = [inputTensors]

        for layer in self.__endoDecoders:
            endoData.append(layer(endoData[-1], training=training))

        return endoData

    def __loss(targets, outputs):
        return tf.reduce_mean(tf.squared_difference(targets, outputs, name='meanSquaredError'))

    def __KLDivergence(rhoHat, rho=0.05):
        return tf.reduce_sum(tf.add(tf.multiply(rho, tf.log(tf.div(rho, rhoHat))), tf.multiply(1.0 - rho, tf.log(tf.div(1.0 - rho, tf.subtract(1.0, rhoHat))))))

    def fit(self, dataFrame, stepCounter, logInterval=None):
        dataset = self.__makeDataset((dataFrame[:-1], dataFrame[1:]), training=True, batchSize=64)
        start = time()
        for (batch, (inputs, targets)) in enumerate(dataset):
            with tf.GradientTape(persistent=True) as tape:
                predicts = self.__forwardPass(inputs, training=True)
                mseLoss = self.__loss(targets=targets, outputs=predicts[-1])
                if self.__isSparse:
                    rhoHat = tf.squeeze(tf.reduce_mean(predicts[self.__endoLayer], axis=0))
                    kl = self.__KLDivergence(rhoHat=rhoHat)
            grads = tape.gradient(mseLoss, self.variables)
            if self.__isSparse:
                grads += tape.gradient(tf.multiply(0.001, kl), self.variables)
            self.__optimiser.apply_gradients(zip(grads, self.variables))
            tape.reset()
            if logInterval and batch % logInterval == 0:
                rate = logInterval / (time() - start)
                print('Step #{}\tLoss: {:.6f} ({} steps/sec)'.format(batch, mseLoss, rate))
                start = time()

    def predict(self, dataFrame):
        dataset = self.__makeDataset(dataFrame, training=True, batchSize=1)
        predictions = []
        for inputs in dataset:
            predicts = self.__forwardPass(inputs, training=False)
            predictions.append(predicts[-1])
        return predictions

    def __makeDataset(dataFrame, training=False, batchSize=1):
        def __parse_dataset(input, target):
            inputTranspose = tf.transpose(input)
            targetTranspose = tf.transpose(target)
            return tf.expand_dims(inputTranspose, axis=0), tf.expand_dims(targetTranspose, axis=0)
        dataset = tf.data.Dataset.from_tensor_slices(dataFrame)
        dataset = dataset.map(__parse_dataset)
        if training:
            dataset = dataset.shuffle(buffer_size=60000)
        dataset = dataset.batch(batch_size=batchSize)
        return dataset