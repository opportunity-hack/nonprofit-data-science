# Crawler
This grabs text from several nonprofit websites and slings them into text files.
```
pip install scrapy
cd npocrawler
scrapy crawl quotes
```
You can see the text files in their respective directories within the `npocrawler/` directory

# Summarization
To summarize the data from text files, use the following command:
```
python summarize.py
```

## Example output
For `npocrawler/site_positivepathsaz_org/text-.txt`

```
- Original text was 2970 characters and 421 words
- Broke text into 1 batches to support summarization
```
> ```Summary: Positive Paths is a 501(c)(3) non-profit organization serving women and their families in the East Valley of Phoenix, Arizona. We support East Valley women by providing a life bridge to economic stability, personal growth and professional achievement. We believe that empowering women to be key change agents is an essential element to achieving a world that works for everyone.```

For `npocrawler/site_sarsef_org/text-.txt`
```
- Original text was 3166 characters and 458 words
- Broke text into 1 batches to support summarization
```
> ```Summary: SARSEF is creating Arizona’s future critical thinkers and problem solvers through science and engineering. Every SARSEF program uniquely prepares students for the future by giving them the tools and support they need to think like scientists and engineers. Students go on to become neurosurgeons, cancer researchers, engineers, wildlife conservationists, veterinarians, teachers and professors, journalists.```
