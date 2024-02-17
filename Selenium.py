from selenium.webdriver.common.by import By


from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FireFoxService
from webdriver_manager.firefox import GeckoDriverManager


class Selenium:

    driver = ""
    home_window = ""
    def __init__(self, **kwargs):
        browser = kwargs.get('browser')
        if browser == "chrome":
            pass
        elif browser == "firefox":
            options = Options()
            options.add_argument("-headless")
            self.driver = Firefox(service=FireFoxService(GeckoDriverManager().install()), options=options)
        
    
    def get(self, url):
        self.driver.get(url)
    
    def find_element_by_id(self, id, parent=None):
        if parent:
            return parent.find_element(By.ID, id)
        return self.driver.find_element(By.ID, id)

    def find_element_by_css_selector(self, selector, parent=None):
        if parent:
            return parent.find_element(By.CSS_SELECTOR, selector)
        return self.driver.find_element(By.CSS_SELECTOR, selector)
    
    def find_element_by_name(self, name, parent=None):
        if parent:
            return parent.find_element(By.NAME, name)
        return self.driver.find_element(By.NAME, name)
    
    def find_element_by_link_text(self, link_text, parent=None):
        if parent:
            return parent.find_element(By.LINK_TEXT, link_text)
        return self.driver.find_element(By.LINK_TEXT, link_text)
    
    def find_elements_by_tag_name(self, tag_name, parent=None):
        if parent:
            return parent.find_elements(By.TAG_NAME, tag_name)
        return self.driver.find_elements(By.TAG_NAME, tag_name)
    
    def find_elements_by_class_name(self, class_name, parent=None):
        if parent:
            return parent.find_elements(By.CLASS_NAME, class_name)
        return self.driver.find_elements(By.CLASS_NAME, class_name)
    
    def find_elements_by_xpath(self, xpath, parent=None):
        if parent:
            return parent.find_elements(By.XPATH, xpath)
        return self.driver.find_elements(By.XPATH, xpath)
    
    def open_new_tab(self, tab_name, url=None):
        """
        The open_new_tab function opens a new tab in the browser.
            The function takes two arguments:
                1) tab_name - A string that is used to identify the new tab.  This can be any string, but it should be unique for each open tab.  If you don't specify a name, then one will be generated for you (but this may not work as expected).
                2) url - An optional argument that specifies what URL to load into the newly opened window/tab.  If no URL is specified, then an empty page will be loaded.
        
        :param self: Reference the current instance of the class
        :param tab_name: Name the tab
        :param url: Open a new tab with the url specified
        :return: The driver
        :doc-author: Sabari
        """
        driver = self.driver
        self.home_window = driver.current_window_handle
        driver.execute_script(f"window.open('about:blank', '{tab_name}');")
        if url:
            driver.switch_to.window(f"{tab_name}")
            driver.get(url)
        self.switch_tab(self.home_window)
    
    def switch_home(self):
        """
        The switch_home function switches the current tab to the home window.
                
        
        :param self: Access the attributes and methods of a class
        :return: A tab
        :doc-author: Sabari
        """
        self.switch_tab(self.home_window)

    def switch_tab(self, tab_name):
        """
        The switch_tab function switches to the tab with the name passed in as an argument.
            Args:
                tab_name (str): The name of the tab you want to switch to. 
        
        
        :param self: Represent the instance of the class
        :param tab_name: Switch to a new tab
        :return: The name of the tab that is currently open
        :doc-author: Sabari
        """
        self.driver.switch_to.window(f"{tab_name}")

    def close(self):
        """
        The close function closes the browser window that is currently open.
            
        
        :param self: Represent the instance of the class
        :return: Nothing
        :doc-author: Sabari
        """
        self.driver.close()
