from watchers.count_watcher import CountWatcher


def main():
    target_url = "https://www.petfinder.com/search/cats-for-adoption/ca/quebec/"
    "montreal/?age%5B0%5D=Baby&distance=10&gender%5B0%5D=female"
    initial_count = 5
    options = dict(
        list_element='pfdc-animal-search-results',
        list_attr='observe-state',
        list_attr_val='animalSearch.results',
        target_element='span',
        target_attr='data-test',
        target_attr_val='Pet_Card_Pet_Details_List')

    cw = CountWatcher(target_url, initial_count, options)
    cw.start()


if __name__ == "__main__":
    main()
