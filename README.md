# security_connection_platform
An automated testing framework
<html>
  <H4> 一.测试框架的使用范围</h4>
    <ul>该框架基于pytest开发，主要用于测试http协议的API。</ul>
  <H4>二.待测API的基本特征</h4>
    <ul>基于http协议进行通讯</ul>
    <ul>Post请求中采用JSON格式组织数据</ul>
    <ul>数据需要进行两次加解密再进行传输</ul>
    <ul>单接口逻辑简单，但对应测试用例数据数量大且范围灵活</ul>
  <H4>三.测试框架设计的基本思路</h4>
    <ul>测试框架主要用于回归测试和版本修改时对已有功能的验证测试（防止修改范围蔓延）</ul>
    <ul>根据API特点进行适当的抽象分离：将多接口公用的部分抽象为工具类</ul>
    <ul>充分利用pytest框架fixture和hook函数的灵活性，实现测试用例数据的灵活扩展和裁剪</ul>
    <ul>使用allure动态完成测试数据的收集，并友好展示</ul>
    <ul>基于已有API功能稳定的考量，测试数据使用数据库来存储。结合pytest的命令行选项和SQL语句实现测试数据的动态获取</ul>
    <ul>测试用例设计时聚焦在测试用例执行的结果，将过程全部封装</ul>
    <ul>持续集成：使用github作为VC工具，Jenkins作为持续集成平台，通过webhook的方式，实现持续集成、邮件发送等功能</ul>
    <ul>后续：探索除数据库以外的其他测试数据存储方式、pytest的多个插件的使用方式（如并发执行等）。</ul>
  
  <H4>三.测试框架的结构</h4>
    <ul>log文件夹存放日志文件</ul>
    <ul>report_src文件夹存放allure需要的源数据</ul>
    <ul>test文件夹存放测试用例</ul>
    <ul>pytest.ini中除了pytest的设置外，还添加了数据库连接、测试环境URL设置、key等信息</ul>
    <ul>conftest.py中是框架实现的hook函数、fixture函数和生成测试用例id的辅助函数</ul>
    <ul>init_config.py读取配置信息，进行框架初始化信息的设置</ul>
    <ul>setting_initial_env.py存放所有接口公用的工具类和方法</ul>
    <ul>sm4decode.py加解密工具模块</ul>
    
</html>
