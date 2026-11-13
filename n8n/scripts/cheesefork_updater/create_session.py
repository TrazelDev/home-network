from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="./temp_chrome_profile",
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )

    page = context.pages[0]
    page.goto("https://cheesefork.cf")

    print("\n--- ACTION REQUIRED ---")
    print("1. Log in with your Google account in the browser.")
    print("2. Wait until you can see your Cheesefork timetable.")
    
    # Wait for manual terminal input instead of a browser close event
    input("3. ONCE LOGGED IN, PRESS [ENTER] RIGHT HERE IN THIS TERMINAL...\n")

    # Extract the state while the browser is still alive
    context.storage_state(path="auth.json")
    
    # Now the script can safely close the browser itself
    context.close()

    print("Session saved to auth.json successfully.")
