import requests
from bs4 import BeautifulSoup as bs
import psycopg2

conn = psycopg2.connect(
	host = "localhost",
	database = "tarea1",
	user = "postgres",
	port = 5432,
	password = "")

cur = conn.cursor()

id_list = []
url_list = []

f = open('user-ct-test-collection-06.txt','r')

urls_desc = {}

lines = f.readlines()[1:]
for line in lines:
	x = line.strip('\n').split('\t')
	if x[4] != "":
		url_list.append(x[4])
		id_list.append(x[0])

cont = 0
for url in url_list:
	page = requests.get(url_list[cont])
	soup = bs(page.text, 'html.parser')
	head_items = soup.find_all('head')
	for head in head_items:

		if head.find('title') != None and soup.find('meta', attrs={"name" : "description"}) != None and soup.find('meta', attrs={"name" : "keywords"}) != None:

			titulo = str(head.find('title'))
			descripcion = str(soup.find('meta', attrs={"name" : "description"}))
			palabras_clave = str(soup.find('meta', attrs={"name" : "keywords"}))

			if url_list[cont] not in urls_desc:
				urls_desc[url_list[cont]] = (str(id_list[cont]), titulo.strip("\n"), descripcion, palabras_clave, str(url_list[cont]))

	cont += 1
try:
	cur.execute("create table DATOS(id char(30), titulo text(2000), descripcion text(4000), keywords text(3000), url char(255));")
	for value in urls_desc.values():
		insert = "insert into DATOS(id, titulo, descripcion, keywords, url) values ({}, {}, {}, {}, {});"
		insert2 = insert.format(value[0], value[1], value[2], value[3], value[4])
		cur.execute(insert2)
	conn.commit()
except:
	print("no puedo ejecutar eso")

cur.close()
conn.close()
f.close()