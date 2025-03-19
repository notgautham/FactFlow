# Fake News Detector Project

This project implements a browser extension that detects fake news using a hybrid approach involving:
1. Content Extraction and Preprocessing
2. Content-Based Analysis (using advanced NLP and deep learning models)
3. Source Credibility Assessment
4. Cross-Referencing with Trusted Sources
5. A Composite Decision Engine

It also reserves a folder for future integration of the DeepSeek API.

## Project Structure
(See the docs/architecture.md file for a detailed explanation.)

## Temp changes for test training with smaller dataset

from train_model.py remove the lines marked by the specific comments
from content_model.py modify  num_train_epochs=2 to 3
