import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


def test_iframe_text(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/iframes.html")
    wait = WebDriverWait(driver, 20)
    # проверка наличия текста в iframe
    field = wait.until(EC.presence_of_element_located((By.ID, "my-iframe")))
    driver.switch_to.frame(field)

    # поиск подтекста в тексте
    elements = driver.find_elements(By.CLASS_NAME, "lead")
    my_text = "semper posuere integer et senectus justo curabitur."

    assert f"Text '{my_text}' found in iframe"


def test_drup_drop(driver):
    driver.get("https://www.globalsqa.com/demo-site/draganddrop/")
    wait = WebDriverWait(driver, 25)

    # Закрываем первое окно при открытии
    try:
        button1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button")))
       # driver.execute_script("arguments[0].scrollIntiView(true);", button1)
        button1.click()
    except:
        pass

    # Переключаемся во фрейм
    frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".resp-tab-content-active > p > iframe")))
    driver.switch_to.frame(frame)

    # Находим элементы
    image = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gallery > li:nth-child(1) > img")))
    trash = wait.until(EC.presence_of_element_located((By.ID, "trash")))

    # Перетаскиваем первую фотографию в корзину
    action = ActionChains(driver)
    action.drag_and_drop(image, trash).perform()


    trash_photos = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#trash > ul > li"))
    )
    gallery_photos = driver.find_elements(By.CSS_SELECTOR, "#gallery li")

    print(f"\nВ корзине фото: {len(trash_photos)}")
    print(f"В галерее фото: {len(gallery_photos)}")

    # Проверяем количество фото
    assert len(trash_photos) == 1, "Фото не появилось в корзине"
    assert len(gallery_photos) == 3, "Неверное количество фото в галерее"

    driver.switch_to.default_content()


