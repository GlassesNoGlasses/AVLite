import time
import logging
import threading
import os
import watchdog

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        logging.info(f"File created: {event.src_path}")

    def on_deleted(self, event: FileSystemEvent) -> None:
        logging.info(f"File deleted: {event.src_path}")

    def on_modified(self, event: FileSystemEvent) -> None:
        logging.info(f"File modified: {event.src_path}")
    
    def on_any_event(self, event: FileSystemEvent) -> None:
        print(event)

class FileMonitor:
    def __init__(self, paths: list[str]) -> None:
        if not paths:
            raise ValueError("File paths must be provided")

        for path in paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Path {path} does not exist")
        
        self.paths = paths
        self.thread_id = 0 # original thread
        self.observers = {} # {thead_id: thread(observer)}
        self.event_handler = FileEventHandler() # event handler for file monitoring
    

    def start_monitor(self, path: str):
        ''' Start monitoring the given path '''
        observer = Observer()
        observer.schedule(self.event_handler, path, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            logging.info(f"[{threading.get_ident()}] Stopped monitoring {path}")
        observer.join()

        
    def run(self):
        ''' Start monitoring all paths '''

        for path in self.paths:
            logging.info(f"[Event] Attempting to monitor {path}...")

            thread = threading.Thread(target=self.start_monitor, args=(path,))
            thread.start()
            self.observers[thread.ident] = thread

            logging.info(f"[EVENT] Created thread ${thread.ident}; Monitoring {path}...")
        
        logging.info(f"[EVENT] Monitoring started for {len(self.paths)} paths")


    def stop_monitor(self, thread_id: int):
        pass



if __name__ == "__main__":
    import constants
    logging.basicConfig(filename=f'{constants.LOG_DIR}/file_monitor.log',
                        level=logging.INFO, 
                        format='%(asctime)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')
    