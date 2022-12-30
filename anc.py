

    elif message.content.startswith('anc.wikia'):

        def generalise(string):
            name = ''
            for i in string.h1.text.split('\n'):   #It finds the h1 title name and makes it into a text itself
                if i != '':
                    for j in i.split('\t'):
                        if j != '':
                            name+=j + ' '
            return name


        ctx = message.content[10:]
        ctx = ctx.replace(" ", "+")

        animalswikia = f'https://ancient-animals.fandom.com/wiki/Special:Search?query={ctx}'
        dinowikia = f'https://dinopedia.fandom.com/wiki/Special:Search?query={ctx}'
        # print(animalswikia)

        Req = Request(animalswikia)
        uClient = urlopen(Req)
        soup = BeautifulSoup(uClient.read(), 'html5lib')

        Req = Request(dinowikia)
        uClient = urlopen(Req)
        soup2 = BeautifulSoup(uClient.read(), 'html5lib')

        length = 0   #To find the titles and the length of the list of all of these titles from each of the 2 websites
        if len(soup.find_all('li', {'class', 'unified-search__result'})) >= 5:
            length += 5
        else:
            length += len(soup.find_all('li', {'class', 'unified-search__result'}))

        length2 = 0
        if len(soup2.find_all('li', {'class', 'unified-search__result'})) >= 15:
            length += 15
            length2 += 15
        else:
            length += len(soup2.find_all('li', {'class', 'unified-search__result'}))
            length2 += len(soup2.find_all('li', {'class', 'unified-search__result'}))

        # print(length, length2)
        list = []
        for i in range(length - length2):
            #list.append(soup.find_all('a',{ "class", "result-link"})[int(2*i)]['href'])
            list.append(soup.find_all('li', {'class', 'unified-search__result'})[i].a['href'])
            alpha = generalise(soup.find_all('li', {'class', 'unified-search__result'})[i])
            await channel.send(f'```[{i}]. {alpha}```')                                #Titles with numbers now!!

        for i in range(length2):
            list.append(soup2.find_all('li', {'class', 'unified-search__result'})[i].a['href'])
            alpha = generalise(soup2.find_all('li', {'class', 'unified-search__result'})[i])
            await channel.send(f'```[{i+length - length2}]. {alpha}```')                                #Titles with numbers now!!



        await channel.send("``Please choose one of the provided links: 0, 1, 2 etc ...``")


        def check(m):
            return m.content == m.content and m.channel == message.channel
        morecontent = await client.wait_for('message',check = check, timeout = 40.0)
        ans = int(morecontent.content)
        eligible = []
        eligible2 = []
        for i in range(length - length2):
            eligible.append(i)
        for i in range(length - length2, length):
            eligible2.append(i)



        if ans in eligible:
            animalswikia = soup.find_all("li", {"class":"unified-search__result"})[ans].a['href']
            print(animalswikia)

            Req = Request(animalswikia)
            uClient = urlopen(Req)
            soup = BeautifulSoup(uClient.read(), 'html5lib')

            if len(soup.find_all('table', {'class':'wikia-infobox'})) != 0:
                Classification = []
                Ans = []
                Titles = []
                nt = 0
                no = 0
                nolist = []
                yet = 0
                for element in soup.find_all('table', {'class':'wikia-infobox'}):
                    for part in element.find_all('tr'):
                        if len(part.find_all('th')) != 0:
                            if len(part.find_all('td')) != 0:
                                if part.th.has_attr('class') == False:
                                    if part.td.has_attr('class') == False:
                                        if part.div == None:
                                            Classification.append(part.th.text)
                                            Ans.append(part.td.text)
                                            no += 1
                            elif part.th.has_attr('class'):
                                if part.th['class'] == ['wikia-infobox-header']:
                                    if yet != 0:
                                        Titles.append(part.text)
                                        nt+=1
                                        nolist.append(no)
                                        no = 0
                                        yet += 1
                                    else:
                                        Titles.append(part.text)
                                        nt+=1
                                        no = 0
                                        yet += 1
                nolist.append(no)

                #Recursive way to export out the table values
                add = 0
                n = 0
                for ii in nolist:
                    prev = add
                    add += ii
                    # print('NEWLISTODESU')
                    colours = [0xF2F7F2, 0x7FB285   , 0xEDEEC0, 0xBCAA99   , 0x00171F  , 0x3066BE , 0x60AFFF, 0x832161, 0x28C2FF, 0x2AF5FF]
                    emb = discord.Embed(title = f"{Titles[n]} wikia findings...", color = random.choice(colours))
                    for element in range(prev, add):
                        emb.add_field(name = f'{Classification[element]}', value = f'{Ans[element]}' )
                    emb.set_author(name = "Novum", icon_url = "https://cdn.discordapp.com/attachments/83566743976411136/650138167403479050/m8.png")
                    await channel.send(content = None, embed = emb)
                    n += 1



        elif ans in eligible2:
            def filtern(string):
                list = string.split('\n')
                for thing in list:
                    if thing == '':
                        list.remove(thing)

                for element in list:
                    list = element.split(' ')
                    for thing in list:
                        if thing == '':
                            list.remove(thing)
                return list

            def filtern2(string):
                list = string.split('\n')
                for thing in list:
                    if thing == '':
                        list.remove(thing)

                for element in list:
                    list = element.split(' ')
                    for thing in list:
                        if thing == '':
                            list.remove(thing)

                str = ''
                for i in list:
                    str += f'{i}' + ' '
                return str

            def green(ele):   #On 'tr' results
                return len(ele.find_all('th'))

            def greenno():    #I think this calculated the number of table elements
                no = 0
                for i in soup.find_all('tr'):
                    if green(i) != 0:
                        no+= 1

                return no

            def Tits():
                list = []
                begin = 0
                n = 0
                if len(soup.find_all('table',{'class':'infobox'})) >= 1:
                    for i in soup.find_all('tr'):
                        n+=1
                        if filtern2(i.text) == 'Scientific classification ':
                            list.append(f'Scientific classification ' + '/' + f'{n-1}')
                            begin += 1
                            break

                if begin!=0:
                    for i in range(n, len(soup.find_all('tr'))):
                        if len(list) <= greenno() -2:
                            if green(soup.find_all('tr')[i]) != 0:
                                str = filtern2(soup.find_all('tr')[i].text)
                                newstr = str + '/' + f'{i}'
                                list.append(newstr)
                                # print((soup.find_all('tr')[i].text))
                                # print(list)


                return list



            print(length2)
            print(length)
            print(ans)
            animalswikia = soup2.find_all("li", {"class":"unified-search__result"})[ans-length+length2].a['href']
            print(animalswikia)

            Req = Request(animalswikia)
            uClient = urlopen(Req)
            soup = BeautifulSoup(uClient.read(), 'html5lib')

