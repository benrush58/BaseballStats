from TeamClass import Team


def main():
    astros15 = Team('HOU', '2015')
    astros16 = Team('HOU', '2016')
    astros17 = Team('HOU', '2017')
    astros18 = Team('HOU', '2018')
    astros19 = Team('HOU', '2019')
    
    teams = [astros15, astros16, astros17, astros18, astros19]
    """
    reg_ba = astros15.reg_ba()
    post_ba = astros15.post_ba()
    reg_era = astros15.reg_era()
    post_era = astros15.post_era()
    reg_hra = astros15.reg_hra()
    post_hra = astros15.post_hra()
    """
    for team in teams:
        reg_ba = team.reg_ba()
        post_ba = team.post_ba()
        reg_era = team.reg_era()
        post_era = team.post_era()
        reg_hra = team.reg_hra()
        post_hra = team.post_hra()
        print(reg_ba)
        print(post_ba)
        print(reg_era)
        print(post_era)
        print(reg_hra)
        print(post_hra)


if __name__ == '__main__':
    main()


