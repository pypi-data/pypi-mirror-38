import json


class OptionException(Exception):
    pass


class UploadConflictException(Exception):
    def __init__(self, destination_path):
        self.message = 'Conflict. File "{}" exists on remote server.'.format(destination_path)


class UploadDirConflictException(Exception):
    def __init__(self, destination_path):
        self.message = 'Conflict. Directory "{}" exists on remote server.'.format(destination_path)


class AsperaExecutableNotFound(Exception):
    message = 'Aspera executable "ascp" is not found. Please add path to "ascp" into PATH environment variable.'


class AsperaUploadFailed(Exception):
    def __init__(self, return_code):
        self.message = '"ascp" returned non successful code "{}".'.format(return_code)


class HttpClientError(Exception):
    def __init__(self, response, message, reason, **kwargs):
        self.response = response
        for key, value in kwargs.items():
            if type(value) is dict:
                kwargs[key] = json.dumps(value, sort_keys=True)
        self.message = "{} {}".format(message.format(**kwargs), reason)


class ChecksumJobTimeout(Exception):
    def __init__(self):
        self.message = (
            'Generation checksum timeout. '
            'To synchronize content please use the same command one more time.'
        )


class ChecksumJobsFailed(Exception):
    def __init__(self, failed_checksum_filenames):
        self.message = (
            'Generation checksum for files: {} {} failed. '
            'To synchronize content please use the same command one more time.'.format(
                ', '.join(failed_checksum_filenames),
                'was' if len(failed_checksum_filenames) == 1 else 'were'
            )
        )
