# measure.py - YouTube Premium (Using saved session)
from playwright.sync_api import sync_playwright
import time

def timestamp_us():
    """Returns the current timestamp in microseconds"""
    return int(time.time() * 1_000_000)

def note(msg):
    """Prints in the format expected by GMT"""
    print(f"{timestamp_us()} {msg}", flush=True)

def watch_video(page, url, duration, label):
    page.goto(url, timeout=60000, wait_until="domcontentloaded")
    
    # Accept cookies if necessary (outside the measured phase)
    for text in ['Accept all', 'Aceptar todo', 'Tout accepter']:
        try:
            page.click(f"button:has-text('{text}')", timeout=3000)
            break
        except:
            pass
    
    # Wait for the video to actually start
    time.sleep(3)
    
    note(f"START {label}")   # ← GMT records this timestamp
    time.sleep(duration)
    note(f"END {label}")     # ← GMT records this timestamp

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Tell Playwright to load your Premium session
        # Since GMT copies the files to /app, this is the path:
        context = browser.new_context(storage_state="/app/premium_state.json")
        page = context.new_page()

        watch_video(page, 
                    "https://youtu.be/8YxQLBRBpJI?si=WqOA2tSgWDM5BMKB", 
                    166, "video1")
        
        watch_video(page, 
                    "https://youtu.be/cX24KlL8klY?si=havUAEjKDooz68T_", 
                    191, "video2")
        
        watch_video(page, 
                    "https://youtu.be/Y4J_NYAQQEQ?si=BLcMRRYQMqy0-23l", 
                    186, "video3")
        context.close()
        browser.close()
        time.sleep(5)  # let powermetrics finish properly

if __name__ == "__main__":
    run()
