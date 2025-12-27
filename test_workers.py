
import sys
import logging
from PySide6.QtCore import QCoreApplication, QThread, QTimer, Slot
from src.workers import DataLoadWorker, MapGenerationWorker
from src.models.camera import Camera

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestWorkers")

app = QCoreApplication(sys.argv)


# Global refs to prevent GC
current_thread = None
current_worker = None

def test_data_load_worker():
    global current_thread, current_worker
    logger.info("Testing DataLoadWorker...")
    
    current_thread = QThread()
    current_worker = DataLoadWorker()
    current_worker.moveToThread(current_thread)
    
    def on_finished(success, cameras):
        logger.info(f"Data Load Finished: success={success}, count={len(cameras)}")
        if success:
            logger.info("Starting MapGenerationWorker test...")
            QTimer.singleShot(1000, lambda: test_map_generation_worker(cameras[:10]))
        else:
            logger.error("Data load failed!")
            app.quit()
            
    current_thread.started.connect(current_worker.run)
    current_worker.finished.connect(on_finished)
    # Don't quit thread immediately here, wait for next step or cleanup
    current_worker.finished.connect(current_thread.quit)
    current_thread.finished.connect(current_worker.deleteLater)
    current_thread.finished.connect(current_thread.deleteLater)
    
    current_thread.start()

def test_map_generation_worker(cameras):
    global current_thread, current_worker
    logger.info("Testing MapGenerationWorker...")
    
    current_thread = QThread()
    current_worker = MapGenerationWorker(cameras, show_districts=True)
    current_worker.moveToThread(current_thread)
    
    def on_finished(path, summary):
        logger.info(f"Map Generation Finished. Path: {path}")
        logger.info("All tests passed!")
        app.quit()
        
    def on_error(msg):
        logger.error(f"Map Generation Error: {msg}")
        app.quit()
        
    current_thread.started.connect(current_worker.run)
    current_worker.finished.connect(on_finished)
    current_worker.error.connect(on_error)
    current_worker.finished.connect(current_thread.quit)
    current_worker.error.connect(current_thread.quit)
    
    current_thread.start()


# Start after a short delay
QTimer.singleShot(100, test_data_load_worker)

sys.exit(app.exec())
