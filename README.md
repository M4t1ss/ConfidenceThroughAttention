# Confidence Through Attention
Use attention alignments from neural machine translations to get a confidence score on how well the text has been translated.
In addition, the same score can be used to compare translations (with attentions) from multiple NMT systems and perform hybrid selections of the best outputs.


Usage:
  - Train a neural MT system ([Neural Monkey](https://github.com/ufal/neuralmonkey/) and/or [Nematus](https://github.com/rsennrich/nematus/))
    - Get source + translated texts + NumPy 3d tensor of alignments from Neural Monkey
    - Get translations together with alignments in one file from Nematus
  - Score one or the other, or combine both in a hybrid
    - Nematus
    ```sh
    python score.py -f Nematus -a test_data/nem.out.ali.lv
    ```
    - Neural Monkey
    ```sh
    python score.py -f NeuralMonkey -a test_data/nm.alignment.npy -s test_data/nm.bpe.en -t test_data/nm.out.bpe.lv
    ```
    - Hybrid
    ```sh
    python hybrid.py -nem test_data/nem.out.ali.lv -nm test_data/nm.alignment.npy -s test_data/nm.bpe.en -t test_data/nm.out.bpe.lv
    ```

Parameters for score.py:

| Option | Description                   | Required 		 | Possible Values 			 		| Default Value  |
|:------:|:------------------------------|:-----------------:|:---------------------------------|:---------------|
| -a     | Input alignment file			 | Yes     			 | Path to file						|				 |
| -s     | Source sentence subword units | For Neural Monkey | Path to file			  	 		|				 |
| -t     | Target sentence subword units | For Neural Monkey | Path to file			  	 		|				 |
| -f     | Where are the alignments from | No     	 		 | 'NeuralMonkey', 'Nematus' 		| 'NeuralMonkey' |


Parameters for hybrid.py:

| Option | Description                                 | Required   | Possible Values |
|:------:|:--------------------------------------------|:----------:|:----------------|
| -nem    | Nematus alignment file		               | yes	    | Path to file	  |
| -nm   | Neural Monkey alignment file	               | yes	    | Path to file	  |
| -s     | Neural Monkey source sentence subword units | yes		| Path to file	  |
| -t     | Neural Monkey target sentence subword units | yes 		| Path to file	  |

	
Publications
---------

If you use this tool, please cite the following paper:

Matīss Rikters and Mark Fishel (2017). "[Confidence Through Attention.](http://aamt.info/app-def/S-102/mtsummit/2017/research-track/)" In Proceedings of the 16th Machine Translation Summit (MT Summit 2017) (2017).

```
@inproceedings{Rikters-Fishel2017MTSummit,
	author = {Rikters, Matīss and Fishel, Mark},
	booktitle={Proceedings of the 16th Machine Translation Summit (MT Summit 2017)},
	title = {{Confidence Through Attention}},
	address={Nagoya, Japan},
	year = {2017}
}
```