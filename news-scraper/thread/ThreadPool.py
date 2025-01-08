import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

class ThreadPoolWithQueue:
    def __init__(self, max_workers: int = 3, task_queue: Queue = Queue()):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue = task_queue

    def submit(self, func, *args, **kwargs):
        """
        작업을 큐에 추가하고, 스레드 풀에 제출.
        """
        self.task_queue.put((func, args, kwargs))
        return self.executor.submit(self._run_task)

    def _run_task(self):
        """
        큐에서 작업을 꺼내 실행.
        """
        func, args, kwargs = self.task_queue.get()
        try:
            return func(*args, **kwargs)
        finally:
            self.task_queue.task_done()  # 작업 완료

    def get_waiting_tasks(self):
        """
        대기 중인 작업 개수 반환.
        """
        return self.task_queue.qsize()

    def shutdown(self, wait=True, clear_pending=False):
        """
        스레드 풀을 종료합니다.

        :param wait: 실행 중인 작업이 완료될 때까지 기다릴지 여부
        :param clear_pending: True일 경우 대기 중인 작업을 모두 제거
        """
        if clear_pending:
            with self.task_queue.mutex:  # Queue의 내용을 안전하게 비웁니다.
                self.task_queue.queue.clear()

        self.executor.shutdown(wait=wait)




# # 테스트 코드
# if __name__ == "__main__":
#     def task(n):
#         print(f"Task {n} 시작")
#         time.sleep(2)
#         print(f"Task {n} 완료")
#         return n
#
#     pool = ThreadPoolWithQueue(max_workers=10)
#
#     for i in range(50):
#         pool.submit(task, i + 1)
#
#     while True:
#         print(f"대기 중인 작업 개수: {pool.pending_tasks()}")
#         time.sleep(0.5)
#
#
#
#     pool.shutdown()