###

            Class = []
            Ans = []
            for element in soup.find('table', {'class':'infobox'}).find_all('tr'):
                if len(element.find_all('td')) == 2:
                    Class.append(element.find_all('td')[0].text.split('\n')[0])
                    Ans.append(element.find_all('td')[1].text)

            colours = [0xF2F7F2, 0x7FB285   , 0xEDEEC0, 0xBCAA99   , 0x00171F  , 0x3066BE , 0x60AFFF, 0x832161, 0x28C2FF, 0x2AF5FF]
            emb = discord.Embed(title = f"{soup.find('h1').text} wikia findings...", color = random.choice(colours))
            emb.set_author(name = "Novum", icon_url = "https://cdn.discordapp.com/attachments/83566743976411136/650138167403479050/m8.png")
            for element in range(len(Class)):
                emb.add_field(name = f'{Class[element]}', value = f'{Ans[element]}' )


            imgcount = 0
            img = []
            row = 0
            for element in soup.find('table', {'class':'infobox'}).find_all('tr'):
                row += 1
                if len(element.find_all('a')) >= 0.1:
                    for thing in element.find_all('a'):
                        if thing.has_attr('title') == False:
                            imgcount += len(element.find_all('a'))
                            img.append(thing['href'])
                    if imgcount >= 1.1:
                        print(f'There are {imgcount} images in the table section for the {row}th row.')

            emb.set_thumbnail(url = f'{img[0]}')

            conditionforsynonym = 0
            for i in range(len(soup.find_all('tr'))):
                if filtern2(soup.find_all('tr')[i].text) == 'Synonyms ':
                    conditionforsynonym += i

            if conditionforsynonym != 0:
                if len(soup.find_all('tr')[conditionforsynonym+1].find_all('p')) >= 1:
                    left = []
                    right = []
                    for i in range(len(soup.find_all('tr')[conditionforsynonym+1].find_all('p'))):
                        left.append(soup.find_all('tr')[conditionforsynonym+1].find_all('p')[i].text)
                        try:
                            right.append(soup.find_all('tr')[conditionforsynonym+1].find_all('ul')[i].text)
                        except:
                            right.append('Nil')

                    for i in range(len(left)):
                        emb.add_field(name = f'{left[i]}', value = f'{right[i]}' )


            await channel.send(content = None, embed = emb)
