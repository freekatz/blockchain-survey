proxies = {
    "https": "http://127.0.0.1:18889",
    "http": "http://127.0.0.1:18889"
}

out_data = {
    "year": "",
    "origin": "",
    "title": "",
    "topics": "",
    "publisher": "",
    "cites": "",
    "authors": "",
    "url": "",
    "abstract": "",
}

# static variable setting
nan_str = "nothing"
options = ["freq", "cite"]

input_root_dir = "./input"
output_root_dir = "./output"
crawler_output_dir = output_root_dir + "/crawler"
filter_output_dir = output_root_dir + "/filter"
preprocess_output_dir = output_root_dir + "/preprocess"
analyzer_output_dir = output_root_dir + "/analyzer"
plot_output_dir = output_root_dir + "/plot"

plot_chart_types = []
