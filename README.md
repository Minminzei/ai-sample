# FaceSwapサンプル

## 環境構築
### 1. dockerコンテナビルド
```
docker-compose build
```
### 2. dockerコンテナに入る
```
docker-compose run --rm app
```
### 3. 変換したい素材動画を静止画像に変換する
```
python resources.py -o {保存するフォルダ名(半角英字)} -i {動画パス: Ex. resources/inputs/HD.mp4}
```

### 1. Extract
```
# 抽出する
python run_faceswap.py extract -n {対象の人物名(半角英字)}
# 顔写真をクラスタリングする
python run_faceswap.py sort_by_face -n {対象の人物名(半角英字)}
# 不要な顔写真を削除後、alignmentsファイルをクリーンアップする
python run_faceswap.py clean_up -n {対象の人物名(半角英字)}
```

### 2. Training
```
```

### 3. Convert
```
```

# FaceSwapについて

以下はFaceSwapについて[FaceSwap: Extract](https://forum.faceswap.dev/viewtopic.php?f=5&t=27)と[FaceSwap: Training](https://forum.faceswap.dev/viewtopic.php?f=6&t=146)の内容を整理したものです。

## 1. Overview
顔生成のニューラルネットワークではデータセット(顔写真)をvectorにエンコーディングして、デコーダーでvectorから顔を生成する。入力された顔と出力された顔の乖離度を損失として評価して、改善されている場合はWeightsを更新する。
<img src="https://forum.faceswap.dev/download/file.php?id=139"  />

上記NNでは顔を認識しreconstructすることができるが、DeepFakeの目的は「Aの顔を認識して、Bの顔に差し替える」ことなので、FaceSwapは上記NNに`Shared Encoder`と`Switched Decoders`という概念を追加して拡張させる。
<img src="https://forum.faceswap.dev/download/file.php?id=141" />

### Shared Encoder
Trainingにおいて2人のデータセットを一つのEncoderにfeedし、2つのDecoderを学習させる。Decoder AはAの顔を、Decoder BはBの顔を生成する。

### Switched Decoders
Convertingにおいて、Aの顔を入力して学習させたDecoder Bに通すことで、AとBの顔を差し替える。

## 2. [Extract](https://forum.faceswap.dev/viewtopic.php?f=5&t=27)
ディープラーニングにあたえるデータセット(Facial sets)を準備する。

### 2-1. Facial sets作成フロー
Facial setsは次の3段階を経て作成される。
1. Detection
対象の写真から顔を認識し、正方形の写真に切り抜く。

![25CCD2F400000578-2958597-image-a-27_1424270103152](https://github.com/Minminzei/faceswap_sample/assets/3320542/01c721a1-515b-484c-b826-6c3eac306195)


2. Alignment
正方形の顔写真に対して68個のlandmarksをつける。landmarksの座標情報は正方形写真のメタデータに追記される。

<img src="https://miro.medium.com/max/828/1*96UT-D8uSXjlnyvs9DZTog.png" width="300" />

3. Mask
正方形の顔写真に対して背景から顔の箇所を抽出する。この情報も正方形写真のメタデータに追記される。

<img src="https://forum.faceswap.dev/download/file.php?id=587&sid=ea0d317156907824a87904533e236925" />

#### Extractフロー
![無題の図形描画](https://github.com/Minminzei/faceswap_sample/assets/3320542/4487c88e-26fa-42fb-9d17-40eb9a2b58bb)

### 2-2. 高品質な素材データを集める
- 様々な角度、表情、光の加減の写真データを1,000〜10,000集めて学習させる。
- 全体的に写真データは明瞭であるべき(sharp and detailed)。しかしながら一部のデータが不明瞭(blurry/partially obscured)なのはモデルの学習にプラスなのでOK。割合は5%未満を目処にする。

<img src="https://i.imgur.com/5L5sAUa.png" />

### 2-3.  Facial setsから不要な写真を削除する
複数の人物が写っている写真をExtractした場合、対象の人物以外もFacial Setsに含まれてしまう。また同じ人物の同じ写真が複数含まれてしまった場合も、Facial setsの品質が落ち、学習の精度が落ちてしまうので不本意な顔写真を目視で削除する必要がある。

大量の写真から不要データを目視で削除するのは大変である。そこで`Sort By Face`で似た写真をグルーピングする(教師なし学習によるクラスタリング)。そうすることで同じ写真は同じグループに収まり、別人物の画像はまとめてフォルダに配置されるので削除作業の効率能率的になる。

### 2-4. Clean Up alignment.fsa file
`Sort By Face`で不要な顔写真を削除したら、再度Extactを実行してfsaファイルを更新する。

## 3. [Training](https://forum.faceswap.dev/viewtopic.php?f=6&t=146)
Extractで準備したFacial Setsを学習させる。Trainingでは設定(Configure)の組み合わせを試行錯誤することで訓練の質を改善できる。ベストな組み合わせは決まっておらず、またアウトプットの評価は主観的になるため(スワップがどれくらいの精度でできたかは判定できない`there are no real-world examples of a swapped face for the NN to compare against.`)、本格的に運用する際には体系的な比較フローを構築すると良さそう。詳細は`config/train.ini`を参考。

### 3-1. どのModelを使うか？
利用可能なモデルを一部抜粋。モデルは進化＆新しいものが追加されるのでウォッチする。

| モデル | 概要 | input/ output | カスタム設定  |
| -------- | ------------------------------------ | --- | --- |
| Lightweight | 開発用の超軽量モデル。本番では使用しないがローカルでのコーディングやデバッグ時には良さそう | 64px/ 64px | ? |
| IAE  | EncoderとDecoderの間にIntermediate layersを追加したモデル。https://github.com/deepfakes/faceswap/pull/251  |  64px/ 64px | ? |
| Dfaker  | input画像を高解像度にアップスケールしてoutputすることに強いモデル。RealfaceやDlightに継承されている |  64 or 128px/ 128 or 256px | ☓ |
| Villain | ハイスペックなVRAMと十分な訓練が必要なモデル。  |  128px/ 128px | ☓ |
| Realface  | B Decoderに重きをおいたモデルでAからBへのスワップに強い(逆は弱い)。Dfakerも継承してアップスケールもできる。 |  64-128px/ 64-256px | ◯ |
| Dlight  | Dfakerを継承した最新版。アップスケールに強い。  | 128px/ 128-384px | ◯ |
| Phaze-A  | 複雑なモデルで専用のスレッドがある。初学者が使うのは敷居が高いらしい。https://forum.faceswap.dev/viewtopic.php?f=27&t=1525  | ？ | ◯ |

### モデルのアウトプット例
#### Phaze-A model

[<img src="https://user-images.githubusercontent.com/36920800/178301720-b69841bb-a1ca-4c20-91db-a2a10f5692ca.png"  />](https://www.dailymotion.com/video/x810mot)

#### Villain
<img src="https://camo.githubusercontent.com/64e9770523a74e1c3f43a3b04c8625c15bcc8dbf0096b2e43cb396bc1e6c3409/68747470733a2f2f696d672e796f75747562652e636f6d2f76692f72316a6e673739613578632f302e6a7067" />

### 3-2.  initializerに何を使うか？
initializerは学習初期のWeightを決めてくれ学習を効率的にする。現在対応しているinitializerは`he_uniform(default)`, `ICNR Init`, `Conv Aware Init`の3つ。それぞれの特徴は論文を読まないとわからない。
[ICNR Init](https://arxiv.org/abs/1707.02937)
[Conv Aware Init](https://arxiv.org/abs/1702.06295)

### 3-3. Optimizerをどう設定するか？
最適化(Optimizer)については[こちらの記事](https://qiita.com/omiita/items/1735c1d048fe5f611f80)を参照。
- アルゴリズムは定評があるAdamを使うのが推奨されている。
  - オプション的にはAdaBeliefやNadamなども準備されている 。
- Learning Rate: 小さいと収斂まで時間がかかる。とりあえずデフォルトで良さそう。
- Batch Size: 一度に何個のデータを学習させるか？1-32で指定できる。大きいほど学習の質は上がるが学習速度が遅くなる。
- Epsilon Exponent: `divide by zero errors`を避けるためのもの。これもデフォルトで良さそう。

### 3-4. 損失関数をどう設定するか？
- デフォルトではSSIM (Structural Similarity)が設定されている。損失関数は正則化関数を組み合わせたりできる。

### 3-5. monitorning:いつ学習を終えるか？
学習中はiterationごとに`Total Iterations: 87 | Loss A: 0.0411 Loss B: 0.0451`というフォーマットでDecoderA, Bの損失を出力してくれる。しかしながらこの損失はインプットデータから人物A、Bをうまく生成できたかの指標で、人物AをBに差し替えたスワップ写真の品質を示すものではない。そもそもそのようなスワップ写真はこの世に存在せず、スワップにおける損失を測ることができない。そのため最終的な品質は目視で確認することになる。

modelが保存されるたびにスワップ実行時のpreview画像が作成されるので、それらを目視して十分な品質に達したと判断したら学習を終える。目の光加減と歯の形は最後に学習される傾向にあるので、この２つに注目して判断すると良いらしい。
<img src="https://forum.faceswap.dev/download/file.php?id=190" />

### 3-6. pre-trained modelをどうするか？
一般にスクラッチでモデルを作るのではなく事前学習モデルをファインチューニングするほうが学習の効率・質が上がりそうだが、FaceSwapに事前学習モデルは準備されていない。どういったモデルが事前学習に使えるのかなど検討が必要。
[Deepfake Video Forensics based on Transfer Learning](https://arxiv.org/abs/2004.14178)

## 4. Converting
Trainingで使った人物AのAlignment Fileとは**違う**人物Aの動画データをExtractしてスワップを行う。

## 5. 実行環境をどうするか？
コーディングとデバッグはローカル環境で行い、GPUが必要な学習はColabなど別環境で行う

