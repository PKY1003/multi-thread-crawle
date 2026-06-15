# multi-thread-crawle
A simple multi-threaded crawler for downloading high-definition wallpapers
这是我的第二个爬虫项目，相较于我的第一个项目，他已经不再那么的简陋，具有了多线程爬取和一定的反反爬能力。但是问题依旧明显，遇到反爬能力高的网站就显得力不从心。依次依然只推荐把该项目作为一个爬虫的素材来使用。
2026-6-15 简单的多线程爬虫
技术栈：urllib+requests+beautifulsoup4
挑战：1、多线程概念比单线程复杂很多，从单线程转到多线程时缺乏经验，明显手足无措
2、误以为线程数=下载图片数，一开始把开发方向搞成了"多线程爬多个页面"，而不是"多线程下载同一页面的多张图片"
3、下载了所有img标签的图片，包括垃圾文件和无关图片，无法精确筛选想要的内容
4、反爬升级：wallpaperswide从可爬变成403，urllib裸请求被直接拒绝
