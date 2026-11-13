import sys
from playwright.sync_api import sync_playwright

def update_cheesefork():
    try:
        with sync_playwright() as p:
            print("1. Launching headless browser...")
            context = p.chromium.launch_persistent_context(
                user_data_dir="./temp_chrome_profile",
                headless=True,
                viewport={'width': 1920, 'height': 1080}
            )

            page = context.pages[0]
            page.goto("https://cheesefork.cf")

            print("2. Waiting 3 seconds for the page's JavaScript to fully load...")
            page.wait_for_timeout(3000)

            print("3. Verifying login session...")
            try:
                # Look for the Logout button to confirm the session is alive
                page.get_by_text("יציאה").wait_for(state="visible", timeout=10000)
                print("Session is valid.")
            except Exception:
                # If it times out looking for 'יציאה', the token is dead
                raise Exception("SESSION_EXPIRED: You need to run the login script on Chaos again.")

            print("4. Clicking the iCalendar button...")
            button = page.get_by_text("iCalendar")
            button.wait_for(state="visible", timeout=10000)
            button.click(force=True)

            print("5. Waiting 5 seconds for the background sync to complete...")
            page.wait_for_timeout(5000)

            context.close()
            print("Update finished successfully!")
            sys.exit(0)

    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_cheesefork()
