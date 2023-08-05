import random
import os


class UtilityFile:
    @staticmethod
    def _line_generator(read_path):
        """
        get a line generator of a file
        :param read_path: string
        :return:
        """
        with open(read_path, 'r') as file:
            while True:
                line = file.readline()
                if line:
                    yield line
                else:
                    return

    @staticmethod
    def _line_shuffle(read_path):
        """
        first get all lines in file, then shuffle, finally save to file again.
        :param read_path: string
        :return:
        """
        # read
        with open(read_path, 'r') as file:
            info_list = file.readlines()

        # shuffle
        random.shuffle(info_list)

        # write
        with open(read_path, 'w') as file:
            for info in info_list:
                file.write(info)

    @staticmethod
    def get_file_list(directory, shuffle):
        """

        :param directory:
        :param shuffle:
        :return:
        """

        file_list = os.listdir(directory)

        if shuffle:
            random.shuffle(file_list)

        return file_list

    @staticmethod
    def get_line_generator(read_path,
                           shuffle):
        """

        :param read_path:
        :param shuffle: True: first shuffle and save, then return generator; False: return generator
        :return:
        """

        if shuffle:
            UtilityFile._line_shuffle(read_path)

        return UtilityFile._line_generator(read_path)

    @staticmethod
    def save_str_list(write_path,
                      info_list,
                      mode='w'):
        """
        save a list of info to a file
        :param write_path: string
        :param info_list: a list of info to save
        :param mode: file mode
        :return:
        """
        with open(write_path, mode) as file:
            for info in info_list:
                file.write(str(info))

    @staticmethod
    def count(count: dict = None,
              directory: str = None,
              sub_dir: bool = False):

        for root, batch_dir, batch_filename in os.walk(directory):
            for filename in batch_filename:
                suffix = os.path.splitext(filename)[1]
                if suffix in count:
                    count[suffix] += 1
                else:
                    count[suffix] = 1

            if sub_dir:
                for _dir in batch_dir:
                    count = UtilityFile.count(
                        count=count,
                        directory=root + '/' + _dir
                    )

        return count

    @staticmethod
    def dict_2_markdown(output: list = None,
                        src: dict = None,
                        rank: str = '#',
                        name: str = ''):

        output.append('\n%s %s\n' % (rank, name))

        # divide
        final = dict()
        not_final = dict()
        for key, value in src.items():
            if type(value) is not dict:
                final[key] = value
            else:
                not_final[key] = value

        # final part
        for key, value in final.items():
            output.append('- %s: %s\n' % (key, value))

        # not final part
        if len(not_final) > 0:
            for key, value in not_final.items():
                output = UtilityFile.dict_2_markdown(output, value, rank + '#', key)

        return output
