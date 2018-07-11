import os
import sys
import logging
import json


class Converter:

    def __init__(self):
        self.logger = logging.getLogger('Generator')
        self.setup_logger()
        self.output_file_name = None
        self.data = None
        self.output = {"tagGroup": [], "bookmark": []}
        self.tags_set = set()
        pass

    def convert(self, input_file_name, output_file_name):
        self.logger.info('\nInput:  [{}]\nOutput: [{}]'.format(input_file_name, output_file_name))
        self.output_file_name = output_file_name
        input_file = open(input_file_name)
        self.data = json.loads(input_file.read())
        # self.logger.debug(self.firefox_data)

        for root_child in self.data['children']:
            for child in root_child['children']:
                if 'tags' in child:
                    self.logger.debug(child['tags'])
                    self.tags_set.add(child['tags'])
        for idx, tags in enumerate(self.tags_set):
            self.logger.debug('Tag set [{}:{}]'.format(idx, tags))
            self.logger.debug('Tags:{}'.format(tags.split(',')))

            self.output['tagGroup'].append({'tags': tags.split(','), 'id': idx})

        self.save()
        return json.dumps(self.output, sort_keys=True)

    def save(self):
        with open(self.output_file_name, "w") as text_file:
            text_file.write(json.dumps(self.output, sort_keys=True))

    def setup_logger(self):
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s[%(levelname)s]: %(message)s')
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(stream_handler)
        # self.logger.setLevel(logging.INFO)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug('Logger setup')


x = Converter()
if len(sys.argv) == 1:
    print('USAGE:\n'
          '\t{0} <CATALOG_FILE_NAME> [ICONS_FOLDER]\n\n'
          'OPTIONS:\n'
          '\tICON_FOLDER\tThis directory, if specified, should contain at least one\n'
          '\t\t\tfile icon.png that will be use for all generated operator\n'
          '\t\t\tthat do not have their specific icons. Specific icon should\n'
          '\t\t\thave the following name format OPERATOR_DIR_NAME.png.\n'
          '\t\t\tExample: Pal_pal_regression_multiplelinearregression.png\n'
          'EXAMPLES:\n'
          '\t{0} catalog.json\n'
          '\t{0} catalog.json operator_icons'.format(os.path.basename(__file__)))

elif len(sys.argv) == 2:
    x.convert(sys.argv[1])
else:
    x.convert(sys.argv[1], sys.argv[2])

