
def recommendation(user_input, df_team, df_items):
    base_item_lst = df_items.loc[df_items['item_type'] == "base", 'item_name'].tolist()

    def tier_rank(tier):
        mapping = {"S": 0, "A": 1, "B": 2}
        return mapping[tier]

    df_team["tier_rank"] = df_team.apply(lambda row: tier_rank(row["team_tier"]), axis=1)

    def n_need(tid, item):
        return df_team.at[tid, item]

    def n_have(item, user_item_lst):
        return user_item_lst.count(item)

    def hit(tid, item, user_item_lst):
        need = n_need(tid, item)
        have = n_have(item, user_item_lst)
        return min(need, have)

    def miss_item(tid, item, user_item_lst):
        n_need = df_team.at[tid, item]
        n_have = user_item_lst.count(item)
        return max(0, n_need - n_have)

    def hit_rate(tid, user_item_lst):
        total = 0
        for item in base_item_lst:
            total += hit(tid, item, user_item_lst)
        return total / 12

    def miss_items(tid, user_item_lst):
        missing_items = {}
        for item in base_item_lst:
            if miss_item(tid, item, user_item_lst) != 0:
                missing_items[item] = miss_item(tid, item, user_item_lst)
        return missing_items

    def ratio(tid, item, user_item_lst):
        return f'{n_have(item, user_item_lst)}/{n_need(tid, item)}'

    # perform logic on user input

    df_team["hit_rate"] = df_team.apply(lambda row: hit_rate(row["team_id"], user_input), axis=1)
    df_team["miss_items"] = df_team.apply(lambda row: miss_items(row["team_id"], user_input), axis=1)

    item_short_lst = []

    for item in base_item_lst:
        item_s = ''.join([c for c in item if c.isupper()])
        item_short_lst.append(item_s)
        df_team[item_s] = df_team.apply(lambda row: ratio(row["team_id"], item, user_input), axis=1)

    df_team_sorted = df_team.sort_values(['hit_rate', 'tier_rank', 'team_id'], ascending=[False, True, True])

    columns_to_select = ['team_id', 'team_name', 'team_tier', 'team_ramp'] + item_short_lst

    df_clean = df_team_sorted.loc[:, columns_to_select]

    return df_clean
