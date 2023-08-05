

import tensorflow as tf
import numpy as np

import textwrap
import re
import io
import itertools
import matplotlib
from textwrap import wrap
import re
import itertools

import matplotlib

from sklearn.metrics import confusion_matrix


class ConfusionMatrixSaverHook(tf.train.SessionRunHook):
    """
    Saves a confusion matrix as a Summary so that it can be shown in tensorboard
    """

    def __init__(self, labels, confusion_matrix_tensor_name, summary_writer):
        """Initializes a `SaveConfusionMatrixHook`.

        :param labels: Iterable of String containing the labels to print for each
                       row/column in the confusion matrix.
        :param confusion_matrix_tensor_name: The name of the tensor containing the confusion
                                             matrix
        :param summary_writer: The summary writer that will save the summary
        """
        self.confusion_matrix_tensor_name = confusion_matrix_tensor_name
        self.labels = labels
        self._summary_writer = summary_writer

    def end(self, session):
        cm = tf.get_default_graph().get_tensor_by_name(
                self.confusion_matrix_tensor_name + ':0').eval(session=session).astype(int)
        globalStep = tf.train.get_global_step().eval(session=session)
        figure = self._plot_confusion_matrix(cm)
        summary = self._figure_to_summary(figure,self.confusion_matrix_tensor_name)
        self._summary_writer.add_summary(summary, globalStep)

    def _figure_to_summary(self, fig, tag):
        """
        Converts a matplotlib figure ``fig`` into a TensorFlow Summary object
        that can be directly fed into ``Summary.FileWriter``.
        :param fig: A ``matplotlib.figure.Figure`` object.
        :return: A TensorFlow ``Summary`` protobuf object containing the plot image
                 as a image summary.
        """

        # attach a new canvas if not exists
        if fig.canvas is None:
            matplotlib.backends.backend_agg.FigureCanvasAgg(fig)

        fig.canvas.draw()
        w, h = fig.canvas.get_width_height()

        # get PNG data from the figure
        png_buffer = io.BytesIO()
        fig.canvas.print_png(png_buffer)
        png_encoded = png_buffer.getvalue()
        png_buffer.close()

        summary_image = tf.Summary.Image(height=h, width=w, colorspace=4,  # RGB-A
                                      encoded_image_string=png_encoded)
        summary = tf.Summary(value=[tf.Summary.Value(tag=tag, image=summary_image)])
        return summary

    def _plot_confusion_matrix(self, cm):
        '''
        :param cm: A confusion matrix: A square ```numpy array``` of the same size as self.labels
    `   :return:  A ``matplotlib.figure.Figure`` object with a numerical and graphical representation of the cm array
        '''
        numClasses = len(self.labels)

        fig = matplotlib.figure.Figure(figsize=(numClasses, numClasses), dpi=100, facecolor='w', edgecolor='k')
        ax = fig.add_subplot(1, 1, 1)
        ax.imshow(cm, cmap='Oranges')

        classes = [re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', x) for x in self.labels]
        classes = ['\n'.join(textwrap.wrap(l, 20)) for l in classes]

        tick_marks = np.arange(len(classes))

        ax.set_xlabel('Predicted')
        ax.set_xticks(tick_marks)
        ax.set_xticklabels(classes, rotation=-90, ha='center')
        ax.xaxis.set_label_position('bottom')
        ax.xaxis.tick_bottom()

        ax.set_ylabel('True Label')
        ax.set_yticks(tick_marks)
        ax.set_yticklabels(classes, va='center')
        ax.yaxis.set_label_position('left')
        ax.yaxis.tick_left()

        for i, j in itertools.product(range(numClasses), range(numClasses)):
            ax.text(j, i, int(cm[i, j]) if cm[i, j] != 0 else '.', horizontalalignment="center", verticalalignment='center', color="black")
        fig.set_tight_layout(True)
        return fig




def plot_confusion_matrix(correct_labels,
                          predict_labels,
                          labels,
                          title='Confusion matrix',
                          tensor_name = 'MyFigure/image',
                          normalize=False,
                          font_size=28,
                          cm=None):
  '''
  Parameters:
      correct_labels                  : These are your true classification categories.
      predict_labels                  : These are you predicted classification categories
      labels                          : This is a lit of labels which will be used to display the axix labels
      title='Confusion matrix'        : Title for your matrix
      tensor_name = 'MyFigure/image'  : Name for the output summay tensor

  Returns:
      summary: TensorFlow summary

  Other itema to note:
      - Depending on the number of category and the data , you may have to modify the figzie, font sizes etc.
      - Currently, some of the ticks dont line up due to rotations.
  '''
  if cm is None:
    cm = confusion_matrix(correct_labels, predict_labels, labels=labels)
  if normalize:
      cm = cm.astype('float')*10 / cm.sum(axis=1)[:, np.newaxis]
      cm = np.nan_to_num(cm, copy=True)
      cm = cm.astype('int')

  np.set_printoptions(precision=2)
  ###fig, ax = matplotlib.figure.Figure()

  fig = matplotlib.figure.Figure(figsize=(6, 6), dpi=96, facecolor='w', edgecolor='k')
  ax = fig.add_subplot(1, 1, 1)
  im = ax.imshow(cm, cmap='Oranges')

  classes = [re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', x) for x in labels]
  classes = ['\n'.join(wrap(l, 40)) for l in classes]

  tick_marks = np.arange(len(classes))

  ax.set_xlabel('Predicted', fontsize=font_size)
  ax.set_xticks(tick_marks)
  c = ax.set_xticklabels(classes, fontsize=int(font_size/2), rotation=-90,  ha='center')
  ax.xaxis.set_label_position('bottom')
  ax.xaxis.tick_bottom()

  ax.set_ylabel('True Label', fontsize=font_size)
  ax.set_yticks(tick_marks)
  ax.set_yticklabels(classes, fontsize=int(font_size/2), va ='center')
  ax.yaxis.set_label_position('left')
  ax.yaxis.tick_left()

  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
      ax.text(j,
              i,
              format(cm[i, j], 'd') if cm[i,j]!=0 else '.',
              horizontalalignment="center",
              fontsize=int(font_size/1.4), verticalalignment='center',
              color= "black")
  fig.set_tight_layout(True)
  summary = ConfusionMatrixSaverHook._figure_to_summary(None, fig,tag=tensor_name)
  return summary