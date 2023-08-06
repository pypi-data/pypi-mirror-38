import os

import tensorflow as tf
from tensorflow.python import pywrap_tensorflow

from easy_net_tf.utility.file import UtilityFile
from easy_net_tf.utility.log import UtilityLog


class UtilityModel:

    @staticmethod
    def get_variables(checkpoint_path):
        """

        :param checkpoint_path:
        :return:
        """
        reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
        var_to_shape_map = reader.get_variable_to_shape_map()

        var = dict()
        for key in var_to_shape_map:
            var['%s' % key] = reader.get_tensor(key)

        return var

    @staticmethod
    def save_checkpoint(sess,
                        new_merits,
                        save_dir,
                        net_name,
                        global_step,
                        number=5):
        """
        save a better checkpoint according to comparison of a list of merits
        :param sess:
        :param new_merits: a list of merits for comparing
        :param save_dir: Path format
        :param net_name:
        :param global_step:
        :param number: the number of model to be saved
        :return: True: a new model saved; False: new model is not saved
        """

        model_saver = tf.train.Saver()

        # .checkpoint not exist
        if (save_dir / '.checkpoint').exists() is False:

            # update .model_comparision file
            with (save_dir / '.checkpoint').open('w') as file:
                file.write('%s-%d;' % (net_name, global_step)
                           + ';'.join(map(str, new_merits))
                           + '\n')

            # save new model
            model_saver.save(
                sess=sess,
                save_path=(save_dir / net_name).__str__(),
                global_step=global_step
            )
            return True
        # .checkpoint exist
        else:
            with (save_dir / '.checkpoint').open('r') as file:
                caches = file.readlines()

            if len(caches) < number:

                # update .checkpoint file
                with (save_dir / '.checkpoint').open('a') as file:
                    file.write('%s-%d;' % (net_name, global_step)
                               + ';'.join(map(str, new_merits))
                               + '\n')

                # save new model
                model_saver.save(
                    sess=sess,
                    save_path=(save_dir / net_name).__str__(),
                    global_step=global_step
                )
                return True

            else:
                for cache_index, cache in enumerate(caches):
                    records = cache.strip().split(';')
                    old_name = records.pop(0)
                    old_merits = list(map(float, records))

                    """
                    if all new merits greater than old merits
                    """
                    replace = True
                    for i, old_merit in enumerate(old_merits):
                        if new_merits[i] < old_merit:
                            replace = False
                            break

                    if replace:
                        """
                        update .checkpoint file
                        """
                        caches[cache_index] = '%s-%d;' % (net_name, global_step) \
                                              + ';'.join(map(str, new_merits)) \
                                              + '\n'
                        UtilityFile.save_str_list(
                            write_path=(save_dir / '.checkpoint').__str__(),
                            info_list=caches,
                            mode='w'
                        )

                        """
                        delete records file
                        """
                        file_list = UtilityFile.get_file_list(
                            directory=save_dir.__str__(),
                            shuffle=False
                        )
                        for filename in file_list:
                            if filename.find(old_name) >= 0:
                                os.remove((save_dir / filename).__str__())

                        """
                        save new model
                        """
                        model_saver.save(
                            sess=sess,
                            save_path=(save_dir / net_name).__str__(),
                            global_step=global_step
                        )

                        return True

                return False

    @staticmethod
    def restore_model(sess,
                      checkpoint_path,
                      name,
                      log=False):
        """

        :param sess:
        :param checkpoint_path:
        :param name: net name
        :param log: True: print restored model path; False: not
        :return: global_step
        """
        model_saver = tf.train.Saver()
        model_saver.restore(sess=sess,
                            save_path=checkpoint_path)
        global_step = int(checkpoint_path.split('/%s-' % name).pop())

        UtilityLog.text(
            content='restore model:\n'
                    '    %s' % checkpoint_path,
            name=UtilityModel.__name__,
            tag=UtilityLog.LOG,
            option=log
        )

        return global_step
