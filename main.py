import os
import 模块库
urls=['https://pixai.art/zh/artwork/2012407913748708334']
base_path=r"S:\python项目\爬虫多线程\image"
pixai_path=base_path+r'\pixai'#
if not os.path.exists(pixai_path):
      os.mkdir(pixai_path)
responses=模块库.get_html(urls)
模块库.submit_and_as_completed(responses,urls)