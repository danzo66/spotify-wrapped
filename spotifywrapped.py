import numpy as np
from operator import itemgetter

"""
only thing you might want to change in this is at the bottom:

squadwrapped1 = sorter(squadwrapped1, ax="position") 

ax takes either "position" or "frequency"

and it just orders the output array based on either the average position 
or frequency of appearing in the various wrappeds


"""
   
def conc():
    """concatenates all the saved arroys into one big array"""
    
    peeps = ['Dan 19', 'Dan 20', 'Dan 21', 'Cosmic Dance', 'Desert Island']
    
    for i, peep in enumerate(peeps):
        arr = np.load(str(peep) + '.npy', allow_pickle=True)
        arr = [arr]
        if i == 0:
            allwrapped = arr
        else:
            allwrapped = np.concatenate((allwrapped, arr))    

    return allwrapped

allwrapped = conc()



def stats(array, allwrapped, people):
    #frequency
    frequ = [["FREQUENCY"]]
    for i in array[1:]:
        f = len(i[people])
        frequ.append([f])
    
    frequ = np.array(frequ)
    array = np.concatenate((array, frequ), axis=1)
    
    #for artist wrapped
    if people == 2:
        #average position for wrapped
        avgpos = [["AVERAGE POSITION"]]
        for i in array[1:]:
            wee = i[people]
            avg = sum(wee.values())/len(i[people])
            avg = round(avg,2)
            avgpos.append([avg])
        
        avgpos = np.array(avgpos)
        array = np.concatenate((array, avgpos), axis=1)
        
        #weighted average position
        wavgpos = [["WEIGHTED AVERAGE"]]
        for i in array[1:]:
            totpeeps = len(allwrapped)
            frequ = float(i[people+1])
            summ = sum(i[people].values()) + (totpeeps - frequ)*101
            wavg = summ/(frequ)
            wavg = wavg/10
            wavg = round(wavg,2)
            wavgpos.append([wavg])
        
        wavgpos = np.array(wavgpos)
        array = np.concatenate((array, wavgpos), axis=1)
    
    #for artist frequency
    elif people == 1:
        #average songs for top artist
        avgpos = [["AVERAGE SONGS"]]
        for i in array[1:]:
            w = i[people]
            avg = sum(w.values())/len(i[people])
            avg = round(avg,2)
            avgpos.append([avg])
        
        avgpos = np.array(avgpos)
        array = np.concatenate((array, avgpos), axis=1)
    
        #weighted avg no. of songs
        wavgpos = [["POINTS"]]
        for i in array[1:]:
            totpeeps = len(allwrapped)
            frequ = float(i[people+1])
            summ = sum(i[people].values())
            b = summ*(frequ**2)
            wavg = b/(totpeeps)
            wavg = round(wavg,2)
            wavgpos.append([wavg])
        
        wavgpos = np.array(wavgpos)
        array = np.concatenate((array, wavgpos), axis=1)


    
    return array


def sorter(wrapped, ax):
    if len(wrapped[0]) == 6:
        sort = np.array([["ARTIST", "SONG", "PEOPLE", "FREQUENCY", "AVERAGE POSITION", "WEIGHTED AVERAGE"]])
    else:        
        sort = np.array([["ARTIST", "PEOPLE", "FREQUENCY", "AVERAGE SONGS", "POINTS"]])


    for i, row in enumerate(wrapped[1:]):
        value = row[ax]
        sf0 = value[:value.find('.')]
        if len(sf0) == 3:
            continue
        elif len(sf0) == 2:
            wrapped[i+1][ax] = "0" + str(wrapped[i+1][ax])
        elif len(sf0) == 1:
            wrapped[i+1][ax] = "00" + str(wrapped[i+1][ax])    
        
    wrapped = sorted(wrapped[1:], key=itemgetter(ax))
    for i in wrapped:
        np.transpose(i)
        sort = np.concatenate((sort,[i]))
        
    return sort




def process(allwrapped):
    
    avgpos = np.array([["SONG", "POSITION"]])
    
    #gets all matching songs into one big array
    squadwrapped0 = np.array([["SONG", "PEOPLE"]])
    for i, person in enumerate(allwrapped):
        others = np.concatenate((allwrapped[0:i], allwrapped[i+1:-1]))
        for j, songp in enumerate(person):
            for row in others:
                for k, songo in enumerate(row):
                    if songo == songp:
                        if str(songo) != "None":
                            song = np.array([[str(songp), list([person[0],row[0]])]], dtype = object)
                            squadwrapped0 = np.concatenate((squadwrapped0, song))
                            avg = ((j+1)+(k+1))/2
                            pos = np.array([[person[0], j], [row[0],k]])
                            avgpos0 = np.array([[songp, pos]], dtype=object)
                            avgpos = np.concatenate((avgpos, avgpos0))
                            
    avgpos = np.array([avgpos[:,1]])
    avgpos = np.transpose(avgpos)
    squadwrapped0 = np.concatenate((squadwrapped0, avgpos),axis=1)
        
    
    #gets rid of duplicates
    squadwrapped1 = np.array([["SONG", "PEOPLE", "POSITION"]])
    for i, song1 in enumerate(squadwrapped0):
        if np.any(squadwrapped1[:,0] == song1[0]):
            continue
        else:
            ifdupe = np.any(squadwrapped0[(i+1):,0] == song1[0])
            if ifdupe == True:
                people = song1[1]
                for song2 in squadwrapped0:
                    if song1[0] == song2[0]:
                        people = people + song2[1]
                song = np.array([[song1[0], people, song1[2]]], dtype = object)
                squadwrapped1 = np.concatenate((squadwrapped1, song))
            else:
                song1 = np.array([song1])
                squadwrapped1 = np.concatenate((squadwrapped1, song1), axis=0)
                
                
    #gets rid of duplicates in people
    
    peoplearray = squadwrapped1[1:,1]
    freq = np.array([["FREQ"]])
    for i, peoplerow in enumerate(peoplearray):
        people = []
        for j, person in enumerate(peoplerow):
            person = (str(person))
            peoplerow = np.array(peoplerow)
            ifdupe = np.any(peoplerow[(j+1):] == person)
    
            if ifdupe == True:
                continue
            else:
                people.append(person)
        squadwrapped1[i+1,1] = people
        freqrow = np.array([[len(people)]])
        freq = np.concatenate((freq,freqrow))
        
    squadwrapped1 = np.concatenate((squadwrapped1, np.array(freq)), axis=1)
    
    #takes the average position
    for i, positions in enumerate(squadwrapped1[1:,2]):
        for j, pos in enumerate(positions[:,1]):
            positions[j,1]=float(pos)
            
        avg = np.mean(positions[:,1].astype(float))
        squadwrapped1[1:,2][i]=avg
        
    wavg = ["WEIGHTED AVERAGE"]
    for i, row in enumerate(squadwrapped1):
        if i > 0:
            totpeeps = len(allwrapped)
            frequ = float(row[3])
            mean = float(row[2]) + (totpeeps - frequ)*101
            wavg0 = mean*(totpeeps)**(-1)
            wavg0 = round(wavg0, 2)
            wavg.append(wavg0)
    wavg = np.array([wavg])
    wavg = np.transpose(wavg)
    squadwrapped1 = np.concatenate((squadwrapped1, wavg), axis=1)
    
    squadwrapped = sorter(squadwrapped1, 4)

                    
    return squadwrapped
       
