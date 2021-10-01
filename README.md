# Graphene_Finder
Autonomous robotic searching of graphene

## Note
Before running this file, you should replace the folder named my_model by your own model

## 概念說明
控制顯微鏡掃描整個樣品並拍下照片，完成後利用tensorflow掃描是否有graphene存在。偵測結果會存在Detection result資料夾，內有辨識後的圖片與txt文字檔，txt內有紀錄圖片座標。使用者輸入座標即可將顯微鏡移至該位置。為了達到這項目標，程式必須有三個部分，分別是移動顯微鏡、對焦並存下照片、辨識。

## 檔案說明
- coordinate_creator.py
    - 規劃顯微鏡掃描的路徑
    - 輸入起點座標後執行該程式，即可看到預計掃描路徑
- getCCDphoto.py
    - 擷取顯微鏡畫面
	- 該檔案另有清晰度分析功能
- microscope_controller.py
    - 控制顯微鏡模組並附加自動對焦
	- 該檔案利用分析清晰度取得最佳對焦位置
- graphene_detection.py
    - 辨識graphene並將儲存結果
- main.py
    - 主程式
    - 使用者執行該檔案即可開始掃描

## 安裝
- Pandas
- PyWin32
- OpenCV
- PySerial
- TensorFlow 2 Object Detection API

## 操作步驟
1. 關閉Prior Demo x64
2. 設定esp301
	Menu → Run program → 數字3 → Run
	(恢復設定為Menu → Run program → 數字1 → Run)
3. 打開SpinView、CCD
4. 將載物台轉正
5. 打開紅十字(Draw center cross hair)
6. 放樣品並確定樣品是正的
4. 將Blackfly S BFS-U3-51S5C 19370957視窗拉出並調至適當大小
4. 打開Spyder(tensorflow)
5. 執行main

## 重新偵測照片
1. 執行detect_again.py
2. 輸入要偵測的資料夾名稱
3. 輸入過濾多少機率以下的照片 Ex: 0.7