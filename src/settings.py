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
    "cite": "",
    "authors": "",
    "url": "",
    "abstract": "",
}

# static variable setting
nan_str = "nothing"
options = ["freq", "cite"]

input_root_dir = "./input"
output_root_dir = "./output"
crawler_output_dir = output_root_dir + "/1-crawler"
preprocess_output_dir = output_root_dir + "/2-preprocess"
filter_output_auto_dir = output_root_dir + "/3-filter/auto"
filter_output_manual_dir = output_root_dir + "/3-filter/manual"
analyzer_output_dir = output_root_dir + "/4-analyzer"
plot_output_dir = output_root_dir + "/5-plot"

plot_chart_types = []

similar_replace_path = input_root_dir + "/similar.txt"
