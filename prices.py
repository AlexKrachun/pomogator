
fantik_to_usd = 0.01
usd_to_fantik = 1 / fantik_to_usd

prices_for_users_in_fantiks = {
    'gpt-4o-mini': 1,
    'claude-3-5-haiku-latest': 2,
    'gpt-4o': 5,
    'o3-mini': 3,
    'gpt-4o-search-preview': 5,

    'o1': 30,
    'gpt-4.5-preview': 100,
    'claude-3-7-sonnet-latest': 7,
    'dall-e-3': 50,
    # 'face-swap': face_swap_handler_first_photo,
}

price_of_1_token_in_usd = {
    'gpt-4o-mini': {'input': 0.15 * 1e-6,'output': 0.6 * 1e-6},
    'claude-3-5-haiku-latest': {'input': 0.8 * 1e-6,'output': 4 * 1e-6},

    'gpt-4o': {'input': 2.5 * 1e-6,'output': 10 * 1e-6},
    'o3-mini': {'input': 1.1 * 1e-6,'output': 4.4 * 1e-6},
    'gpt-4o-search-preview': {'input': 2.5 * 1e-6,'output': 10 * 1e-6},

    'o1': {'input': 15 * 1e-6,'output': 60 * 1e-6},
    'gpt-4.5-preview': {'input': 75 * 1e-6,'output': 150 * 1e-6},
    'claude-3-7-sonnet-latest': {'input': 3 * 1e-6,'output': 15 * 1e-6},

    'dall-e-3': {'1024x1024': 0.08, '1024x1792': 0.12, '1792x1024': 0.12},
    # 'face-swap': face_swap_handler_first_photo,
}



sub_plan_costs = {  # rub
    'month: 100/week': 160,
    'month: 300/week': 480,
    'month: 1000/week': 1600,
}



at_login_user_fantiks_amount = 100

