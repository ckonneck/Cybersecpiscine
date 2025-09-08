import signal

stop_scraping = False

def signal_handler(sig, frame):
    global stop_scraping
    print("\nReceived Ctrl+C! Stopping the downloads...")
    stop_scraping = True

def register_signal():
    signal.signal(signal.SIGINT, signal_handler)
