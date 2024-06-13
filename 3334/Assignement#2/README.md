### MOVIE -> STOCK analysis


Algorithm: 
step 1: Provide production company name and its code in yahoo finance. 

step 2: Use MovieScraper class to scrape the movies by the production company. 
        inside the MovieScraper following things happen : ( download all movies detail, get only the relased movies, sort movies based on ratings.)

step 3: For a given movie: 
    step 3.0: Find the sentiment, polarity, subjectivity of the movie discription. 
    step 3.1 : get date 15 days before relase date and 15 days after relase date. 
    step 3.2 : scrape data between 2 dates using StockScraper class. 
    step 3.3 : Initialize the Visualizer class.
        step 3.3.1: Plot the Open, High, close of the data. 
        step 3.3.2: Plot the closing price with movie relase date annotated.
        step 3.3.3: Get data after the relase date of the move and Train a regressor on those 15 days of data and plot the regression line. 


Input Details:

1. You start by providing the name of a production company and its corresponding code on Yahoo Finance.
   
2. MovieScraper Class:
    You then use a MovieScraper class to gather details about movies produced by that company.
    This involves:
    Downloading all movie details.
    Filtering the list to include only released movies.
    Sorting these movies based on their ratings.
    Processing Each Movie:

3. For each movie:
    Sentiment Analysis: Determine the sentiment, polarity, and subjectivity of the movie description.
    Date Range: Identify a time window from 15 days before the release date to 15 days after the release date.
    StockScraper Class: Use a StockScraper class to collect stock data for this time window.
    Visualizer Class: Use a Visualizer class to:
        Plot the Open, High, and Close prices of the stock data.
        Plot the closing prices with an annotation for the movie's release date.
        Train a regression model on the stock data for the 15 days following the release date and plot the regression line.


graph TD;
    A[Input: Production Company Name and Yahoo Finance Code] --> B{MovieScraper Class};
    B --> C[Download all movie details,\nFilter only released movies,\nSort movies by ratings.];

    C --> F{Process Each Movie};
    F --> G{Sentiment Analysis};
    G --> H[Movie Description];
    F --> I{Date Range\nTime window: 15 days before and after release};
    I --> J[Identify time window: 15 days before and after release];
    J --> K{StockScraper Class};
    K --> L[Collect stock data for time window];
    L --> M[Stock data];
    M --> N{Visualizer Class};
    N --> O[Plot Open, High, Close prices];
    N --> P[Plot closing prices with release date annotation];
    N --> Q[Train regression model on stock data after movie is relased];
    Q --> R[Plot regression line];



graph TD;
    A[Input: Production Company Name and Yahoo Finance Code] -->|Step 1| B{MovieScraper Class};
    B -->|Step 2| C[Download all movie details,<br>Filter only released movies,<br>Sort movies by ratings.];

    subgraph Process
        C -->|Step 3| F{Process Each Movie};
        F -->|Step 4| G{Sentiment Analysis};
        G -->|Step 5| H[Movie Description];
        F -->|Step 4| I{Date Range<br>Time window: 15 days before and after release};
        I -->|Step 5| J[Identify time window: 15 days before and after release];
    end

    subgraph Stock
        J -->|Step 6| K{StockScraper Class};
        K -->|Step 7| L[Collect stock data for time window];
        L -->|Step 8| M[Stock data];
    end

    subgraph Visualization
        M -->|Step 9| N{Visualizer Class};
        N -->|Step 10| O[Plot Open, High, Close prices];
        N -->|Step 10| P[Plot closing prices with release date annotation];
        N -->|Step 11| Q[Train regression model on stock data after movie is released];
        Q -->|Step 12| R[Plot regression line];
    end




            A - 15         A                  A + 15