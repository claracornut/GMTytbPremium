# measure.py - YouTube Premium (Using saved session)
from playwright.sync_api import sync_playwright
import time

def timestamp_us():
    """Retourne le timestamp actuel en microsecondes"""
    return int(time.time() * 1_000_000)

def note(msg):
    """Print dans le format attendu par GMT"""
    print(f"{timestamp_us()} {msg}", flush=True)

def watch_video(page, url, duration, label):
    page.goto(url, timeout=60000, wait_until="domcontentloaded")
    
    # Accepter les cookies si nécessaire (hors phase mesurée)
    for text in ['Accept all', 'Aceptar todo', 'Tout accepter']:
        try:
            page.click(f"button:has-text('{text}')", timeout=3000)
            break
        except:
            pass
    
    # Attendre que la vidéo démarre vraiment
    time.sleep(3)
    
    note(f"START {label}")   # ← GMT enregistre ce timestamp
    time.sleep(duration)
    note(f"END {label}")     # ← GMT enregistre ce timestamp

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Tell Playwright to load your Premium session
        # Since GMT copies the files to /app, this is the path:
        context = browser.new_context(storage_state="/app/premium_state.json")
        page = context.new_page()

        watch_video(page, 
                    "https://youtu.be/8YxQLBRBpJI?si=WqOA2tSgWDM5BMKB", 
                    161, "video1")
        
        watch_video(page, 
                    "https://youtu.be/cX24KlL8klY?si=havUAEjKDooz68T_", 
                    186, "video2")
        
        watch_video(page, 
                    "https://youtu.be/Y4J_NYAQQEQ?si=BLcMRRYQMqy0-23l", 
                    181, "video3")
        context.close()
        browser.close()

if __name__ == "__main__":
    run()