squadwrapped = process(allwrapped)         



def favartist(allwrapped, indv):
    artists = []
    artistsf = []
    freq = {} 
    songart = []
    
    '''artist frequencies'''
    
    if indv == False:
        #finding artists
        for i, row in enumerate(allwrapped):
            for j, song in enumerate(row):
                if str(song) != "None":
                    song = str(song)
                    artist = song[song.find(' - song by ') + 11 :]
                    song = song[:song.find(' - song by ')]
                    feat = artist.split(", ")
                    for art in feat: 
                        if str(art) != '':
                            art = [row[0],art]
                            artists.append(art)
                            sa = [song, art[1], {str(row[0]):j}]
                            songart.append(sa)
                            
        #adds artists and listeners       
        for person in artists:
            listener = str(person[0])
            singer = person[1]
            if singer in artistsf:
                if listener in freq[singer].keys():
                    freq[singer][listener] = int(freq[singer][listener])+1
                else:
                    freq[singer].update({listener:1})
            else:
                f = {singer : {listener:1}}
                artistsf.append(person[1])
                freq.update(f) 
              
    # does the exact same thing except without listeners cos for one person                            
    elif indv == True:
        for song in allwrapped:
            if str(song) != "None":
                song = str(song)
                artist = song[song.find(' - song by ') + 11 :]
                feat = artist.split(", ")
                for art in feat: 
                    if str(art) != '':
                        artists.append(art)

        for singer in artists:
            if singer in artistsf:
                freq[singer] = int(freq[singer])+1

            else:
                f = {singer : 1}
                artistsf.append(singer)
                freq.update(f) 

    #deletes all bad values or those less than one    
    for i in freq.copy():
        if i == '':
            freq.pop(i)
        elif i == " - 2021 Wrapped | Podcast ":
            freq.pop(i)
        elif len(freq[i]) == 1:
            freq.pop(i)
    
    #turns dict into array
    freqk = list(freq.keys())
    freqp = list(freq.values())
    
    freq = np.concatenate(([freqk], [freqp]), axis = 0)
    freq = np.transpose(freq)
    
    '''creates artist wrapped'''
    
    #gets songs    
    artistwrapped = []
    for artist in freq:
        for i, song in enumerate(songart):
            if song[1] == artist[0]:
                artistwrapped.append([artist[0],song[0], song[2]])
    
    #adds everyones top 5 song as well
    for row in allwrapped:
        for i, music in enumerate(row):
            if i < 6:
                song = music[:music.find(' - song by ')]
                if song in artistwrapped[1]:
                    break
                else:
                    for j in songart:
                        if song == j[0]:
                            p = [j[1],j[0], j[2]]
                            artistwrapped.append(p)
            
    #deletes dupes
    for i, song in enumerate(artistwrapped):
        pos = {}
        pos.update(song[2])
        copies = artistwrapped[(i+1):]
        for j, songcopy in enumerate(copies):
            if song[1] == songcopy[1]:
                index = j + i + 1
                if index == len(artistwrapped):
                    break
                else:
                    pos.update(songcopy[2])
                    artistwrapped.pop(index)
        song[2] = pos


    songs = [["ARTIST", "SONG", "PEOPLE"]]
    for i in artistwrapped:
        song = np.array([[i[0],i[1],i[2]]])
        songs = np.concatenate((songs, song), axis=0)      
    
    artistwrapped = songs
    
    artistwrapped = stats(artistwrapped, allwrapped, people=2)
    artistwrapped = sorter(artistwrapped, 5)
    
    tit = [["ARTIST", "PEOPLE"]]
    freq= np.concatenate((tit, freq))
    freq = stats(freq, allwrapped, people=1)
    freq = sorter(freq, 4)
    freq = np.flip(freq[1:], axis=0)
    tit = [["SONG", "PEOPLE","FREQUENCY", "AVERAGE SONGS", "POINTS"]]
    freq = np.concatenate((tit, freq,), axis=0)
        
    return freq, artistwrapped

artistfreq = favartist(allwrapped, False)[0]
artistwrapped = favartist(allwrapped, False)[1]




