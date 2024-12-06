

db = {
    "users": [
        {
            "username": "asdf",
            "hashed_password": "$2b$12$ufx8/VOpoxahaLDosWi8dedGgW/7fjEwM9dTnE.fJdOpiRc/Uzd8K"
        },
        {
            "username": "asdf",
            "hashed_password": "$2b$12$11aPN1RrgUxlaJ3KGnrbDuU8Rn0Qgl1Qrr1z4iE0orEBxlq/sZYAm"
        },
        {
            "username": "string",
            "hashed_password": "$2b$12$DUBQAvo3JMzq0CMAGX9BDOnzQeQQS4Avj95plJbwvWuuBFEQ77xL."
        },
        {
            "username": "asdf",
            "hashed_password": "$2b$12$TaB9SDfrflO6A9DU7FCADuWpSVndpCJu.1WbjQI9ALxv3Al4S9Z8q"
        },
        {
            "username": "string",
            "hashed_password": "$2b$12$mAwgvtyDTu/fUqF.BdIdzOtEtqyf7alQmAvGyUJpBesAS2hE0JYKS"
        },
        {
            "username": "string",
            "hashed_password": "$2b$12$EfhbKVBhXXFYws62AT1c2u7ST/YsUIdhRqtlW6Vo2bFfgeI67hVYq"
        },
        {
            "username": "string",
            "hashed_password": "$2b$12$XqyLvNg4WmqboucabWFrIuCVjgJhFIc4AxqwDJJGgungbcnqzWdwS"
        },
        {
            "username": "string",
            "hashed_password": "$2b$12$zvMjH0ijg/..VLM04Hz/eui8PzJ9u7.E4ckRm4EO8aWYwnKuaewF2"
        },
        {
            "username": "string",
            "hashed_password": "$2b$12$/Slge2da6MA7QkG7liOxlO.w9Pvi1ed0IUB9rUbLxiOBVhFkyOOxm"
        },
        {
            "username": "string",
            "hashed_password": "$2b$12$5IRmJF8h0e3cz4kopDF.juda4WEbdCSZgNQI67N7UXB4R.LaJnj6."
        },
        {
            "username": "string",
            "hashed_password": "$2b$12$M6sRIJ9C8z/zh5p4bP1jK.TV5cReQO3bOGwjoVVh0IyOPi18fIjoq"
        }
    ]
}



user = filter(lambda u: u['username'] == 'adf', db['users'])
print(user)
print(list(user))
