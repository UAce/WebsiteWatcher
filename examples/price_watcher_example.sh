# Example command for PriceWatcher
URL="https://www.google.com/travel/flights/booking?tfs=CBwQAhpJEgoyMDIzLTA5LTI0Ih8KA1lVTBIKMjAyMy0wOS0yNBoDQkNOKgJBQzIDODIyagwIAxIIL20vMDUycDdyDAgCEggvbS8wMWY2MhpJEgoyMDIzLTEwLTA4Ih8KA0JDThIKMjAyMy0xMC0wOBoDWVVMKgJBQzIDODIzagwIAhIIL20vMDFmNjJyDAgDEggvbS8wNTJwN0ABQAFIAXABggELCP___________wGYAQE&curr=CAD"
python websiteWatcher.py price --url $URL \
                               --description 'Air Canada flight ticket to Spain' \
                               --initial-price 2387 \
                               --threshold-price 2000 \
                               --notify-on-change \
                               --full-xpath /html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/span