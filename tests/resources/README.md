# Sources

The articles inside this folder were downloaded using the following simple script below.
The files were downloaded on the 4th of January 2021, and the original articles may have
been updated or even deleted since then.

```python
import requests

articles = {
    "article1.html": "https://www.gov.il/he/departments/news/03012021-03",
    "article2.html": "https://www.gov.il/he/departments/news/health-and-environment-news",
    "article3.html": "https://www.gov.il/he/departments/news/my_wave",
    "article4.html": "https://www.gov.il/he/departments/news/agra_2021",
}


for filename, url in articles.items():
    content = requests.get(url).content
    with open(filename, 'wb') as f:
        f.write(content)
```
