import pandas as pd 
import requests
import re


def main(df: pd.DataFrame, i: int):
	urls = df['url']
	for u in urls[i:]:
		print(i, ': ', u)
		url = u.replace('abs', 'pdf')
		content = requests.get(url).content

		with open('./arxiv%s.pdf' % re.search(r'pdf/(.*)', url).groups()[0], 'wb') as f:
			f.write(content)

		f.close()

		i += 1



if __name__ == '__main__':
	df = pd.read_excel('./arxiv.xlsx')
	i = 51
	main(df, i)
