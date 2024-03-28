"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from .gpt_utils import (
    generate_ticker_ideas,
    get_analyst_ratings,
    get_current_price,
    get_final_analysis,
    get_industry_analysis,
    get_sentiment_analysis,
    get_stock_data,
)
from rxconfig import config

import reflex as rx

prices = {}


class State(rx.State):
    """The app state."""

    industry: str = ""
    tickers: dict[str, str]
    analyses: dict[str, str]
    # What stage the analysis is: "stopped", "analyzing", "ranking"
    stage: str = "stopped"

    def handle_submit(self, data: dict):
        if data["industry"]:
            self.industry = data["industry"]
            self.tickers = generate_ticker_ideas(self.industry)
            self.stage = "analyzing"
            print(self.stage)
            return State.fetch_analyses

    @rx.background
    async def fetch_analyses(self):
        for ticker in self.tickers.keys():
            async with self:
                self.tickers[ticker] = "processing"
            print(f"\nAnalyzing {ticker}...")
            hist_data, balance_sheet, financials, news = get_stock_data(ticker, years=1)
            # main_data = {
            #     "hist_data": hist_data,
            #     "balance_sheet": balance_sheet,
            #     "financials": financials,
            #     "news": news,
            # }
            sentiment_analysis = get_sentiment_analysis(ticker, news)
            analyst_ratings = get_analyst_ratings(ticker)
            industry_analysis = get_industry_analysis(ticker)
            final_analysis = get_final_analysis(
                ticker, {}, sentiment_analysis, analyst_ratings, industry_analysis
            )
            prices[ticker] = get_current_price(ticker)
            async with self:
                self.analyses[ticker] = final_analysis
                self.tickers[ticker] = "finished"
        async with self:
            print(self.stage)
            self.stage = "ranking"


def ticker_progress(ticker_kv: list[str]) -> rx.Component:
    """Args: ticker_kv is [key, value]"""
    return rx.hstack(
        rx.text(ticker_kv[0], size="7"),
        rx.cond(
            ticker_kv[1] == "finished",
            rx.icon(
                tag="check-check", height="2em", width="2em", color="rgb(149,134,106)"
            ),
            rx.chakra.circular_progress(
                value=0, is_indeterminate=(ticker_kv[1] == "processing")
            ),
        ),
        spacing="4",
        align="center",
        width="10em",
    )


def ticker_progress_block() -> rx.Component:
    return rx.vstack(
        rx.foreach(State.tickers, ticker_progress),
        align="start",
    )


def ranking_item(analysis_kv: list[str]) -> rx.Component:
    return rx.accordion.item(header=analysis_kv[0], content=analysis_kv[1])


def ranking_block() -> rx.Component:
    return rx.vstack(
        rx.text("Final Ranking"),
        rx.accordion.root(
            rx.foreach(State.analyses, ranking_item),
            collapsible=True,
            width="500px",
            variant="soft",
        ),
        align="start",
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            # rx.theme_panel(),
            rx.heading("Claude Investor", size="9"),
            rx.text.em("This is not investment advice", font_size="1em"),
            rx.form(
                rx.hstack(
                    rx.input.input(
                        placeholder="Enter the industry to analyze",
                        id="industry",
                        width="250px",
                    ),
                    rx.button("Go", type="submit"),
                    width="250px",
                ),
                on_submit=State.handle_submit,
            ),
            rx.cond(
                State.stage == "analyzing",
                ticker_progress_block(),
            ),
            rx.cond(
                State.stage == "ranking",
                ranking_block(),
            ),
            align="center",
            spacing="7",
            font_size="2em",
        ),
        height="100vh",
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="gold"
    ),
)
app.add_page(index, title="Claude Investor | Reflex")
