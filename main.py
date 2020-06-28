from selenium import webdriver  # Importing selenium webdriver (automates web-driven process)
from selenium.webdriver.support.ui import WebDriverWait # Explicit/ Implicit waiting for elements to appear on the webpage
from selenium.webdriver.support import expected_conditions as EC # WebDriverWait by default calls the ExpectedCondition every 500 milliseconds until it returns successfully. Boolean
from selenium.webdriver.common.by import By # Various attributes used to locate element i.e. "CLASS_NAME", "CCS_SELECTOR", "ID", "LINK_TEXT", etc.
import time # Importing time
import insta_credentials # Importing username, password and instagram_name variables from insta_credentials.py

username = insta_credentials.username # Calling insta_credentials.py and retrieving "username" variable
password = insta_credentials.password # Calling insta_credentials.py and retrieving "password " variable
instagram_name = insta_credentials.instagram_name # Calling insta_credentials.py and retrieving "instagram_name" variable

# Function that allows us to access instagram via selenium (chrome web driver) and log in
def accessing_instagram_and_logging_in(self):
    options = webdriver.ChromeOptions() # Assigning options for chrome into a variable
    options.add_argument("--start-maximized") # Start chrome maximised

    self.driver = webdriver.Chrome('C:/WebDrivers/chromedriver.exe',chrome_options=options)  # Opening chrome via chrome driver in 'maximised' mode (full screen)
    self.driver.get("https://instagram.com/")  # Accessing this link via Google Chrome (instance created)

    # Wait for element to load + Click "Log in with Facebook" button
    self._make_driver_wait('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[6]/button/span[2]')
    self.driver.find_element_by_xpath(
        '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[6]/button/span[2]').click()

    # Wait for element to load + Add username, password + Click "submit" button
    self._make_driver_wait("//input[@name=\"email\"]")
    self.driver.find_element_by_xpath("//input[@name=\"email\"]").send_keys(username)
    self.driver.find_element_by_xpath("//input[@name=\"pass\"]").send_keys(password)
    self.driver.find_element_by_xpath('//button[@type="submit"]').click()

    # Wait for element to load + Click "Now Now" button
    self._make_driver_wait("//button[contains(text(), 'Not Now')]")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

# Function that compares list of followers to following and stores "not following back" in a list
def comparing_followers_to_following(self):
    # Wait for element to load + Click instagram name button i.e. profile
    self._make_driver_wait("//a[contains(@href,'/{}')]".format(self.instagram_name))
    self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.instagram_name)).click()

    # Wait for element to load + Click "following"
    self._make_driver_wait("//a[contains(@href,'/following')]")
    self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
    following = self._get_names() # "following" people stored into a list via "._get_names()" function

    # Wait for element to load + Click "followers"
    self._make_driver_wait("//a[contains(@href,'/followers')]")
    self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
    followers = self._get_names() # "followers" people stored into a list via "._get_names()" function

    # Compare both lists and add people who "not following back" into another python list
    not_following_back = [user for user in following if user not in followers]

    return not_following_back # Return list of unfollowers

# Function that adds people "not following you back" to a text file
def add_unfollowers_to_txt_file(not_following_back):
    unfollowers_file = open('C:/Users/jorda/Desktop/Code/insta_bot/Insta_Unfollowers.txt', 'w') # Create and open txt file, 'w' = we writing to file
    unfollowers_file.write("************* INSTAGRAM UNFOLLOWERS *************" + "\n\n")

    # Iterating through all "unfollowers" and writing to text file
    for i, unfollower in enumerate(not_following_back):
        unfollowers_file.write("%s%s %s %s" % (i, ".", unfollower, "\n"))
    unfollowers_file.close()

# Creating class
class Instabot():

    # Reseved method in python classes. It is known as a constructor in object oriented concepts.
    # This method called when an object is created from the class and it allow the class to initialize the attributes of a class
    def __init__(self, username, password):
        self.username = username # Setting username
        self.password = password # Setting password
        self.instagram_name = instagram_name # Setting instagram name

        accessing_instagram_and_logging_in(self) # Calling method to access instagram and log in

        not_following_back = comparing_followers_to_following(self) # Calling method to get "unfollowers" and assigning them to variable "not_following_back"

        add_unfollowers_to_txt_file(not_following_back) # Calling method to write "unfollowers" to text file

        time.sleep(2) # Sleep/Wait for 2 seconds

    # Explicitly waiting for an element to be loaded before the user attempts to interact with that element
    def _make_driver_wait(self, element_to_locate, by='xpath'):
        wait = WebDriverWait(self.driver, 20) # Constructor, takes a WebDriver instance and timeout in seconds
        if by == 'xpath':
            wait.until(EC.element_to_be_clickable((By.XPATH, element_to_locate)))
        elif by == 'class_name':
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, element_to_locate)))
        elif by == 'tag_name':
            wait.until(EC.element_to_be_clickable((By.TAG_NAME, element_to_locate)))

    # Function that iterates through the "following" and "followers" list and returns names in both lists
    def _get_names(self):
        time.sleep(2) # Sleep/Wait for 2 secs

        # Wait for element to load + Click "Scroll Bar/Bar"
        self._make_driver_wait("/html/body/div[4]/div/div/div[2]")
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

        last_ht = 0 # Variable that determines the last height of the scroll box
        ht = 1 # Variable that determines the current height of the scroll box

        # Loop that compares the last height to the current height to ensure that we are still scrolling through "following" and "followers" all the way to the end
        while last_ht != ht:
            last_ht = ht
            time.sleep(1)
            ht = self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box) # Computing the current height of the scroll box

        links = scroll_box.find_elements_by_tag_name('a') # Identifying names of all "following" and "following" using 'a' (anchor tag)
        names = [name.text for name in links if name.text != ''] # Adding the names (name.text) from anchor tags into this list

        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click() # Click 'X' button to exit the following/followers list

        return names # Returning all the names

# Main method
def main():

    Instabot(username, password) # Creating an instance of Instabot class

main()
