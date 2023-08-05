import logging
import datetime
import json
import os

request_id = None


class JsonLogger:
    """
	Used to create JSON formattted logs and print message to console.
	Logging level for all messages is set to INFO.
	Args:
	    file_name (str): name of the file which the logger was created in
	"""

    def __init__(self, file_name=None):
        self.file_name = file_name
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        super(JsonLogger, self).__init__()

    def _format(self, record):
        """
		Args:
			record (str): message content as readable string
		Returns:
			JSON formatted string
		"""
        data = {
            "message": record,
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "request_id": request_id,
        }
        if self.file_name:
            data["file_name"] = self.file_name
        return json.dumps(data)

    def _format_error(self, sys_info):
        """
		Args:
			record (str): expects exact arguement of sys.exc_info() as parameter
		Notes:
			exec_type - type of the exception being handled
			exc_obj - exception instance
			fname - name of file which exception occured in
		Returns: JSON formatted string:
		"""
        exc_type, exc_obj, exc_tb = sys_info
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error = exc_type, exc_obj, fname, exc_tb.tb_lineno
        return str(error)

    def log(self, message):
        """
		Prints message as JSON string to the console with the follwing format:
			{"message": "", "timestamp": "", "file_name": ""}
		Args:
			message (str): readable string description of message to be logged
		"""
        print(self._format(message))

    def log_error(self, sys_info):
        """
		Prints system information as JSON string to the console with the follwing format:
			{"message": "exc_type, exc_obj, fname, exc_tb.tb_lineno)", "timestamp": "", "file_name": ""}
		Args:
			message (str): readable string description of message to be logged
		"""
        message = self._format(self._format_error(sys_info))
        print(message)

    def set_request_id(self, id):
        """
		Sets request id to use while logging
		Args:
			request_id (str): request id to log with
		"""
        global request_id
        request_id = id
