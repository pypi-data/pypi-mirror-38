from tokenizer_tools.conll.iterator_reader import iterator_reader


def tag_collector(input_files, tag_index=1):
    all_tag_set = set()
    for sentence in iterator_reader(input_files):
        tag_set = {i[tag_index] for i in sentence}

        all_tag_set.update(tag_set)

    return all_tag_set
