# Claude Investor

Based on the [gpt-investor](https://github.com/mshumer/gpt-investor) by
[Matt](https://twitter.com/mattshumer_). See the [original README](notebooks/README.md) for more details.

This is an app built using [Reflex](https://github.com/reflex-dev/reflex). The AI prompts, data fetching and processing logic are directly lifted from the [notebook](notebooks/Claude_Investor.ipynb). The UI elements and the reactivity are built using Reflex.

## Prerequisites

To run the code, you need to have an Anthropic API key. You can get one by signing up at [Anthropic](https://anthropic.com/).

## Requirements

As specified in the pyproject.toml file, the following packages are required to run the code:

```txt
yfinance
requests
beautifulsoup4
reflex==0.4.5
```

These are the defaults added by poetry. Relaxed versions of some of these packages likely work as well.

## Environment variables

The app reads two environment variables `ANTHROPIC_API_KEY` and `MAX_TICKERS_TO_ANALYZE`. `MAX_TICKERS_TO_ANALYZE` is part of the prompt to Claude for how many tickers it returns for further analysis, defaults to `4` right now. The analysis takes a bit of time to run.

```bash
export ANTHROPIC_API_KEY="your_api_key"
```

## Running the app

This app is based on [Reflex](https://github.com/reflex-dev/reflex) framework. In the top level directory (this directory has a file named `rxconfig.py`), run the following commands to run the app:

```bash
reflex init
reflex run
```

Also check out [Reflex Documentation](https://reflex.dev/docs/getting-started/introduction/) to build/run/host your own app.

## Background | Excerpt from the original README

Below is part of the original README on the implementation.

### Claude-Investor | The first release in the gpt-investor repo

Claude-Investor is an experimental investment analysis agent that utilizes the Claude 3 Opus and Haiku models to provide comprehensive insights and recommendations for stocks in a given industry. It retrieves financial data, news articles, and analyst ratings for companies, performs sentiment analysis, and generates comparative analyses to rank the companies based on their investment potential.

### Workflow

- Generates a list of ticker symbols for major companies in a specified industry
- Retrieves historical price data, balance sheets, financial statements, and news articles for each company
- Performs sentiment analysis on news articles to gauge market sentiment
- Retrieves analyst ratings and price targets for each company
- Conducts industry and sector analysis to understand market trends and competitive landscape
- Generates comparative analyses between the selected company and its peers
- Provides a final investment recommendation for each company based on the comprehensive analysis, including price targets
- Ranks the companies within the industry based on their investment attractiveness

### Disclaimer

Claude-Investor is an educational and informational tool designed to assist in investment analysis. It should not be considered as financial advice or a substitute for professional investment guidance. Always conduct thorough research and consult with a qualified financial advisor before making any investment decisions.
