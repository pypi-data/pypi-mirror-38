import tensorflow as tf
import numpy as np
import sys, os

sys.path.append('/home/ca1216/Gits/AngelEncoder/')

from AngelEncoder import AngelEncoder
from datetime import datetime
from sklearn import metrics
from time import time

flags = tf.app.flags
flags.DEFINE_string('dataPath', '/home/ca1216/RHData', 'Path to Data folder')
flags.DEFINE_string('modelPath', '/home/ca1216/RHResults/checkpoints', 'Path to Model folder')
flags.DEFINE_string('summaryPath', '/home/ca1216/RHResults/summary', 'Path to Summary folder')
flags.DEFINE_integer('Epoch', 100, 'How many epoch')
flags.DEFINE_integer('logInterval', 10, 'Interval to Log')
flags.DEFINE_boolean('isSparse', False, 'Sparse AutoEncoder?')
FLAGS = flags.FLAGS

def _parse_dataset(example_proto):
    features = {'data/height': tf.FixedLenFeature((), tf.int64, default_value=0),
                'data/width': tf.FixedLenFeature((), tf.int64, default_value=0),
                'data/input': tf.FixedLenFeature((), tf.string, default_value=''),
                'data/target': tf.FixedLenFeature((), tf.string, default_value='')}
    parsed_features = tf.parse_single_example(example_proto, features)
    input_raw = tf.cast(tf.decode_raw(parsed_features['data/input'], tf.uint8), tf.float32)
    target_raw = tf.cast(tf.decode_raw(parsed_features['data/target'], tf.uint8), tf.float32)
    data_shape = tf.stack([parsed_features['data/height'], parsed_features['data/width']])
    input_reshape = tf.transpose(tf.reshape(input_raw, data_shape))
    target_reshape = tf.transpose(tf.reshape(target_raw, data_shape))
    return tf.expand_dims(input_reshape, axis=0) / 255.0, tf.expand_dims(target_reshape, axis=0) / 255.0

def makeDataset():
    trainDataFiles = tf.data.Dataset.list_files(os.path.join(FLAGS.dataPath, 'train/*.record'))
    validationDataFiles = tf.data.Dataset.list_files(os.path.join(FLAGS.dataPath, 'validation/*.record'))
    trainDataset = trainDataFiles.apply(tf.contrib.data.parallel_interleave(map_func=tf.data.TFRecordDataset, cycle_length=4))
    validationDataset = validationDataFiles.apply(tf.contrib.data.parallel_interleave(map_func=tf.data.TFRecordDataset, cycle_length=4))
    trainDataset = trainDataset.shuffle(buffer_size=60000)
    trainDataset = trainDataset.apply(tf.contrib.data.map_and_batch(batch_size=512, map_func=_parse_dataset))
    validationDataset = validationDataset.apply(tf.contrib.data.map_and_batch(batch_size=256, map_func=_parse_dataset))
    return trainDataset, validationDataset

def loss(targets, outputs):
    return tf.reduce_mean(tf.squared_difference(targets, outputs, name='meanSquaredError'))

def computeRsquareds(targets, outputs):
    return [metrics.r2_score(targets[i, 0, :, :], outputs[i, 0, :, :]) for i in range(targets.shape[0])]

def KLDivergence(rhoHat, rho=0.05):
    return tf.reduce_sum(tf.add(tf.multiply(rho, tf.log(tf.div(rho, rhoHat))),
                                tf.multiply(1.0 - rho, tf.log(tf.div(1.0 - rho, tf.subtract(1.0, rhoHat))))))

def train(model, optimiser, dataset, stepCounter, logInterval=None):
    start = time()
    for (batch, (inputs, targets)) in enumerate(dataset):
        with tf.contrib.summary.record_summaries_every_n_global_steps(10, global_step=stepCounter):
            with tf.GradientTape() as tape1, tf.GradientTape() as tape2:
                predicts = model(inputs, training=True)
                mseLoss = loss(targets=targets, outputs=predicts[-1])
                tf.contrib.summary.scalar('mseLoss', mseLoss)
                tf.contrib.summary.scalar('aggregateRsquared', tf.reduce_mean(computeRsquareds(targets=targets, outputs=predicts[-1])))
                if FLAGS.isSparse:
                    rhoHat = tf.squeeze(tf.reduce_mean(predicts[3], axis=0))
                    kl = KLDivergence(rhoHat=rhoHat)
            grads = tape1.gradient(mseLoss, model.variables)
            if FLAGS.isSparse:
                grads += tape2.gradient(tf.multiply(0.001, kl), model.variables)
            optimiser.apply_gradients(zip(grads, model.variables), global_step=stepCounter)
            if logInterval and batch % logInterval == 0:
                rate = logInterval / (time() - start)
                print('Step #{}\tLoss: {:.6f} ({} steps/sec)'.format(batch, mseLoss, rate))
                start = time()

def test(model, dataset):
    avgMSELoss = tf.contrib.eager.metrics.Mean('mseLoss', dtype=tf.float32)
    aggrRsquared = tf.contrib.eager.metrics.Mean('aggregateRsquared', dtype=tf.float32)

    for (inputs, targets) in dataset:
        predicts = model(inputs, training=False)
        avgMSELoss(loss(targets=targets, outputs=predicts[-1]))
        aggrRsquared(tf.reduce_mean(computeRsquareds(targets=targets, outputs=predicts[-1])))
    print('Test set: Average loss: {:.4f}, Aggregated R-squared: {:.4f}\n'.format(avgMSELoss.result(), aggrRsquared.result()))
    with tf.contrib.summary.always_record_summaries():
        tf.contrib.summary.scalar('averageMSELoss', avgMSELoss.result())
        tf.contrib.summary.scalar('aggregateRsquared', aggrRsquared.result())

def main(_):
    
    if FLAGS.isSparse:
        print("Enabled sparse mode")
        summaryPath = FLAGS.summaryPath + '_sparse'
        modelPath = FLAGS.modelPath + '_sparse'
    else:
        summaryPath = FLAGS.summaryPath
        modelPath = FLAGS.modelPath

    trainDataset, validationDataset = makeDataset()
    model = AngelEncoder(dataFormat='channels_first', filters=[3,4,5], kernelSizes=(8,80), endoLayer=3)
    optimiser = tf.train.AdamOptimizer()

    tf.gfile.MakeDirs(summaryPath)
    trainSummaryWriter = tf.contrib.summary.create_file_writer(logdir=os.path.join(summaryPath, 'train'), flush_millis=10000, name='train')
    testSummaryWriter = tf.contrib.summary.create_file_writer(logdir=os.path.join(summaryPath, 'test'), flush_millis=10000, name='test')

    tf.gfile.MakeDirs(modelPath)
    checkpointPrefix = os.path.join(modelPath, 'ckpt')
    stepCounter = tf.train.get_or_create_global_step()
    checkpoint = tf.train.Checkpoint(model=model, optimizer=optimiser, step_counter=stepCounter)
    checkpoint.restore(tf.train.latest_checkpoint(modelPath))

    with tf.device('/gpu:0'):
        for _ in range(FLAGS.Epoch):
            start = time()
            with trainSummaryWriter.as_default():
                train(model, optimiser, trainDataset, stepCounter, FLAGS.logInterval)
            end = time()
            print('\nTrain time for epoch #{} ({} total steps): {}'.format(checkpoint.save_counter.numpy() + 1, stepCounter.numpy(), end - start))
            with testSummaryWriter.as_default():
                test(model, validationDataset)
            checkpoint.save(checkpointPrefix)

if __name__ == '__main__':
    tf.enable_eager_execution()
    tf.app.run()
