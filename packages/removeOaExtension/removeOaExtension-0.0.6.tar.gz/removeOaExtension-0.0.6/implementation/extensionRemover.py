import copy


def remove_extensions(document_tree: dict, vendor_extension: list) -> dict:
    mutable_tree = copy.deepcopy(document_tree)

    # Iterate the current dictionary
    for key, value in document_tree.items():
        # Match the key/value with any vendor extension
        for extension in vendor_extension:
            if extension in value or extension in key:
                del mutable_tree[key]
                break
        if extension in value or extension in key:
            continue
        if isinstance(value, dict):
            mutable_tree[key] = remove_extensions(mutable_tree[key], vendor_extension)

    return mutable_tree
