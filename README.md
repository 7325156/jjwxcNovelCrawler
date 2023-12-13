**用[这个app](https://legado.cn/thread-9082-1-1.html)搭配这个[书源](https://legado.cn/forum.php?mod=viewthread&tid=7411)吧，我这儿暂时解决不了**

![jjwxc](https://user-images.githubusercontent.com/57527406/157160102-811010d2-dca2-422c-853b-99d46bbd02a9.png)

<br/>
github下载：

[![GitHub release](https://img.shields.io/github/release/7325156/jjwxcNovelCrawler.svg)](https://github.com/7325156/jjwxcNovelCrawler/releases/latest/)
<br/>
蓝奏云下载：https://wwr.lanzoui.com/b02oduqmd#a5jo 密码:a5jo <br/>
**采用自解压文件，将exe放到指定位置，双击打开后点击“解压”就行**
<p>此项目仅供学习交流使用，严禁用于商业用途，请在24小时之内删除。</p>
<p>目前找到无需反爬虫的源，所以反爬虫功能暂时退出历史舞台（做人不能太铁齿），反爬虫表依然保留在项目里，感谢各位大佬做出的贡献。</p>
<p>最新版使用app接口下载，无需反爬虫。感谢<b>酷安 @关耳010225 @乃星 @viviyaaa</b>的方案。</p>
<p>也可以直接去微信公众号“开源阅读”下载app，然后按教程添加女频书源</p>
<p>若文章无法下载，可以在issues里把网址和配置的config.yml里除了cookie以外的信息发给我。</p>
<p>常见问题见wiki</p>
<h1>使用说明</h1>
<p>如果不想配置环境，可以直接下载EXE：<a href="https://github.com/7325156/jjdown/releases">exe程序下载</a>，如果直接下载太慢，可以通过<a href="https://d.serctl.com">这个网站</a>下载</p>
<p>如果打开exe后报错，注意下载与版本匹配的config.yml文件，与exe放在同一目录下，还报错的话，在exe里填好配置，点击“保存配置”按钮，还不行就将config.yml里除了cookie以外的信息发给我，我想办法修bug。</p>
<p><strong><center>以下是使用py文件下载的过程</center></strong></p>
<h3>环境配置</h3>
<p>注：我写的这个程序可以在Windows10 x64系统下运行成功，其他环境可自行调整。</p>
<p><span style="font-weight: bold;">&#160;1、安装python环境</span></p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>建议安装python3.8x的环境。安装教程：<a href="https://blog.csdn.net/weixin_40844416/article/details/80889165">https://blog.csdn.net/weixin_40844416/article/details/80889165</a></p>
<p><span style="font-weight: bold;">&#160;2、安装第三方库</span></p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>联网，使用<b>管理员模式</b>打开命令提示符（cmd），依次输入以下命令、按回车键运行</p>
<p>(如果下载慢，可以用pip install --index https://pypi.mirrors.ustc.edu.cn/simple/ 代替pip install</p>
<ul><li>pip install lxml</li>
 <li>pip install opencc_python_reimplemented</li>
 <li>pip install requests</li>
 <li>pip install PyQt5</li>
 <li>pip install PyQt5-tools</li>
 <li>pip install PyYAML</li>
<li>pip install selenium(用于Chrome浏览器)</li>
</ul>
<p>(也可下载requirements.txt文件，使用cmd进入该文件所在目录，输入 pip install -r requirements.txt)</p>
<p>3、（可跳过）安装chormedriver</p>
<p>若要使用client.py获取cookie，必须执行步骤3</p>
<p>该程序使用Chrome87，请在以下网址安装对应的chormedriver：https://chromedriver.chromium.org/downloads</p>
<p>以管理员身份打开cmd，输入where python，找到python路径，将chormedriver放到python.exe所在路径下</p>
<h3>程序使用</h3>
<p>1、若下载非VIP章节，直接双击运行。</p>
<p>2、运行文件后输入小说主页网址。（例如：“http://www.jjwxc.net/onebook.php?novelid=2710871” ）</p>
<p>3、若下载VIP章节，登陆晋江（建议使用谷歌浏览器），右键点击“检查”，或按F12进入开发者模式，点击console（控制台）按钮，输入document.cookie &#160; ，按回车，输入到对应的框里，并保存配置。</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>或者直接下载并打开client.py，按步骤输入用户名密码，将得到的值输入到对应的框里。</p>
<p>　　(注：cookie若失效，请重新登录晋江并及时更换，还不行就更换浏览器。)</p>
<h1>main_epub日志记录</h1>

<p>2022-11-29</p>

<ul><li>将封面图片的格式转换为jpg</li></ul>
<p>2022-03-27</p>
<ul><li>修复部分已购买的章节无法下载问题</li></ul>
<p>2022-03-08</p>

<ul>
 <li>新增去除一键感谢功能</li>
</ul>

<p>2022-01-01</p>
<ul>
 <li>修改网址不能匹配https的bug。</li>
</ul>
<p>2021-11-09</p>
<ul>
 <li>添加自定义标题、卷标格式功能。</li>
</ul>
<p>2021-10-26</p>
<ul>
 <li>为epub2添加网页目录</li>
 <li>获取未购买、被锁章节信息</li>
</ul>
<p>2021-10-22</p>
<ul>
 <li>使用app接口下载，无需反爬虫。</li>
 <li>添加编辑css功能。</li>
</ul>
<p>2021-9-30</p>
<ul>
 <li>新增窗口模式，可自由选择反爬虫模式（侵删）、文件下载格式以及其他必备配置。</li>
</ul>
<p>2021-8-23</p>
<ul>
 <li>感谢@fffonion大佬的反爬虫方案，可根据json文件自动解析并生成反爬虫表，该过程会比较慢。</li>
</ul>
<p>2021-6-21</p>
<ul>
 <li>推出全新版本，将数据存放在config.py中，方便使用和定制下载模式（包括cookie，繁简转换标志，章节标题模式，线程池最大容量）</li>
</ul>
<p>2021-1-23</p>
<ul>
 <li>新增乱码替换功能，对照表已全部完成，感谢<a href="https://github.com/starcrys">starcrys</a>，持续众筹新字体，详见issues</li></ul>
<p>2021-1-21</p>
<ul>
 <li>新增乱码替换功能（需要对照表，对照表仅完成部分，详见issues）</li>
<li>修正无法创建Fonts文件夹的bug。</li>
</ul>
<p>2021-1-19</p>
<ul>
<li>优化反爬虫处理方案，增添“只需联网、无需下载字体文件”的选择。</li>
</ul>
<p>2021-1-18</p>
<ul>
<li>对反爬虫进行处理</li>
</ul>
<p>2020-11-20</p>
<ul>
<li>修改程序无法处理目录、卷标特效的bug</li>
 <li>修改程序无法获取部分网站图源的bug（需科学上网）</li>
</ul>
<p>2020-9-21</p>
<ul>
<li>调整下载文件和EPUB生成文件，使其匹配</li>
 <li>修改EPUB2生成格式，可自由选择生成的epub文件格式</li>
 <li>新增文案特效版下载，可以显示文案特效</li>
</ul>
<p>2020-3-23</p>
<ul>
<li>使用多线程下载章节（python的多线程好像不怎么给力）</li>
 <li>优化封面保存功能</li>
 <li>文件保存格式从epub2改为epub3</li>
 <li>优化目录保存方式</li>
 <li>替换不安全符号</li>
</ul>
<p>2020-2-14</p>
<ul>
 <li>修复文案审核期间无法下载的bug</li>
 <li>将epub打包功能单独拆分到EPUB.py文件中</li>
</ul>
<p>2020-01-05</p>
<ul>
 <li>优化繁简转换方式</li>
 <li>优化内容简介和标题不匹配的bug</li>

</ul>
<p>2019-12-20</p>
<ul>
 <li>在epub打包前暂停程序，便于修改。</li>
 <li>优化繁简转换方式</li>
 <li>关于OpenCC的使用方法，详见https://github.com/yichen0831/opencc-python</li>
</ul>
<p>2019-12-19</p>
<ul>
 <li>优化封面后存在乱码的bug</li>
 <li>优化内容简介和标题不匹配的bug</li>
<li>新增繁转简转换功能（若不需要此功能，将含有OpenCC('t2s').convert的所有行删除）</li>
</ul>
<p>初始功能：</p>
<ul><li>添加封面（若不需要，将包含"C.xhtml"和"p.jpg"的所有行删除）</li>
<li>添加两级目录（若不需要添加目录，删除"create_tox"函数）</li>
<li>通过cookie下载已购买VIP章节</li>
</ul>
