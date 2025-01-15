import requests
from bs4 import BeautifulSoup
import re
from collections import namedtuple

#example url = "https://w5.hkust-gz.edu.cn/wcq/cgi-bin/2410/subject/AIAA"
#AIAA AMAT BSBE CMAA DSAA EOAS FTEC FUNH INFH INTR IOTA IPEN LANG MICS PDEV PLED ROAS SEEN SMMG SOCH SYSH UCMP UCUG UFUG UGOD
list = ["AIAA","AMAT", "BSBE", "CMAA", "DSAA", "EOAS", "FTEC", "FUNH", "INFH", "INTR", "IOTA", "IPEN", "LANG", "MICS", "PDEV", "PLED", "ROAS", "SEEN", "SMMG", "SOCH", "SYSH", "UCMP", "UCUG", "UFUG", "UGOD"]
# for each of the list we get into its url
for subject in list:
    url = f"https://w5.hkust-gz.edu.cn/wcq/cgi-bin/2410/subject/{subject}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Process the soup object as needed
        print(f"Successfully fetched data for {subject}")
        # save respectively like AIAA.html
        with open(f"{subject}.html", "w", encoding="utf-8") as file:
            file.write(str(soup))

    else:
        print(f"Failed to fetch data for {subject}")


