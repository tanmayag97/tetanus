# Global Burden of Tetanus Dashboard 

Tetanus is a bacterial infection that leads to painful muscle contractions, typically beginning in the jaw and then progressing to the rest of the body. In recent years, tetanus has been fatal ‘in approximately 11% of reported cases.


## The Contributors

I am a [student](https://github.com/tanmayag97) at UBC, Vancouver, part of the Master of Data Science program:


## Overview

The dataset for this dashboard is extracted from this [website](https://ourworldindata.org/tetanus). The motivation, purpose, description of data and research question can be found in our [proposal](https://github.com/tanmayag97/tetanus/blob/main/docs/proposal.md).

## Usage

This dashboard is designed to help healthcare professionals and policymakers gain insights into the global burden of tetanus. With its three visualizations, users can explore the following questions:

1. What is the number of tetanus cases per million people in a specific year across different countries? This information can help users understand the burden of tetanus in different regions and identify countries that may need more attention in terms of prevention and treatment.

2. Which continent has the highest number of tetanus cases per million people? This visualization provides a high-level view of the burden of tetanus across different continents and can help users identify regions that need more targeted interventions.

3. How does the incidence of tetanus vary across different age groups in a specific country? This information can help users understand which age groups are most vulnerable to tetanus and design targeted interventions to prevent and treat the disease.

The dashboard also provides users with various filtering options, including the ability to select a specific year of interest, continent of interest, and country of interest. This feature can help users identify patterns in the data that may not be immediately obvious and gain a deeper understanding of tetanus globally.

The 3 types of visualizations included are:

- A world map that shows the number of tetanus cases per million people for a specific year, which can be controlled by a slider.
- A widget where the world map can focus on a specific continent, allowing users to compare the burden of tetanus across different continents.
- A dropdown that gives the options to choose between two charts (Showing a line plot of deaths due to tetanus or incidence of tetanus). Each of these charts have another dropdown linked to them which shows the line chart by choosing a country.

The brief questions answered by this dashboard would be:

- How many cases are there of tetanus in different countries and regions from 1974 to 2020?
- Which continent has the most cases of tetanus?
- How do the deaths of tetanus vary across different age groups in a specific country?


## The Contributing Guidelines
Do you have ideas on how I can improve my dashboard, and are you interested in contributing? I'd love to see your suggestions! To make changes locally just clone the repo, navigate to the top folder, and run the app:

```
git clone https://github.com/tanmayag97/tetanus.git 

cd tetanus

python src/app.py
```

Check out the [contributing guidelines](CONTRIBUTING.md) if you're looking to make additions to this project! Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By contributing to this project, you agree to abide by its terms.

# License 

`tetanus` was created using Dash visualization by Tanmay Agarwal. It is licensed under the terms of the [MIT license](LICENSE).
