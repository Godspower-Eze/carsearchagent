from __future__ import absolute_import, unicode_literals

from celery import shared_task

import requests
from bs4 import BeautifulSoup
import time
# from lxml import html
import datetime
import re
import websocket
import json
from django.core.mail import send_mail
from .models import SearchedValue

ws = websocket.WebSocket()

car_list = []
with open('car_list.txt', 'r') as f:
    for w in f:
        car_list.append(w.lower().strip())

pages_list = []
with open('pages.txt', 'r') as f:
    for w in f:
        pages_list.append('http://' + 'tori.fi/' + w.lower().strip())


def crawl(href):
    print(href)
    r = requests.get(href)
    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.findAll("a", class_="item_row_flex"):
        car_div = a.findAll("div", class_="li-title")
        if len(car_div) != 0:
            item = car_div[0].text.split()[0].lower()
            if item in car_list:

                div = a.findAll("div", class_="date_image")
                now = datetime.datetime.now()
                nowhr, nowmin = now.hour + 3, now.minute

                nowhr2, nowmin2 = now.hour, now.minute

                nowmin_ls = list(range(nowmin + 1))
                if len(nowmin_ls) >= 5:
                    nowmins = nowmin_ls[-5:]
                else:
                    nowmins = nowmin_ls

                nowmin_ls2 = list(range(nowmin2 + 1))
                if len(nowmin_ls2) >= 5:
                    nowmins2 = nowmin_ls2[-5:]
                else:
                    nowmins2 = nowmin_ls2

                # print(nowmins)

                today = "tänään"
                now = str(nowhr) + ":" + str(nowmin)
                day = div[0].text.split()[0]

                if day == today:
                    time = div[0].text.split()[1]
                    timehr, timemin = time.split(":")
                    timehr = int(timehr)
                    timemin = int(timemin)
                    if (timehr == nowhr and timemin in nowmins) or (timehr == nowhr2 and timemin in nowmins2):
                        # print('found')
                        car_features = a.findAll("p", class_="param")
                        car_img = a.findAll("img", class_="item_image")

                        res_collector = []
                        if len(car_img) != 0:
                            href_img = car_img[0].attrs.get("src")
                            res_collector.append(href_img)
                        else:
                            res_collector.append('no image')

                        href_item = a.attrs.get("href")
                        item_id = re.split('[_.]', href_item)[-2]

                        if len(car_div) != 0:
                            res_collector.append(car_div[0].text)
                        else:
                            res_collector.append('no feature1')
                        if len(car_features) != 0:
                            res_collector.append(car_features[0].text)
                        else:
                            res_collector.append('no feature2')
                        context = {'href_item': href_item, 'feature1': res_collector[1], 'feature2': res_collector[2],
                                   'img_url': res_collector[0]}
                        res_collector = []
                        return context


car_list = []
with open('/home/propertywithin/Desktop/computation/car_list.txt', 'r') as f:
    for w in f:
        car_list.append(w.lower().strip())

pages_list = []
with open('/home/propertywithin/Desktop/computation/pages.txt', 'r') as f:
    for w in f:
        pages_list.append('http://' + 'tori.fi/' + w.lower().strip())


