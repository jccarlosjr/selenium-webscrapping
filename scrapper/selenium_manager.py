# scrapper/selenium_manager.py
import threading
import queue
import time

from selenium.common.exceptions import WebDriverException

from .selenium_driver import init_driver, close_driver
from .utils import search_by_cpf, login


task_queue = queue.Queue()
driver_lock = threading.Lock()
worker_started = False

IDLE_TIMEOUT = 300  # 5 minutos
last_activity = None


def selenium_worker():
    """
    Worker único:
    - consome a fila
    - reutiliza o driver
    - encerra após 5 min inativo
    """
    global last_activity

    driver = None

    while True:
        try:
            # aguarda tarefa ou timeout
            cpf, callback = task_queue.get(timeout=5)
        except queue.Empty:
            # verifica inatividade
            if driver and last_activity and (time.time() - last_activity > IDLE_TIMEOUT):
                with driver_lock:
                    close_driver()
                    driver = None
                    last_activity = None
            continue

        with driver_lock:
            try:
                if not driver:
                    driver = init_driver()

                try:
                    resultado = search_by_cpf(driver, cpf)
                except WebDriverException:
                    login(driver)
                    resultado = search_by_cpf(driver, cpf)

                last_activity = time.time()
                callback(resultado, None)

            except Exception as e:
                callback(None, e)

        task_queue.task_done()
        time.sleep(1)  # respiro para o site


def start_worker():
    global worker_started

    if worker_started:
        return

    thread = threading.Thread(
        target=selenium_worker,
        daemon=True
    )
    thread.start()
    worker_started = True
