from fake_useragent import UserAgent
from msedge.selenium_tools import Edge, EdgeOptions

options = EdgeOptions()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
driver = Edge(options=options, executable_path=r'd:\Python3.7\msedgedriver.exe')
driver.get("https://www.google.co.in")
driver.quit()
