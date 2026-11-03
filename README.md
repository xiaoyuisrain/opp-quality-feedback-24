# Automatic feedback for OPP texts

This repo contains the code (.py files), prompt, experiment results (.json files), and report for the study \enquote{Automatic feedback for OPP texts}, where I tested state-of-the-art LLMs on their capabilities to produce rubric-based quality feedback for Dutch OPP texts.

Use `test_deepseek.py` and `test_gemini.py` to run the main experiments.
Provide a range of OPP documents you would like to query as follows:

```
python test_{model_name}.py {range_start} {range_stop}
```

For example, `0 10` runs the experiments through the first 10 documents.

Use `test_gemini_further.py` to run the additional experiment that employs Gemini's own PDF processing engine.
No additional arguments are needed; the code loops through the 5 randomly selected documents by default.

You can test the DeepSeek model and the Gemini model in parallel---the two main experiments do not interfere with each other.
However, please do not run `test_gemini.py` and `test_gemini_further.py` at the same time, as they write to the same output file.