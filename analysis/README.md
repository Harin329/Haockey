# 2021-2022 NHL Season Analysis

## Problem Statement
I want to pick up players who are about to score many power play goals in the coming week.

## Phase Plans
### Phase 1 - Pre-Processing & Feature Engineering
Feature Engineering - Finding the tightest correlated metrics that indicate a player is about to score many power play goals with ensemble method.

Features Considered:
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
- upcomingDifficulty - metric indicating the difficulty of a player's schedule for the upcoming week
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

### Phase 2 - Prediction Presentation
Webapp/CLI - Displaying top player predictions for the upcoming week.

### Phase 3 - Result Validation
Webapp/CLI - Displaying historical results for predicted players, compared to a set of random players from the top 300.


## Results
### Feature Engineering
Features identified to be an early indicator of power play goals:
- powerPlayPoints_W
- powerPlayGoals
- powerPlayTimeOnIce
- goals
- powerPlayPoints
- timeOnIce
- evenTimeOnIce
- upcomingDifficulty
- powerPlayTimeOnIce_W

### Presentation
### Validation