def sql_bonus_withdrawal_list(bonus_tag, from_date, to_date):
    sql = "SELECT " \
          "a.Login, a.Equity, a.Credit, SUM(d.Profit) as Bonus " \
          "FROM mt5_deals d, mt5_accounts a " \
          "WHERE " \
          "d.Login = a.Login and " \
          "a.Login IN (SELECT d.Login FROM mt5_deals d " \
                      "WHERE d.Profit < 0 and d.Action = 2 and d.Time >= '"+from_date+"') and " \
          "d.Time >= '"+from_date+"' and d.Time <= '"+to_date+"' and " \
          "LOCATE('"+bonus_tag+"', d.Comment) > 0 and " \
          "a.Equity - a.Credit < 200  and a.Credit > 0 " \
          "GROUP BY d.Login HAVING SUM(d.Profit) > 0 "
    return sql
