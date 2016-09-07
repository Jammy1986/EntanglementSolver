from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class SeleniumManager:
    def __enter__(self):
        self.driver = Chrome(executable_path="../Common/chromedriver.exe")
        self.driver.get("http://entanglement.gopherwoodstudios.com/")

        WebDriverWait(self.driver, 20).until(EC.invisibility_of_element_located((By.ID, "main-menu-background")))

        # Love the audio, but not as much as whatever is coming out of Spotify while I'm coding.
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "sfx-on")))
        self.driver.find_element(By.ID, "sfx-button").click()
        WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.ID, "music-on")))
        self.driver.find_element(By.ID, "music-button").click()
        return self

    def get_tiles(self):
        tiles = self.driver.execute_script("return gws.currentGame.tiles")
        start_tile = self.driver.execute_script("return gws.currentGame.players[0][3][1]")
        swap_tile = self.driver.execute_script("return gws.currentGame.players[0][3][0]")
        return tiles, start_tile, swap_tile

    def swap_tile(self):
        action_chains = ActionChains(self.driver)
        action_chains.context_click(self.driver.find_element_by_class_name("map")).perform()

    def rotate(self, rotation):
        action_chains = ActionChains(self.driver)
        for i in range(0, rotation):
            action_chains.send_keys(Keys.ARROW_RIGHT)
        action_chains.perform()

    def place(self):
        action_chains = ActionChains(self.driver)
        action_chains.click(self.driver.find_element_by_class_name("map")).perform()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