def get_all_website_links(href, mileagerange, pricerange, searchlist, year_model):
    for i in range(len(searchlist)):
        if searchlist[i] == 'None':
            searchlist[i] = None
    search = 1
    r = requests.get(href)
    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.findAll("a", class_="item_row_flex"):
        car_div = a.findAll("div", class_="li-title")
        if len(car_div) != 0:
            item = car_div[0].text.split()[0].lower()
            if item in car_list:

                div = a.findAll("div", class_="date_image")
                now = datetime.datetime.now()
                print(now, 'first')
                nowhr, nowmin = now.hour + 3, now.minute
                print(nowhr, 'seconde')
                print(nowmin, 'thirde')
                # nowhr2, nowmin2 = now.hour, now.minute

                # nowmin_ls = list(range(nowmin + 1))
                # if len(nowmin_ls) >= 5:
                #     nowmins = nowmin_ls[-5:]
                # else:
                #     nowmins = nowmin_ls
                #
                # nowmin_ls2 = list(range(nowmin2 + 1))
                # if len(nowmin_ls2) >= 5:
                #     nowmins2 = nowmin_ls2[-5:]
                # else:
                #     nowmins2 = nowmin_ls2

                # print(nowmins)

                today = "tänään"
                now = str(nowhr) + ":" + str(nowmin)
                day = div[0].text.split()[0]

                if day == today:
                    time = div[0].text.split()[1]
                    timehr, timemin = time.split(":")
                    timehr = int(timehr)
                    timemin = int(timemin)
                    if timehr == nowhr and (timemin >= nowmin and nowmin < timemin + 5):  # or (timehr == nowhr2 and timemin in nowmins2):
                        context = {}
                        href_item = a.attrs.get("href")
                        if search == 1:
                            dic_of_carfeatures = {}
                            r = requests.get(href_item)
                            soup = BeautifulSoup(r.content, "html.parser")
                            linked = soup.find_all('div', class_='moottori_fi')
                            if len(linked) == 2:
                                cars = linked[0]
                                car = cars.find_all('a')
                                if len(car) == 2:
                                    speccar = car[1].text.split()
                                    cartype = speccar[1]
                                    carmodel = speccar[2]
                                    dic_of_carfeatures['cartype'] = cartype
                                    dic_of_carfeatures['carmodel'] = carmodel
                            else:
                                dic_of_carfeatures = {}
                            price = soup.find("span", {"itemprop": "price"})['content']
                            if len(price) != 0:
                                price = int(price)
                            else:
                                price = 0
                            table = soup.findAll("table", class_="tech_data")
                            if len(table) == 4:
                                topics = table[1].findAll("td", class_="topic")
                                values = table[1].findAll("td", class_="value")
                                for i in range(len(topics)):
                                    keyv = topics[i].text.strip().split(':')[0]
                                    vv = values[i].text
                                    dic_of_carfeatures[keyv] = vv
                                if dic_of_carfeatures['Ilmastointi'] == '✓':
                                    dic_of_carfeatures['Ilmastointi'] = 'Air conditioning'
                                if dic_of_carfeatures['Huoltokirja'] == '✓':
                                    dic_of_carfeatures['Huoltokirja'] = 'Service book'
                                if dic_of_carfeatures['Vakionopeudensäädin'] == '✓':
                                    dic_of_carfeatures['Vakionopeudensäädin'] = 'Cruise control'
                                if dic_of_carfeatures['Isofix-valmius'] == '✓':
                                    dic_of_carfeatures['Isofix-valmius'] = 'Isofix readiness'
                                if dic_of_carfeatures['Nahkasisustus'] == '✓':
                                    dic_of_carfeatures['Nahkasisustus'] = 'Leather upholstery'
                                if dic_of_carfeatures['Lohkolämmitin'] == '✓':
                                    dic_of_carfeatures['Lohkolämmitin'] = 'Motor heater'
                                if dic_of_carfeatures['Sisätilapistoke'] == '✓':
                                    dic_of_carfeatures['Sisätilapistoke'] = 'Internal plug'
                                if dic_of_carfeatures['Kahdet renkaat'] == '✓':
                                    dic_of_carfeatures['Kahdet renkaat'] = 'Two tires'
                                if dic_of_carfeatures['Vetokoukku'] == '✓':
                                    dic_of_carfeatures['Vetokoukku'] = 'Towbar'
                                if dic_of_carfeatures['Metalliväri'] == '✓':
                                    dic_of_carfeatures['Metalliväri'] = 'Metallic color'
                                if dic_of_carfeatures['Pysäköintitutka'] == '✓':
                                    dic_of_carfeatures['Pysäköintitutka'] = 'Parking sensors'
                                if dic_of_carfeatures['Xenon-ajovalot'] == '✓':
                                    dic_of_carfeatures['Xenon-ajovalot'] = 'Xenon headlights'
                                if dic_of_carfeatures['LED-ajovalot'] == '✓':
                                    dic_of_carfeatures['LED-ajovalot'] = 'LED headlights'
                                if dic_of_carfeatures['Webasto/Eber'] == '✓':
                                    dic_of_carfeatures['Webasto/Eber'] = 'Webasto/Eber'
                            else:
                                dic_of_carfeatures = {}
                            if len(table) != 0:
                                topics = table[0].findAll("td", class_="topic")
                                values = table[0].findAll("td", class_="value")
                                for i in range(len(topics)):
                                    keyv = topics[i].text.strip().lower().split(':')[0]
                                    vv = values[i].text.strip().lower()
                                    if keyv == 'mittarilukema':
                                        vv = re.sub('\D', '', vv)
                                    dic_of_carfeatures[keyv] = vv
                                    if dic_of_carfeatures.get('mittarilukema') != None and dic_of_carfeatures.get(
                                            'mittarilukema') != "":
                                        dic_of_carfeatures['mittarilukema'] = int(dic_of_carfeatures['mittarilukema'])
                                searchlistlen = len(searchlist)
                                foundlist = [item for item in searchlist if item in dic_of_carfeatures.values()]
                                foundlen = len(foundlist)
                                if searchlistlen - foundlen >= 1:
                                    if dic_of_carfeatures.get('vuosimalli') != None and dic_of_carfeatures.get(
                                            'vuosimalli') != '-':
                                        year = dic_of_carfeatures['vuosimalli']
                                        year = int(year)
                                        if year_model[0] != 'None' and year_model[1] != 'None':
                                            minn = year_model[0]
                                            maxx = year_model[1]
                                            minn = int(minn)
                                            maxx = int(maxx)
                                            if year >= minn and year <= maxx:
                                                context['href_item'] = href_item
                                        elif year_model[0] != 'None':
                                            minn = year_model[0]
                                            minn = int(minn)
                                            if year >= minn:
                                                context['href_item'] = href_item
                                        elif year_model[1] != 'None':
                                            maxx = year_model[1]
                                            maxx = int(maxx)
                                            if year <= maxx:
                                                context['href_item'] = href_item
                                        else:
                                            context['href_item'] = href_item
                                    if pricerange[0] != 'None' and pricerange[1] != 'None':
                                        minn = pricerange[0]
                                        maxx = pricerange[1]
                                        minn = int(minn)
                                        maxx = int(maxx)
                                        if price >= minn and price <= maxx:
                                            context['href_item'] = href_item
                                    elif pricerange[0] != 'None':
                                        minn = pricerange[0]
                                        minn = int(minn)
                                        if price >= minn:
                                            context['href_item'] = href_item
                                    elif pricerange[1] != 'None':
                                        maxx = pricerange[1]
                                        maxx = int(maxx)
                                        if price <= maxx:
                                            context['href_item'] = href_item
                                    else:
                                        context['href_item'] = href_item
                                    mileagemin = mileagerange[0]
                                    mileagemax = mileagerange[1]
                                    if dic_of_carfeatures.get('mittarilukema') != None and dic_of_carfeatures.get(
                                            'mittarilukema') != "":
                                        if mileagerange[0] != 'None' and mileagerange[1] != 'None':
                                            mileagemin = mileagerange[0]
                                            mileagemax = mileagerange[1]
                                            mileagemin = int(mileagemin)
                                            mileagemax = int(mileagemax)
                                            if dic_of_carfeatures['mittarilukema'] >= mileagemin and dic_of_carfeatures[
                                                'mittarilukema'] <= mileagemax:
                                                context['href_item'] = href_item
                                        elif mileagerange[0] != 'None':
                                            mileagemin = mileagerange[0]
                                            mileagemin = int(mileagemin)
                                            if dic_of_carfeatures['mittarilukema'] >= mileagemin:
                                                context['href_item'] = href_item
                                        elif mileagerange[1] != 'None':
                                            mileagemax = mileagerange[1]
                                            mileagemax = int(mileagemax)
                                            if dic_of_carfeatures['mittarilukema'] <= mileagemax:
                                                context['href_item'] = href_item
                                        else:
                                            context['href_item'] = href_item

                                    car_features = soup.findAll("p", class_="param")
                                    car_img = soup.findAll("img", class_="image_next")

                                    res_collector = []
                                    if len(car_img) != 0:
                                        href_img = car_img[0].attrs.get("src")
                                        res_collector.append(href_img)
                                    else:
                                        res_collector.append('no image')

                                    href_item = a.attrs.get("href")
                                    item_id = re.split('[_.]', href_item)[-2]

                                    if len(car_div) != 0:
                                        res_collector.append(car_div[0].text)
                                    else:
                                        res_collector.append('no feature1')
                                    if len(car_features) != 0:
                                        res_collector.append(car_features[0].text)
                                    else:
                                        res_collector.append('no feature2')
                                    context['href_item'] = href_item
                                    context['feature1'] = res_collector[1]
                                    context['feature2'] = res_collector[2]
                                    context['img_url'] = res_collector[0]
                                    res_collector = []
                                    return context
    # koeajoista


