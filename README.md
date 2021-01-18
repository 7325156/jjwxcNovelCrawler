<p>众筹晋江反爬虫字体文件和对照表，详见issues</p>
<p>若文章无法下载，可以在issues里把网址发给我。若某一章显示乱码，先看看fonts文件夹里有没有多出来一个不在字体列表中的文件，将文件名发给我。</p>
<h1>使用说明</h1>
<p>如果不想配置环境，可以直接下载EXE：<a href="https://github.com/7325156/jjdown/releases">exe程序下载</a>，如果直接下载太慢，可以通过<a href="https://d.serctl.com">这个网站</a>下载</p>
<h3>环境配置</h3>
<p>注：我写的这个程序可以在Windows10 x64系统下运行成功，其他环境可自行调整。</p>
<p><span style="font-weight: bold;">&#160;1、安装python环境</span></p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>建议安装python3.7的环境。安装教程：<a href="https://blog.csdn.net/weixin_40844416/article/details/80889165">https://blog.csdn.net/weixin_40844416/article/details/80889165</a></p>
<p><span style="font-weight: bold;">&#160;2、安装第三方库</span></p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>联网，使用<b>管理员模式</b>打开命令提示符（cmd），依次输入以下命令、按回车键运行</p>
<p></p>
<ul><li>pip install&#160;requests</li>
<li>pip install lxml</li>
<li>pip install&#160;selenium</li>
 <li>pip install opencc-python-reimplemented</li>
</ul>
&#160;3、（可跳过）安装chormedriver<p></p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>若要使用client.py获取cookie，必须执行步骤3</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>点击support文件夹，下载两个exe文件到本地。如果版本不是78.0.3904.108，双击chormesetup安装浏览器。</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>以管理员身份打开cmd，输入where python，找到python路径，将chormedriver放到python.exe所在路径下</p>
<h3>程序使用</h3>
<p>1、若下载非VIP章节，直接下载main_txt.py或“epub下载”文件夹中全部文件，双击运行。<b>主要更新epub格式下载的程序，因为我发现epub文件大小居然比txt小，读起来也方便。</b></p>
<p>　　(注：main_txt.py可将小说保存为txt格式，main_epub.py可将小说保存为epub格式，EPUB.py存放epub打包方法)</p>
<p>2、运行文件后输入小说主页网址。（例如：“http://www.jjwxc.net/onebook.php?novelid=2710871” ）</p>
<p>3、若下载VIP章节，登陆晋江（建议使用edge浏览器或IE浏览器），右键点击“检查”，或按F12进入开发者模式，点击console（控制台）按钮，输入document.cookie &#160; ，按回车，按照代码注释复制到main_txt.py|main_epub.py文件header中的指定位置</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>或者直接下载并打开client.py，按步骤输入用户名密码，将得到的值（包括大括号）赋给main_txt.py|main_epub.py的headerss</p>
<p>　　(注：cookie若失效，请及时更换，如果换了还不行，就使用ie浏览器获取cookie，如果还不行，删除"timeOffset_o=任意字符串;")</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>保存main_txt.py|main_epub.py，运行文件</p>
<p><b>繁简转换功能</b>：输入编号后，若不转换，直接按回车，若繁转简，输入s后按回车，若简转繁，输入t后按回车。</p>
<p><b>若epub文件有问题，可以用epub编辑工具修复一下，本人建议使用sigil或calibre，这两个软件在GitHub上都有。</b></p>
<h1>main_epub日志记录</h1>
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
