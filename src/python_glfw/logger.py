from logging import DEBUG, Formatter, getLogger, FileHandler, StreamHandler
import sys

formatter = Formatter('%(asctime)s | %(levelname)s | %(message)s')

logger = getLogger("python_glfw")
logger.setLevel(DEBUG)

stdout_handler = StreamHandler(sys.stdout)
stdout_handler.setLevel(DEBUG)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

file_handler = FileHandler('app.log')
file_handler.setLevel(DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


