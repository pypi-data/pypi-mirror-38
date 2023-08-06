# allennlp_wordsplitter_corenlp

Add a [CoreNLP] `WordSplitter` into [AllenNLP]'s tokenizers.

## config

```js
{
  "dataset_reader": {

    // ... ...

    "tokenizer": {
      "word_splitter": {
        "type": "corenlp_remote",
        "url": "http://10.1.1.174:9000"
      }
    },

    // ... ...

  },

  // ... ...

}
```

## CLI

```sh
allennlp train --include-package allennlp_wordsplitter_corenlp -s /your/output/dir /your/training/config/file
```

------
[AllenNLP]: https://allennlp.org/
[CoreNLP]: https://stanfordnlp.github.io/CoreNLP/
