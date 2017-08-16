import pkg_resources


class Categories:
    """
    Load categories from YAML
    representation.
    """
    bio_data = {}
    password_mappings = {}
    individuals = {}
    category_plugin = "pata_password_cracker.plugins"
    encryption_plugin = "pata_password_cracker.encryption"
    substitutors_plugin = "pata_password_cracker.substitutors"
    loaded_cat_plugin_dict = {}
    loaded_encryption_plugin_dict = {}
    loaded_substitutors_plugin_dict = {}
    words = []

    def __init__(self, bio_data, words):
        """
        Store list of biographical data
        """
        self.bio_data = bio_data
        self.words = words
        self.loaded_cat_plugin_dict = self.load_plugins(self.category_plugin)
        self.loaded_encryption_plugin_dict = self.load_plugins(
            self.encryption_plugin)
        self.loaded_substitutors_plugin_dict = self.load_plugins(
            self.substitutors_plugin)

    def load_plugins(self, plugin):
        """
        Load the plugin and store object in array
        """
        plugin_dict = {}
        for p in pkg_resources.iter_entry_points(plugin):
            plugin_dict[p.name] = p.load()
        return plugin_dict

    def process_categories(self):
        """
        Process an individuals categories data
        to generate a list of potential
        passwords
        """
        individual = {}
        count = 0
        for target in self.bio_data:
            indv_key = str(count) + ":" + target
            indv_key = indv_key.replace(" ", "")
            individual[indv_key] = target
            target_vals = []
            count = count + 1

            for category in self.bio_data[target]:
                for k, v in category.iteritems():
                    for p in self.loaded_cat_plugin_dict:
                        if k == p:
                            target_vals.append(
                                {k: self.loaded_cat_plugin_dict[p]().process_data(
                                    k,
                                    self.words,
                                    v,
                                    self.loaded_encryption_plugin_dict,
                                    self.loaded_substitutors_plugin_dict)})
            individual[indv_key] = target_vals

        return individual
