print("--- testCase.py execution started ---")
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, WebDriverException
import subprocess
import json
import sys
from appium.webdriver.common.touch_action import TouchAction

def get_connected_device_info():
    try:
        print("Checking for connected Android devices...")
        # Get the list of connected devices
        adb_output = subprocess.check_output(['adb', 'devices']).decode('utf-8')
        print("ADB Devices output:", adb_output)
        
        devices = adb_output.strip().split('\n')[1:]
        
        if not devices or all(not line.strip() for line in devices):
            raise Exception("No Android devices connected")
            
        # Get the first connected device
        device_id = devices[0].split('\t')[0]
        print(f"Found device with ID: {device_id}")
        
        # Get device properties
        print("Getting device properties...")
        device_name = subprocess.check_output(['adb', '-s', device_id, 'shell', 'getprop', 'ro.product.model']).decode('utf-8').strip()
        platform_version = subprocess.check_output(['adb', '-s', device_id, 'shell', 'getprop', 'ro.build.version.release']).decode('utf-8').strip()
        
        device_info = {
            "deviceId": device_id,
            "deviceName": device_name,
            "platformVersion": platform_version
        }
        print("Device info retrieved:", json.dumps(device_info, indent=2))
        return device_info
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {str(e)}")
        print(f"Command output: {e.output.decode('utf-8') if e.output else 'No output'}")
        return None
    except Exception as e:
        print(f"Error getting device info: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        return None

try:
    print("Starting the automation script...")
    
    # Get dynamic device information
    device_info = get_connected_device_info()
    if not device_info:
        print("Using default device capabilities as fallback")
        device_info = {
            "deviceId": "QV770AW4CM",
            "deviceName": "QV770AW4CM",
            "platformVersion": "12"
        }

    caps = {
        "platformName": "Android",
        "deviceName": device_info["deviceName"],
        "udid": device_info["deviceId"],
        "platformVersion": device_info["platformVersion"],
        "app": "F:/Background-Remover-FollowPath/BG Remover v1.0.5_d3.apk",
        "appPackage": "com.braincraftapps.droid.bgremover",
        "appActivity": "com.braincraftapps.droid.bgremover.ui.activity.launcher.LauncherActivity",
        "automationName": "UiAutomator2",
        "autoGrantPermissions": True,
        "noReset": False
    }

    print("Initializing with capabilities:", json.dumps(caps, indent=2))

    # Convert capabilities to UiAutomator2Options
    options = UiAutomator2Options().load_capabilities(caps)
    
    print("Connecting to Appium server...")
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
    print("Successfully connected to Appium server")

    '''Handle -- I Agree Button'''

    try:
        # Wait for the "I Agree" button (using XPath text matching)
        agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//android.widget.Button[contains(@text, "I Agree")]')
            )
        )
        agree_button.click()
        print("Clicked 'I Agree' button successfully!")
    except TimeoutException:
        print("No 'I Agree' button found (may have already been accepted).")

    '''Click Gallery button'''

    try:
        gallery_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.braincraftapps.droid.bgremover:id/gallery_button_linear_layout'))
        )
        gallery_btn.click()
        print("Clicked Gallery Button")
    except TimeoutException:
        print("Gallery Button not found")

    '''Click Folder Button'''
    folder_name = 'Skype'
    # Take a screenshot before trying to click the folder
    driver.save_screenshot("before_folder_click.png")
    # Print all visible folder names for debugging
    folders = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
    print("Visible folders:")
    for f in folders:
        try:
            print(f.text)
        except Exception as e:
            print(f"Error reading folder text: {e}")
    try:
        folder_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                AppiumBy.XPATH, f'//android.widget.TextView[contains(@text, "{folder_name}")]'))
        )
        folder_btn.click()
        print("Clicked Folder Button")
    except TimeoutException:
        print("Folder Button not found")

    '''Click an Image which one is 1st index'''
    try:
        # Wait for the recyclerview to be present first
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView'))
        )

        # Then wait for images to load (check if at least one exists)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView//android.widget.FrameLayout'))
        )

        # Now find and click the first image
        image_btn = driver.find_element(AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView//android.widget.FrameLayout[1]//android.widget.ImageView')
        image_btn.click()
        print("Successfully Click the image")
    except TimeoutException:
        print(f"Folder '{folder_name}' is empty or images didn't load!")

    # Wait for 10 seconds as requested after the process completes
    print("\nWaiting 10 seconds for image processing to finish...")
    time.sleep(10)

    '''Test Case- 1: Edit Image with Heart Shape. 
        1. Tap on the Shape Button
        2. Click Love Shapes Category
        3. Click on the Heart Shape
        4. Click Done Button'''

    '''Step 1: Tap on the Shape Button'''
    try:
        # Take a screenshot before swipe for debugging
        driver.save_screenshot("before_swipe.png")
        print("Screenshot taken before swipe.")
        # Swipe the bottom navigation bar to bring the Shape Button into view
        bottom_nav = driver.find_element(AppiumBy.ID, 'com.braincraftapps.droid.bgremover:id/bottom_nav')
        location = bottom_nav.location
        size = bottom_nav.size
        start_x = location['x'] + size['width'] - 10
        end_x = location['x'] + 10
        y = location['y'] + size['height'] // 2
        action = TouchAction(driver)
        action.press(x=start_x, y=y).wait(500).move_to(x=end_x, y=y).release().perform()
        print("Swiped bottom navigation bar to reveal Shape Button")
        # Take a screenshot after swipe for debugging
        driver.save_screenshot("after_swipe.png")
        print("Screenshot taken after swipe.")
        # Now try to click the Shape Button
        shape_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.braincraftapps.droid.bgremover:id/shape_nav_button'))
        )
        shape_btn.click()
        print("Successfully clicked Shape Button")
    except Exception as e:
        print(f"Error clicking Shape Button: {e}")
        driver.save_screenshot("shape_button_fail.png")

    '''Step 2: Click Love Shapes Category'''
    try:
        love_category_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@text="LOVE"]'))
        )
        love_category_btn.click()
        print("Successfully clicked Love Shapes Category")
    except Exception as e:
        print(f"Error clicking Love shapes category: {e}")

    '''Step 3: Click on the Heart Shape'''
    try: 
        heart_shape_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageButton[@resource-id="com.braincraftapps.droid.bgremover:id/image_button"])[3]'))
        )
        heart_shape_btn.click()
        print("Successfully clicked Heart Shape")
    except Exception as e:
        print(f"Error clicking Heart Shape: {e}")

    '''Step 4: Click Done Button'''
    try:
        done_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.braincraftapps.droid.bgremover:id/done_button'))
        )
        done_btn.click()
        print("Successfully clicked Done button")
    except Exception as e:
        print(f"Error clicking Done Button: {e}")
    
    '''Tap on the Export Button'''
    try:
        export_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.braincraftapps.droid.bgremover:id/share_button'))
        )
        export_btn.click()
        print("Successfully Click Export button")
    except TimeoutException:
        print("Button is not found")

    '''Handle Optional Review Dialog'''
    try:
        # Use a short wait time to quickly check for the dialog
        print("Checking for optional review dialog...")
        review_close_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.braincraftapps.droid.bgremover:id/close_button'))
        )
        print("Review dialog appeared, closing it.")
        review_close_btn.click()
    except TimeoutException:
        # This is expected if the dialog doesn't appear
        print("Review dialog not present, continuing...")
    
    '''Click Save to Gallery button'''
    try:
        save_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.braincraftapps.droid.bgremover:id/save_to_gallery_button"]'))
        )
        save_btn.click()
        print("Save To Gallery Button")
    except TimeoutException:
        print("Image is not action to Save")

    '''Click Home button'''
    try:
        home_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.braincraftapps.droid.bgremover:id/home_button'))
        )
        home_btn.click()
        print("Successfully Click Home button")
    except TimeoutException:
        print("Button is not found")

    '''App Close'''
    print("Closing button to close the App...")
    try:
        close_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.braincraftapps.droid.bgremover:id/close_button'))
        )
        close_btn.click()
        print("First tap done")
        time.sleep(1)
        close_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.braincraftapps.droid.bgremover:id/close_button'))
        )
        close_btn.click()
        print("App closed successfully")
    except Exception as e:
        print(f"Error closing the app: {e}")

    print(driver.contexts)

except WebDriverException as e:
    print(f"WebDriver Error: {str(e)}")
    if "Connection refused" in str(e):
        print("Make sure Appium server is running on http://localhost:4723")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
    print(f"Exception type: {type(e).__name__}")
    import traceback
    print("Traceback:")
    traceback.print_exc()


finally:
    try:
        if 'driver' in locals():
            driver.quit()
    except:
        pass
