<h1>使用说明</h1>
<h3>环境配置</h3>
<p>注：我写的这个程序可以在Windows10 x64系统下运行成功，其他环境可自行调整。</p>
<p><span style="font-weight: bold;">&#160;1、安装python环境</span></p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>建议安装python3.7的环境。安装教程：<a href="https://blog.csdn.net/weixin_40844416/article/details/80889165">https://blog.csdn.net/weixin_40844416/article/details/80889165</a></p>
<p><span style="font-weight: bold;">&#160;2、安装第三方库</span></p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>联网，使用管理员模式打开命令提示符（cmd），依次输入以下命令、按回车键运行</p>
<p></p>
<ul><li>pip install&#160;requests</li>
<li>pip install lxml</li>
 <li>pip install hanziconv</li>
<li>pip install&#160;selenium</li>
</ul>
&#160;3、（可跳过）安装chormedriver<p></p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>若要使用client.py获取cookie，必须执行步骤3</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>点击support文件夹，下载两个exe文件到本地。如果版本不是78.0.3904.108，双击chormesetup安装浏览器。</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>将chormedriver放到python所在路径下</p>
<h3>程序使用</h3>
<p>1、若下载非VIP章节，直接下载main_txt.py或main_epub.py，双击运行。<b>主要更新epub格式下载的程序，因为我发现epub文件大小居然比txt小，读起来也方便。</b></p>
<p>　　(注：main_txt.py可将小说保存为txt格式，main_epub.py可将小说保存为epub格式)</p>
<p>2、运行文件后输入小说编号。（若小说网址为“http://www.jjwxc.net/onebook.php?novelid=2710871” ，那么2710871就是小说编号。）</p>
<p>3、若下载VIP章节，登陆晋江（建议使用edge浏览器或IE浏览器），右键点击“检查”，或按F12进入开发者模式</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>点击console（控制台）按钮，输入document.cookie &#160; ，按回车，按照代码注释复制到main_txt.py|main_epub.py文件header中的指定位置</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>或者直接打开client.py，按步骤输入用户名密码，将得到的值赋给main_txt.py|main_epub.py的header</p>
<p>　　(注：cookie若失效，请及时更换)</p>
<p><span class="Apple-tab-span" style="white-space:pre">	</span>保存main_txt.py|main_epub.py，运行文件</p>
<p><b>若epub文件有问题，可以用sigil修复一下，本人建议使用0.9.14版本。</b></p>
<h1>main_epub功能描述&更新记录</h1>
<p>&#160;2019-12-19增添功能</p>
<p></p>
<ul>
 <li>优化封面后乱码问题</li>
 <li>优化内容简介和标题不匹配</li>
<li>新增繁转简转换功能（若不需要此功能，将含有HanziConv.toSimplified的所有行删除）</li>
 <li>若想实现简转繁功能，将所有HanziConv.toSimplified替换为HanziConv.toTraditional即可</li>
</ul>
初始功能：<p></p>
<p></p>
<ul><li>添加封面（若不需要，将包含"C.xhtml"和"p.jpg"的所有行删除）</li>
<li>添加两级目录（若不需要添加目录，删除"create_tox"函数）</li>
<li>通过cookie下载已购买VIP章节</li>
</ul>
