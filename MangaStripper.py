from Selenium import Selenium
from Utilities import create_new_folder, join_path, file_exists, read_json
from Utilities import write_json, download_file, non_char_to_underscore


class MangaStripper:
    def get_manga_info_from_folder(self):
        """
        The get_manga_info_from_folder function returns a dictionary object with details of manga chapters.

        :param self: Access the class variables and methods
        :return: A dictionary object with details of manga chapters
        :doc-author: Sabari
        """
        
        if file_exists(self.chapters_json):
            return read_json(self.chapters_json)
        return {}

    def require_extraction(self):
        """
        The require_extraction function is used to determine whether a chapter extraction is required.
        
        :param self: Refer to the object itself
        :return: A boolean value
        :doc-author: Sabari
        """
        self.get_manga_info_from_page()
        folder_chapters_info = self.get_manga_info_from_folder()
        new_chapters = True

        # If manga folder has chapter information, then compare with web info
        # and the store uncapture info as new chapter
        # If no chapter information in Manga Folder, then store web info as new chapters
        if folder_chapters_info:
            for chapter_name in self.chapters_info:
                if chapter_name in folder_chapters_info:
                    self.chapters_info[chapter_name] = folder_chapters_info[chapter_name]
                else:
                    new_chapters = False

        # Return if there are new chapters
        return new_chapters

class ChapMangaNelo(MangaStripper):

    base_url = "https://chapmanganelo.com/"

    def __init__(self, **kwargs):
        if "browser" in kwargs:
            self.selenium = Selenium(browser=kwargs["browser"])

    def download_image(self, image, file_path):
        with open(file_path, "wb") as f:
            f.write(image.screenshot_as_png)

    def get_manga_info_from_page(self):
        """
        The get_manga_info_from_page function returns manga info extracted from MangaNelo web page
        and stores the details in chapter_info attribute.
        
        
        :param self: Access the attributes and methods of the class in python
        :return: A dictionary of dictionaries
        :doc-author: Sabari
        """
        selenium = self.selenium
        chapter_list = selenium.find_element_by_id("row-content-chapter")
        chapter_list = selenium.find_elements_by_tag_name("li", chapter_list)

        chapters_info = {}
        # Loop through chapter list and get manga info
        for chapter_row in chapter_list:
            chapter_anchor = selenium.find_elements_by_tag_name("a", chapter_row)[0]
            link = chapter_anchor.get_dom_attribute("href")
            chapter_name = chapter_anchor.text
            chapters_info[chapter_name] = {
                "name": chapter_name,
                "href": link,
                "completed": False
            }
        
        self.chapters_info = chapters_info

    def extract_chapter_images(self, chapter_name, chapter_images):
        
        """
        The extract_chapter_images function takes in a chapter name and the images associated with that chapter.
        It then creates a new folder for that chapter, downloads all of the images to it, and writes them to an image.json file.
        
        :param self: Refer to the current object
        :param chapter_name: Create a new folder for the chapter
        :param chapter_images: Store the images in a list
        :return: A list of the image names in a chapter
        :doc-author: Sabari
        """
        chapter_folder = create_new_folder(join_path(self.folder_name, chapter_name))
        images = []
        for img in chapter_images:
            image_href = (img.get_dom_attribute("src"))
            image_name = image_href.split("/")[-1:][0]
            images.append(image_name)
            image_path = join_path(chapter_folder, image_name + ".png")
            self.download_image(img, image_path)
        write_json(join_path(chapter_folder, "images.json"), images)
        self.chapters_info[chapter_name]["completed"] = True

    def extract_chapter_to_folder(self, chapter):
        """
        The extract_chapter_to_folder function extracts the images from a chapter's Web page and saves them to a folder.
            Args:
                chapter (dict): A dictionary containing the name of the chapter and its href.
            Returns: None
        
        :param self: Refer to the object itself
        :param chapter: Extract the name and href of the chapter
        :return: None
        :doc-author: Sabari
        """
        selenium = self.selenium
        name = chapter["name"]
        href = chapter["href"]
        tab_name = non_char_to_underscore(name)
        
        # Extract images from Web page
        selenium.open_new_tab(tab_name=f"{tab_name}", url=f"{href}")
        selenium.switch_tab(tab_name)

        chapter_container = selenium.find_elements_by_class_name("container-chapter-reader")[0]
        chapter_images = selenium.find_elements_by_tag_name("img", chapter_container)
        self.extract_chapter_images(name, chapter_images)
        selenium.close()
        selenium.switch_home()


    def extract_new_chapters(self):
        
        """
        The extract_new_chapters function extracts all chapters that have not been extracted yet.
            It does this by checking the completed field in the chapter_info dictionary for each chapter.
            If it is False, then it calls extract_chapter_to_folder to extract that chapter.
        
        :param self: Access the attributes and methods of the class
        :return: The updated chapters_info dictionary
        :doc-author: Sabari
        """
        if self.require_extraction():
            for chapter_name in self.chapters_info:
                chapter_info = self.chapters_info[chapter_name]
                if not chapter_info["completed"]:
                    self.extract_chapter_to_folder(chapter_info)
                write_json(self.chapters_json, self.chapters_info)

    def extract_manga(self, manga_id):
        
        """
        The extract_manga function is the main function of this class. It takes a manga_id as an argument, and extracts all chapters from that manga into a folder with the name of the manga.
        
        :param self: Refer to the current instance of the class
        :param manga_id: Create the manga_url variable
        :return: The name of the folder where the manga will be downloaded
        :doc-author: Sabari
        """
        if "http" not in manga_id:
            manga_url = self.base_url + manga_id
        selenium = self.selenium

        # Go to the manga page
        selenium.get(manga_url)

        # Extract the manga title
        info = selenium.find_elements_by_class_name("story-info-right")[0]
        heading = selenium.find_elements_by_tag_name("h1", info)[0].text
        print(f"Striping Manga Title: {heading}")
        self.folder_name = create_new_folder(
            join_path("Mangas", non_char_to_underscore(heading))
        )
        self.chapters_json = join_path(self.folder_name, "chapters.json")
        self.extract_new_chapters()
    
    def close(self):
        self.selenium.close()