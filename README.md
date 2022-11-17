# SpeedMeasure
## 简介
SpeedMeasure是一款开源测试工具，用于精确测量耗时，例如App的冷热启动速度。
## 安装
1.支持Mac、Windows和Linux安装；  
2.git clone下载工程后，在根目录下运行“python run.py”即可启动服务； 
![image](https://github.com/wensj845/SpeedMeasure/tree/master/img/startserver.png)  
3.浏览器访问http://127.0.0.1:12355/ 。
## 使用技巧
1.在手机上录制视频（例如App启动过程），目前只支持mp4格式；  
2.上传视频后，耐心等待SpeedMeasure自动解帧；  
3.人工选定开始帧和结束帧后，点击“计算”按钮，计算耗时；  
4.点击保存按钮记录测试结果（需提前使用管理员账号创建项目和功能点）；  
5.SpeedMeasure支持智能选帧，人工挑选开始帧和结束帧后，点击“保存基线”按钮可以创建某个测试场景的基线数据，后续重复测试该类场景时，可以点击“智能选帧”按钮，让SpeedMeasure基于AI算法智能选帧。  
## 权限控制
1.SpeedMeasure有两类用户：普通用户和管理员用户，新注册用户默认为普通用户,普通用户无法看到“系统设置”界面，也无法删除历史数据；  
2.如果需要将普通用户转换为管理员用户，需要修改sqllite数据库（SpeedMeasure.db），将user表中对应用户的administrator字段从0改为1。
