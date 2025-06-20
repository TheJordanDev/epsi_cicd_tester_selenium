import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Tester():
  def setup_method(self, _):
    self.driver = webdriver.Firefox()
    self.actions = webdriver.ActionChains(self.driver)
    self.todo_input = None
    self.add_button = None
    self.vars = {}
  
  def teardown_method(self, _):
    self.driver.quit()

  def click_button(self, button):
    self.actions.move_to_element(button).click().perform()
    time.sleep(0.2)

  def add_todo(self, todo_text):
    self.todo_input.clear()
    self.actions.move_to_element(self.todo_input).click().send_keys(todo_text).perform()
    time.sleep(0.2)
    self.click_button(self.add_button)
    time.sleep(0.2)

  def test(self):  
    wait = WebDriverWait(self.driver, 10)

    self.driver.get("http://192.168.0.44:4561/")
    self.driver.set_window_size(1323, 812)

    wait = WebDriverWait(self.driver, 10)

    self.todo_input = wait.until(EC.presence_of_element_located((By.ID, "todo-input")))
    self.add_button = wait.until(EC.element_to_be_clickable((By.ID, "add-todo")))

    import time

    for i in range(3):
      self.add_todo(f"Test {i + 1}")
    
    self.add_todo("Test 5")

    self.add_todo("Test 4")

    delete_button = self.driver.find_element(By.XPATH, "//li[span[text()='Test 5']]/button")
    self.click_button(delete_button)

    self.add_todo("Test 5")

    self.driver.find_element(By.ID, "add-todo").click()
    todos = self.driver.find_elements(By.CSS_SELECTOR, ".todo-item")

    self.teardown_method(None)

    assert len(todos) == 5, f"Expected 5 todos, found {len(todos)}"
  

tester = Tester()
tester.setup_method(None)
tester.test()