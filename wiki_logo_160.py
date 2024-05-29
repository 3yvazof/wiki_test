import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

@pytest.fixture(params=["chrome", "firefox", "edge"])
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif request.param == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif request.param == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.implicitly_wait(10)  # Set implicit wait
    yield driver
    driver.quit()

def test_nasa_wikipedia_page(driver):
    driver.get("https://en.wikipedia.org/wiki/NASA")

    # Explicit wait for the Wikipedia logo
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Wikipedia']")))

    # Check Wikipedia logo dimensions
    logo = driver.find_element(By.XPATH, "//img[@alt='Wikipedia']")
    assert logo.size['width'] == 160 and logo.size['height'] == 160

    # Check body background color
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.value_of_css_property("background-color") == "rgba(0, 0, 0, 1)"

    # Explicit wait for the NASA budget table
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "NASA_budget_table")))

    # Check box-sizing property of NASA budget table
    table = driver.find_element(By.ID, "NASA_budget_table")
    assert table.value_of_css_property("box-sizing") == "border-box"

    # Explicit wait for links
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul li a")))

    # Check font settings for links list
    links = driver.find_elements(By.CSS_SELECTOR, "ul li a")
    for link in links:
        assert "Sans Serif" in link.value_of_css_property("font-family")
        assert 12.6 == float(link.value_of_css_property("font-size").strip("px"))

# Run the tests directly without the if __name__ == "__main__": block
pytest.main([__file__])