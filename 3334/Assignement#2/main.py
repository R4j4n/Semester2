for item in movies_sorted[:3]:

    is_adult_movie = item["adult"]
    movie_name = item["original_title"]
    overview = item["overview"]
    release_date = item["release_date"]
    print("*" * 20, movie_name, "*" * 20)

    print(f"R rate movie: {is_adult_movie}")
    print(f"Movie Overview: {overview}\n\n")

    print(f"Let's perform sentiment analysis of the movie:")
    print("-" * 50)
    sentiment, polarity, subjectivity = get_sentiment(text=overview)
    print(f"Sentiment : {sentiment}")
    print(f"Polarity : {polarity}")
    print(f"Subjectivity : {subjectivity}")
    print(f"\n\n")

    print(f"Relase Date: {release_date}")
    # lets get the time period to check the stock market
    date_before_str, date_after_str = get_dates_around(date_str=release_date)
    print(
        f"For the movie {movie_name}, we will be looking stock market between two time period : {date_before_str}--{date_after_str}"
    )

    print("Downloading stock data: ")
    scraper = StockScraper(yf_ticker=COMPANY_CODE)
    scraped_data = scraper(start_date=date_before_str, end_date=date_after_str)

    # initializer the data visualzier class:
    visualizer = Visualizer(
        data=scraped_data,
        producer_name=PRODUCTION_COMPANY,
        movie_name=movie_name,
        start_date=date_before_str,
        end_date=date_after_str,
    )

    all_plot = visualizer.plot_o_h_l_c_v()

    all_plot.show()

    plot_relase_date = visualizer.plot_relase_date(release_date=release_date)
    plot_relase_date.show()

    # plot the overall relase date and regression line
    reg_plot = visualizer.plot_overall_trends(release_date=release_date)
    reg_plot.show()
