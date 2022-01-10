# 2021-2022 NHL Season Analysis

## Problem Statement
I want to pick up players who are about to score many power play goals in the coming week.

## Pre-Processing & Feature Engineering
Feature Engineering - Finding the tightest correlated metrics that indicate a player is about to score many power play goals with ensemble method.

The emphasis will be on BorutaPy vs other libraries & algorithms for feature selection.

### Features Considered:
- timeOnIce
- assists
- goals
- pim
- shots
- games
- hits
- powerPlayGoals
- powerPlayPoints
- powerPlayTimeOnIce
- evenTimeOnIce
- penaltyMinutes
- faceOffPct
- shotPct
- gameWinningGoals
- overTimeGoals
- shortHandedGoals
- shortHandedPoints
- shortHandedTimeOnIce
- blocked
- plusMinus
- points
- shifts
- fanPts
- timeOnIce_W (Last Week)
- assists_W (Last Week)
- goals_W (Last Week)
- pim_W (Last Week)
- shots_W (Last Week)
- games_W (Last Week)
- hits_W (Last Week)
- powerPlayGoals_W (Last Week)
- powerPlayPoints_W (Last Week)
- powerPlayTimeOnIce_W (Last Week)
- evenTimeOnIce_W (Last Week)
- penaltyMinutes_W (Last Week)
- faceOffPct_W (Last Week)
- shotPct_W (Last Week)
- gameWinningGoals_W (Last Week)
- overTimeGoals_W (Last Week)
- shortHandedGoals_W (Last Week)
- shortHandedPoints_W (Last Week)
- shortHandedTimeOnIce_W (Last Week)
- blocked_W (Last Week)
- plusMinus_W (Last Week)
- points_W (Last Week)
- shifts_W (Last Week)
- fanPts_W (Last Week)
- upcomingDifficulty - metric indicating the difficulty of a player's schedule for the upcoming week

## Timeline
Week 1:
- Season Stats
- Week Stats

Week 2:
- Schedule Difficulty
- PPG Scored

### Libraries Used
- scikit-feature
    - Fisher Score
    - ReliefF
    - Trace Ratio
- boruta_py
- scikit-rebate

## Results
### Feature Engineering
Features identified to be an early indicator of power play goals:
- powerPlayTimeOnIce_W
- powerPlayGoals
- powerPlayTimeOnIce
- goals
- powerPlayPoints
- timeOnIce
- evenTimeOnIce
- timeOnIce_W
- evenTimeOnIce_W
- shots                     (BorutaPy)
- games                     (BorutaPy)
- goals_W                   (BorutaPy)
- pim_W                     (BorutaPy)
- assists_W                 (BorutaPy)
- games_W
- shifts_W


### Prediction Steps
Run on Sunday after last game of the week!
To predict:
1. Run `getData.py` to get player data
2. Run `getFeatures.py` to select features
3. Run `getPrediction.py` to predict
4. Run `getTruth.py` to get truth results
5. Run `results.py` to get benchmark results

result_baseline will contain the week X 'control' results (PPG scored last week) as well as being used as week X + 1 'truth' results.
result_prediction will contain the week X 'prediction' results.

### Validation
The validation of the predictions can be viewed by running `results.py`