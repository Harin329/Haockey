<p align="center">
  <a href="https://github.com/harin329/Haockey">
    <img src="./Haockey.png" alt="Logo" height="329" resize>
  </a>

  <h3 align="center">Haockey</h3>

  <p align="center">
    <strong>All things fantasy hockey!</strong>
  </p>
</p>

## Fantasy Pickup

1. Set .env file with app keys from yahoo
2. Run auth.py to create an auth.json file
3. Run main.py to do stuff

## Analysis

A data analysis of the 2021-2022 NHL season, predicting powerplay goals for upcoming weeks through ensemble feature selection. Emphasis on BorutaPy. See analysis/data/prediction.csv for weekly results. Project includes validation script for baseline comparison.

## Deployment

1. nohup python3 -u main.py &
2. logout
3. ps -e | grep python

## Deployment Logs
cat nohup.out