@shared_task
def data_sender():
    ws.connect("ws://127.0.0.1:8010/ws/home/")
    for href in pages_list:
        context = (crawl(href))
        ws.send(json.dumps({'value': context}))


@shared_task
def searched_value_sender(mileagerange, pricerange, searchlist, year_model):
    ws.connect("ws://127.0.0.1:8009/ws/search/")
    for href in pages_list:
        print('Working')
        context = (get_all_website_links(href, mileagerange, pricerange, searchlist, year_model))
        print(context)
        ws.send(json.dumps({'value': context}))


@shared_task
def searched_value_email_sender():
    searching_values = SearchedValue.objects.last()
    mileagerange = searching_values.mileagerange
    pricerange = searching_values.pricerange
    searchlist = searching_values.searchlist
    yearmodel = searching_values.yearmodel
    for href in pages_list:
        context = (get_all_website_links(href, mileagerange, pricerange, searchlist, yearmodel))
        print(context)
        if context is not None:
            print(context['feature1'])
            print(context['feature2'])
            print(context['href_item'])
            print(context['img_url'])
            send_mail("Advanced Search Car Update",
                      f"{context['feature1']} {context['feature2']} {context['href_item']} {context['img_url']}",
                      'caragent682@gmail.com',
                      ['ikechukwuka4paypal@gmail.com', 'Milliborn@yahoo.com', 'Clintonbychris@yahoo.com',
                       'godspowereze260@gmail.com'])


@shared_task
def email_sender():
    print('Working')
    for href in pages_list:
        context = (crawl(href))
        if context is not None:
            print(context['feature1'])
            print(context['feature2'])
            print(context['href_item'])
            print(context['img_url'])
            send_mail("Unfiltered Car Update",
                      f"{context['feature1']} {context['feature2']} {context['href_item']} {context['img_url']}",
                      'caragent682@gmail.com', ['ikechukwuka4paypal@gmail.com', 'Milliborn@yahoo.com'])
