cats_api_url = "https://api.thecatapi.com/v1/breeds"
cats_images_url = 'https://api.thecatapi.com/v1/images/search'
cats_api_key = 'f009d6b3-725e-40dd-9a20-5a0b518a0241'

db_file = 'cats.db'

sql_create_breeds_table = """ CREATE TABLE IF NOT EXISTS breeds (
                                    id text,
                                    breed_name text,
                                    temperament text,
                                    origin text,
                                    description text
                                ); """


log_folder = 'logs'
log_file = 'app.log'