import time
import logging
import watchdog

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, paths: list[str]) -> None:
        if not paths:
            raise ValueError("No directory paths provided")
        
        self.paths = paths


    def on_created(self, event: FileSystemEvent) -> None:
        logging.info(f"File created: {event.src_path}")

    def on_deleted(self, event: FileSystemEvent) -> None:
        logging.info(f"File deleted: {event.src_path}")

    def on_modified(self, event: FileSystemEvent) -> None:
        logging.info(f"File modified: {event.src_path}")
    
    def on_any_event(self, event: FileSystemEvent) -> None:
        print(event)


if __name__ == "__main__":
    import constants
    logging.basicConfig(filename=f'{constants.LOG_DIR}/file_monitor.log',
                        level=logging.INFO, 
                        format='%(asctime)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
