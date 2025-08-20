import gc
import tracemalloc
import psutil
import tensorflow as tf
from cnnclassifier import logger

class memmory_optimization:
    @staticmethod
    def get_memory():
        return psutil.Process().memory_info().rss / 1024**2

    @staticmethod
    def clean_memory(*args):
        tracemalloc.start()
        print(f"Before GC: {memmory_optimization.get_memory():.2f} MB")
        print(f"memory used by python functions before cleanup: {tracemalloc.get_traced_memory()[1]/1024**2:.2f} MB")

        for var in args:
            try:
                del var
            except Exception as e:
                logger.info(f"could not delete variable: {e}")

        tf.keras.backend.clear_session()
        collected = gc.collect()
        print(f"memory (python) after cleanup : {tracemalloc.get_traced_memory()[1]/1024**2:.2f} MB")
        print(f"memory (RAM) after gc.collect : {memmory_optimization.get_memory():.2f} MB")

        info = None
        try:
            info = tf.config.experimental.get_memory_info('GPU:0')
            print(f"Internal TensorFlow GPU memory after clear session: {info}")
        except Exception as e:
            print(f"⚠️ Could not retrieve GPU memory info: {e}")

        if info is not None:
            print(f"Internal TensorFlow memory after clear session: {info} "
                  "(use 'GPU:0' for GPU info or 'CPU:0' for CPU info)")

        logger.info(f"garbage collector cleaned up {collected} unreachable objects (TensorFlow session cleared).")
        tracemalloc.stop()
