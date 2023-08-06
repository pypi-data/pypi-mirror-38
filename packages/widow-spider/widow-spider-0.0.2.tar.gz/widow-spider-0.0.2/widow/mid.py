from multiprocessing import Manager


class Middleware:
    rensponce_queue = Manager().Queue()
    requests_queue = Manager().Queue()
    tasks_queue = Manager().Queue()
    faild_queue = Manager().Queue()

    @classmethod
    def judge(cls):
        if cls.requests_queue.empty() is True and cls.rensponce_queue.empty() is True \
                and cls.tasks_queue.empty() is True:
            return True
        else:
            return False
