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
- get_ccd_photo.py
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