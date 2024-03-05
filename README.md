# AI FACE

仕組みについては[こちらを参照](https://github.com/Minminzei/ai-sample/issues/1)

## 環境構築
### 1. dockerコンテナビルド
```
docker-compose build
```
### 2. dockerコンテナに入る
```
docker-compose run --rm faceswap-dev
```

### 1. PrePare Images
1. `resources/originals/{input_a, input_b, convert}`に素材となるmp4動画をおいてください。
2. 次のコマンドで動画を画像に変換します。
```
python files.py video_to_images -n {変換したいフォルダ:input_a, input_b, convert} -f {FPS}
```

### 2. Extract
1. 抽出する
```
python extract.py extract -n {抽出したいフォルダ:input_a, input_b, convert} 
```
2. 顔写真をクラスタリングする
```
python extract.py sort_by_face -n {input_a, input_b, convert} 
```
3. 不要な顔写真を目視で削除後、alignmentsファイルをクリーンアップする
```
python extract.py clean_up -n {input_a, input_b, convert} 
```

### 3. Training
```
python train.py train -t {使用するモデル:lightweight, realface etc}
```
＊previewは`lib/training_preview.png`に出力される。

### 4. Convert
1. 変換元の動画を画像に変換
```
python files.py video_to_images -n convert
```

2. Extract
```
python extract.py extract -n convert
```

3. 変換する
```
python convert.py convert
```

4. 画像から動画を復元する
```
python files.py images_to_video -f {FPS}
```
