# Local path and directory to your Q2 logs
directory = "./files/masked"

# Get this from 1Password, search 'Q2 Log Parser - FI Name,KID list'
fi_name_kid = [
    ("Sunrise Valley Credit Union", "qkypaaJ7Ci7UdMk3zNocO8uJumXdFKZJOsUvZywZxBY"),
    ("Horizon Federal Bank", "l7BqRYYsJc69VurvUzKoGY95Y1D2Zj75WpH6xmDbxZA"),
    ("Summit Community Bank", "ILY7ONi5SmTaECFCxqIFPIG7hTIKaUA4UoY9H8WfqNw"),
    ("Pinecrest Federal Credit Union", "2Tx6PgxWhcxQH1uyYMl8XFYGliG-vAzu1rrwuElkUuA"),
    ("Riverside National Bank", "QB17CpvCwYZbJ1QbG_9Fc3vqaP6gCioIn4QCJMp0N1M"),
    ("Golden Gate Credit Union", "VvBy2k5ElE61HAYnAX-FHx1QLsrjxmm5mvzLt5lpCZs"),
    ("Silver Lake Bank & Trust", "OjBeyWkxw6mf7yXfsbqJUsk1sWBMWnEvvKXk703FxBA"),
    ("Crystal Coast Federal", "UUyoxpb1EPXw1O_ujGDS9RblokTvktAA-GgMn75xutE"),
    ("Mountain View Community Bank", "P-Iisag2XWnXUw-07NGcBw1aJ6gFF87rrP_rwGQw6aM"),
    ("Sunset Valley Federal", "Kzz1zIr366g-IZq7AeOM69-MOAgoLpH9pDw_tXoNkd8"),
    ("Ocean Breeze Credit Union", "o7TsvVlxJjD2hoX9OokCBzT8oB98LzUIa5AX2zrN74g"),
    ("Desert Star Bank", "SnehyGv17x92doJLH3vNQ5zKHt-ZbRQhsx82kgh_hBI"),
    ("Forest Hills Federal", "PFdXTvo2A-vu0PSWaSFpfjnjL-wixvMFxYuP510LKrk"),
    ("Prairie Wind Credit Union", "eYQD4MiyWD5Jb6XgqMmULC74dazx7VJHkM4DN6KRGDY"),
    ("Northern Lights Bank", "xMs2IgH75FHR2nMJCYobQuylx7mzRqu0goTyFzYT7Rg"),
    ("Valley Stream Federal", "qi4pN4F20qXWu9u85I_7jNmKTrkeHk2A2bIqGUcJ59Q"),
    ("Lakeside Community Bank", "P2X9uqcmQ9aoWyXISOjGrHzbt4BX6scnN9euWcoKyu8"),
    ("Cedar Ridge Credit Union", "8zzf0aD8kUG2CV0CPQPTN6HAgFDuEarvKi7TkGBgelQ"),
    ("Bayview Federal Bank", "JDKZsQ8csFPo1RgMcGThGom4rVy1484vyMeVt4AMPko"),
    ("Meadowbrook Bank & Trust", "JUWf0Z84Z4hlSs93l_e1WbMyjQfn-Z9e40LEKXO4e4I"),
    ("Aspen Grove Credit Union", "2gaLy1Svon4Wag6CJNjR93Pm-J1osavNgXKZ5X0WGfc"),
    ("Coastal Community Bank", "mM-80HZOe6lfGSmb3H5Aa91Bk0Frapnstsf96AL00Mw"),
    ("Pine Valley Federal", "_3twJHHfMC703uu6ci-udfujFWdyxFsFrhGsLvZ3IYk"),
    ("Sunrise Federal Bank", "bIIUSIVv4o7vUY3OaS2SE51TXAlM1a6JIXKgXZH1t5o"),
    ("Maple Leaf Credit Union", "t1p9eyMbRVth5JROPTD9VKfvR9uZf-9tUhX88mE13wE"),
    ("Riverbend Community Bank", "RSPE8wmZUrFe7bcHv4sIGJyOBbtEUjOa06I4vwKqrzk"),
    ("Highland Federal Credit Union", "C9xzco2kNR5NnUbbjNBkDd0rJEfDp6GEULpjEhz4gKk"),
    ("Willow Creek Bank & Trust", "7K9BBOWkwEZ5N7PXES6EFcPl5citigKQB7n5MvV78Zg"),
    ("Blue Ridge Federal", "CeLWguA1tuIyjRG-x-gBo-0c6MZ52rqBgVnvu9rOGb8"),
    ("Evergreen Community Bank", "LhnVRQzS4A1oXQtha3EzYMdMAJ_W4Zdm4HnS-twzu3c"),
    ("Cascade Federal Credit Union", "N1Oj7SnMyRfM_44ll2aOCapQ1yCP363VQg5SxYPxCXY"),
    ("Sierra Vista Bank", "o2EeiABdIUs-dDMTdOEP2d8o_p6knvV64fPXS11msr4"),
    ("Rocky Mountain Federal", "Zf8PZ_igH7VC-SQPtDnIKLJqFTPdQxAdkbnpfWuqi_M")
]

# FI Dict, includes key_ids, name, res_times and user_errors
def get_fi_dict():
    fi_dict = {}
    for fi_name, kid in fi_name_kid:
        # print(fi_name, kid)
        fi_dict[kid] = {
            "name": fi_name,
            "res_times": [],
            "user_errors": [],
        }
    return fi_dict
