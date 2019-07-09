# KWDLC2NERDataset
[KWDLC](http://nlp.ist.i.kyoto-u.ac.jp/index.php?KWDLC) -> Japanese NER Dataset


## Requirements

- python3


## Usage

1. Download KWDLC from [link](http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/KWDLC/download\_kwdlc.cgi)
2. Do the following

```
git clone https://github.com/s14t284/KWDLC2NERDataset.git
cd KWDLC2NERDataset/
python3 run.py -d /path/to/KWDLC-1.0.tar.bz2
```


## About Dataset

### NE types

- ORG: ORGANIZATION
- PSN: PERSON
- LOC: LOCATION
- ART: ARTIFACT
- DAT: DATE
- TIM: TIME
- MON: MONEY
- PER: PERCENT

### tagging scheme

- IOB2


## make NER dataset script

```
usage: run.py [-h] [-d DATASET] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        KWDLC tar file path. default ./KWDLC-1.0.tar.bz2
  -f FILE, --file FILE  generated dataset path. default ./dataset.txt
```


## References

- 萩行正嗣, 河原大輔, 黒橋禎夫.  
多様な文書の書き始めに対する意味関係タグ付きコーパスの構築とその分析,  
自然言語処理, Vol.21, No.2, pp.213-248, 2014.

- Daisuke Kawahara, Yuichiro Machida, Tomohide Shibata, Sadao Kurohashi, Hayato Kobayashi and Manabu Sassano.  
Rapid Development of a Corpus with Discourse Annotations using Two-stage Crowdsourcing,  
In Proceedings of the 25th International Conference on Computational Linguistics, pp.269-278, 2014.

- Masatsugu Hangyo, Daisuke Kawahara and Sadao Kurohashi.  
Building a Diverse Document Leads Corpus Annotated with Semantic Relations,  
In Proceedings of the 26th Pacific Asia Conference on Language Information and Computing, pp.535-544, 2012.


## Other

I assume no responsibility for using this program
