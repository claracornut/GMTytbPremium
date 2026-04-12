# measure.py - YouTube Premium (Using saved session)
from playwright.sync_api import sync_playwright
import time
import subprocess

def phase_start(name):
    """Signal à GMT que la phase commence"""
    subprocess.run(["echo", f"[PHASE: {name}]"])

def phase_end(name):
    """Signal à GMT que la phase se termine"""
    subprocess.run(["echo", f"[PHASE-END: {name}]"])

def watch_video(page, url, duration, phase_name):
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
    
    # ---- DÉBUT DE LA PHASE MESURÉE ----
    phase_start(phase_name)
    time.sleep(duration)
    phase_end(phase_name)
    # ---- FIN DE LA PHASE MESURÉE ----

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
