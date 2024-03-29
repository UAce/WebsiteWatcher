# Example command for ListWatcher
URL="https://www.petfinder.com/search/cats-for-adoption/ca/quebec/montreal/?age%5B0%5D=Baby&distance=10&gender%5B0%5D=female"
python3 websiteWatcher.py list --url $URL \
                               --list-tag pfdc-animal-search-results \
                               --list-attribute observe-state \
                               --list-attribute-value animalSearch.results \
                               --target-tag span \
                               --target-attribute data-test \
                               --target-attribute-value Pet_Card_Pet_Details_List