
import tensorflow as tf
from dlpipeline.data_loader.dataset.caching.embedding import get_random_cached_embeddings
from dlpipeline.classifier.add_layers import add_additional_retraining_nodes, add_evaluation_nodes
from dlpipeline.augmentor.embedder.hub_module import create_module_graph

def build_eval_session(module_spec,
                       class_count,
                       checkpoint_name,
                       ):
  '''Builds an restored eval session without train operations for exporting.

  Args:
    module_spec: The hub.ModuleSpec for the image module being used.
    class_count: Number of classes

  Returns:
    Eval session containing the restored eval graph.
    The embedding input, ground truth, eval step, and prediction tensors.
    :param module_spec:
    :param class_count:
    :param learning_rate:
    :param checkpoint_name:
    :param final_node_name:
  '''
  # If quantized, we need to create the correct eval graph for exporting.
  eval_graph, embedding_node, resized_input_tensor_node, quantize = (create_module_graph(module_spec))

  eval_sess = tf.Session(graph=eval_graph)
  with eval_graph.as_default():
    batch_size, embedding_size = embedding_node.get_shape().as_list()

    # Add the new layer for exporting.
    (_,
     _,
     embedding_input_node,
     ground_truth_input_node,
     output_node) = add_additional_retraining_nodes(embedding_node=embedding_node,
                                         input_size=embedding_size,
                                         output_size=class_count,
                                         batch_size=batch_size,
                                         is_training=False,
                                         quantize=quantize
                                         )

    tf.train.Saver().restore(eval_sess, checkpoint_name)  # Now we need to restore the values from the
    # training graph to the eval graph.

    evaluation_step_node, prediction_node = add_evaluation_nodes(output_node,
                                                                 ground_truth_input_node)

  return (eval_sess,
          resized_input_tensor_node,
          embedding_input_node,
          ground_truth_input_node,
          evaluation_step_node,
          prediction_node)


def run_final_eval(train_session,
                   module_spec,
                   dataset,
                   jpeg_data_node,
                   decoded_image_node,
                   resized_image_node,
                   embedding_node,
                   *,
                   checkpoint_name,
                   test_batch_size,
                   embedding_directory,
                   embedding_module,
                   print_misclassified=True,
                   **kwargs):
  '''Runs a final evaluation on an eval graph using the test data set.

  Args:
    train_session: Session for the train graph with the tensors below.
    module_spec: The hub.ModuleSpec for the image module being used.
    class_count: Number of classes
    dataset: OrderedDict of training images for each label.
    jpeg_data_node: The layer to feed jpeg image data into.
    decoded_image_node: The output of decoding and resizing the image.
    resized_image_node: The input node of the recognition graph.
    embedding_node: The embedding output layer of the CNN graph.
    :param checkpoint_name:
  '''

  (test_embeddings,
   test_ground_truth,
   test_filenames) = get_random_cached_embeddings(train_session,
                                                  dataset,
                                                  'testing',
                                                  jpeg_data_node,
                                                  decoded_image_node,
                                                  resized_image_node,
                                                  embedding_node,
                                                  embedding_module=embedding_module,
                                                  batch_size=test_batch_size,
                                                  embedding_directory=embedding_directory)

  (eval_session,
   _,
   features,
   labels,
   evaluation_step_node,
   prediction_node) = build_eval_session(module_spec,
                                    dataset.class_count,
                                    checkpoint_name)

  test_accuracy, predictions = eval_session.run([evaluation_step_node, prediction_node],
                                                feed_dict={
                                                  features:test_embeddings,
                                                  labels:  test_ground_truth
                                                  })

  tf.logging.info(f'Final test accuracy = {test_accuracy * 100:.1f}%% (N={len(test_embeddings):d})')

  if print_misclassified:
    tf.logging.info('=== Results ===')
    for i, test_filename in enumerate(test_filenames):
      if predictions[i] != test_ground_truth[i]:
        tf.logging.info(f'{test_filename:>70}  {list(dataset.keys())[predictions[i]]}')
      else:
        tf.logging.info(f'{test_filename:>70} prediction {predictions[i]} matches '
                        f'ground truth {test_ground_truth[i]}')

