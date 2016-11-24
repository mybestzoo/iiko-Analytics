#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

def revenue(df,period):
    #input: df - dataframe
    #       period - resampling period : 'H' hours, D' days, 'W' weeks, 'M' months, 'Q' quarters
    #output: ts - timeseries of revenue for a period
    #        revenue_current - revenue in the last period
    #        revenue_previous - revenue in the previous period
    ts = pd.Series(df['Sum_after_discount'].values, index = df['Date_Time'])
    # resample to period
    ts = ts.resample(period).sum()
    # delete last unfilled period 
    ts = ts[:-1]
    current = ts[-1]
    previous = ts[-2]
    gain = round((current/previous -1)*100)
    return ts, current, previous, gain

def units(df,period):
    #input: df - dataframe
    #       period - resampling period : 'H' hours, D' days, 'W' weeks, 'M' months, 'Q' quarters
    #output: ts - timeseries of units sold for a preiod
    ts = pd.Series(df['Units'].values, index = df['Date_Time'])
    # resample to period
    ts = ts.resample(period).sum()
    # delete last unfilled period 
    ts = ts[:-1]
    current = ts[-1]
    previous = ts[-2]
    gain = round((current/previous -1)*100)
    return ts, current, previous, gain

def groups_by_revenue(df):
    last_date = df['Date_Time'].iloc[-1]
    last_month = last_date.month
    last_year = last_date.year
    
    # decompose data into current month and previous month
    month_cur = df[(df['Month'] == (last_month-1)) & (df['Year'] == last_year) ]
    month_prev = df[(df['Month'] == (last_month-2)) & (df['Year'] == last_year) ]

    # calculate revenues
    rev_cur = month_cur['Sum_after_discount'].sum()
    rev_prev = month_prev['Sum_after_discount'].sum()

    # calculate revenues by product_groups
    grouping_cur = month_cur.groupby(['Product_group'])
    grouping_cur = grouping_cur['Sum_after_discount'].sum()
    grouping_cur_pct = grouping_cur/rev_cur*100
    grouping_prev = month_prev.groupby(['Product_group'])
    grouping_prev = grouping_prev['Sum_after_discount'].sum()
    grouping_prev_pct = grouping_prev/rev_prev*100

    # sort product groups by percentage of revenues
    ABC = grouping_cur_pct.sort_values(ascending=False)
    
    return ABC

def groups_by_units(df):
    last_date = df['Date_Time'].iloc[-1]
    last_month = last_date.month
    last_year = last_date.year
    
    # decompose data into current month and previous month
    month_cur = df[(df['Month'] == (last_month-1)) & (df['Year'] == last_year) ]
    month_prev = df[(df['Month'] == (last_month-2)) & (df['Year'] == last_year) ]

    # calculate revenues
    rev_cur = month_cur['Units'].sum()
    rev_prev = month_prev['Units'].sum()

    # calculate revenues by product_groups
    grouping_cur = month_cur.groupby(['Product_group'])
    grouping_cur = grouping_cur['Units'].sum()
    grouping_cur_pct = grouping_cur/rev_cur*100
    grouping_prev = month_prev.groupby(['Product_group'])
    grouping_prev = grouping_prev['Units'].sum()
    grouping_prev_pct = grouping_prev/rev_prev*100

    # sort product groups by percentage of revenues
    ABC = grouping_cur_pct.sort_values(ascending=False)
    
    return ABC
