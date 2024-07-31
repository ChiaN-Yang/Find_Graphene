# Graphene_Finder
<a href="#"><img src="https://img.shields.io/badge/TensorFlow-2.5-FF6F00?logo=tensorflow" /></a>

Deep Learning-based Automatic Searching for Graphene

----

## 摘要
自動掃描石墨烯(graphene)的機器人系統。利用USB控制顯微鏡平台自動掃描樣品、自己設計簡易的自動對焦程式，並利用深度學習模型達到辨識石墨烯的目標，以加速製備石墨烯的過程。此機器人系統將節省研究生數小時的時間，掃描石墨烯樣品的工作可完全由機器人負責。

## 動機
石墨烯為目前最火熱的二維材料之一，它只有一個原子厚，硬度卻超過金剛石，它的發現很可能促成量子電腦的發明。目前成大前沿量子科技研究中心製備石墨烯還是以機械剝離法(mechanical exfoliation)為主，然而該方法需要研究人員花數個小時的時間，用顯微鏡觀察多個樣品(圖一)，並在樣品中尋找淺紫色的目標物(圖二)。其步驟非常制式化，若能用電腦工作將會替研究人員省下大筆時間。

![mono layer graphene](https://i.imgur.com/TnGdzdg.png)

## 程式目標
1. 控制顯微鏡掃描整個樣品並拍下照片
2. 利用深度學習模型辨識照片中是否有石墨烯存在
3. 將偵測結果存在指定資料夾，內有辨識後的圖片與目標物在顯微鏡平台的座標
4. 使用者輸入座標即可將顯微鏡移至該位置

![](https://i.imgur.com/TmkKgVM.png)

顯微鏡自動掃描與對焦[影片](https://youtu.be/ObPmyX3FzXE)

## 程式架構
程式分為三個部分，分別是coordinate creator、microscope controller、TensorFlow Object Detection。主程式首先呼叫coordinate creator用來規劃顯微鏡掃描路徑，顯微鏡會依路徑以S型掃描整個樣品。microscope controller負責移動與對焦顯微鏡，並將所得到的影像回傳到主程式。主程式這時會將影像圖片送給TensorFlow Object Detection辨識，辨識結果將以一個資料夾儲存起來。

![程式架構](https://i.imgur.com/w70vTOD.png)

## 物件偵測結果展示
以下為透過深度學習模型所輸出的辨識結果，包含目標位置(bounding boxes)、物件類別(class labels)和信心指數(confidences)。依下圖範例，綠色方塊是石墨烯位置、物件類別是graphene、信心指數是94%。

![物件偵測結果](https://i.imgur.com/SXpvCkP.png)

## 程式設計
1. coordinate creator

    coordinate creator讓使用者設定顯微鏡的倍率、基板的邊長、顯微鏡起始位置。有了這三項參數，程式將會回傳一個一維陣列，裡面包含將掃描的位置座標。
    ![coordinate creator](https://i.imgur.com/gcjoe6W.png)

2. microscope controller

    利用USB跟顯微鏡移動平台進行通訊，成功的讓顯微鏡移動到指定座標，卻沒預料到載物台是斜的，拍下的照片完全失焦。於是我決定自己設計對焦模組，首先在同一位置調整焦距拍下多張照片，使用OpenCV辨識照片的清晰度，接著讓焦距調整到清晰度最高的位置，簡易的對焦系統就完成了。
    ![microscope controller](https://i.imgur.com/ugvOTMX.png)

3. TensorFlow Object Detection

    Google提供完整的物件偵測API，且裡面的物件偵測演算法可以任意更換。我這邊使用Hourglass Network提取目標特徵，並用CenterNet演算法進行物件偵測。

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

In vscode, it can be installed with pip:

    python -m pip install -r requirements.txt

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

## Note
Before running this file, you should replace the folder named my_model by your own model
