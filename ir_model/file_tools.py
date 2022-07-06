from os import walk

class FileTools:
    def __init__(self, path: str):
        self.path = path

    def get_files(self, count = 1000000):
        files_arr = []
        for dirpath, _, filenames in walk(self.path):
            files_arr.extend(map(lambda filename: dirpath + "/" + filename, filenames))

        return files_arr[:count]

    def read_file(self, path):
        f = open(path, "rb")
        return str(f.read().decode("UTF-8", "ignore"))


class DocsCollection:
    def __init__(self, name: str):
        self.docs = []
        self.docs_by_label = {}

        ft = FileTools(f'./docs/{name}')
        files_array = ft.get_files()

        for file_path in files_array:
            label = self.get_label(file_path)
            content = ft.read_file(file_path)
            self.docs.append((content, label))
            try:
                self.docs_by_label[label].append(content)
            except:
                self.docs_by_label[label] = [content]


    def get_label(self, path):
        path_splitted = path.split("/")
        return path_splitted[-2]


    def __getitem__(self, key):
        return self.docs[key][0]
