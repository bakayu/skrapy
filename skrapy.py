import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

def scrapeWeb(url):
    print(f'launching scrapper on {url}')
    
    chrome_driver_path = "chromedriver"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(url)
        print(f'page loaded')
        
        # Inject JavaScript to make all hidden elements visible
        driver.execute_script("""
            var elements = document.querySelectorAll('[style*="display: none"], [style*="visibility: hidden"], [hidden]');
            for (var i = 0; i < elements.length; i++) {
                elements[i].style.display = 'block';
                elements[i].style.visibility = 'visible';
                elements[i].hidden = false;
            }
        """)
        
        # Wait for the JavaScript to execute
        time.sleep(2)
        
        html = driver.page_source
         
        return html
    
    except Exception as e:
        print(f'Error: {e}')
    
    finally:
        driver.quit()

def extractData(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    if body:
        return str(body)
    else:
        return ""
    
def cleanBody(body):
    soup = BeautifulSoup(body, 'html.parser')

    for i in soup(['script', 'style']):
        i.extract()
        
    content = soup.get_text(separator='\n')
    content = "\n".join(line.strip() for line in content.splitlines() if line.strip())
    
    return content

def splitDomContent(dom_content, max_chars=6000):
    return [ dom_content[i:i+max_chars] for i in range(0, len(dom_content), max_chars) ]