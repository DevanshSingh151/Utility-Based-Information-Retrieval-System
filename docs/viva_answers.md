# Viva Preparation Answers
Q1: What is the core learning mechanism utilized?
A: We use a Bayesian posterior update model. The priors are uniformly distributed at first and dynamically update weights depending on the features of documents the user clicks.

Q2: Why use a Cross-Encoder rather than just Sentence Transformers?
A: Cross-encoders output actual classification probabilities comparing the query strings together, leading to vastly higher accuracy although at higher latency cost.

Q3: How does Module 1 map to this exact project?
A: The utility agent ranks documents via an objective utility function dot-product computation, making it a classic Utility Agent under Russell & Norvig definitions.
