import sys, re;
import time
import urllib.request
import urllib.parse

crh_rus = open(sys.argv[1]);

def temizle(s, i, o): #{
	cikis = '';
	durum = 0;	

	for c in s: #{
		if c == i: durum = 1; 
		if c == o: durum = 0;
		if c == i or c == o: continue

		if durum == 0:  #{
			cikis = cikis + c;
		#}
	#}
	return cikis;
#}

def szlk_demek(s): #{
	# wget -q -O - "http://demek.ru/soz/?q=машина"
	url = 'http://demek.ru/soz/?q=' + urllib.parse.quote(s);
	sablon = re.compile('<div class="item_bsc">[^<]+</div>');
	sayfa = urllib.request.urlopen(url).read();
	katilma = sablon.findall(sayfa.decode());
	for i in range(0, len(katilma)): #{
		katilma[i] = temizle(katilma[i], '<', '>');
	#}
	return katilma
#}

def skor(c, t): #{
	s = -1.0;

	cc = set([i for i in c])
	tt = set([i for i in t])

	# Ideas: bump score for unambiguous
	#        

	s = len(cc.intersection(tt))/((len(cc)+len(tt))/2.0)

	return s;
#}

kelime = '';
ilk = True;
sozluk = {};

cyrl = re.compile('[а-яёА-ЯЁ]+[а-яёА-ЯЁ\- ]+[а-яёА-ЯЁ]+');
latn = re.compile('[öçğşüıâña-zA-ZÖÇĞŞÜIÂÑ]+[öçğşüâñıa-zA-ZÖÇĞŞÜIÂÑ\- ]+[öçğşâñüıa-zA-ZÖÇĞŞÜIÂÑ]+');

for cizgi in crh_rus.readlines(): #{
	if cizgi.strip() == '': #{
		continue;
	#}
	
	if ilk == True: #{
		kelime = cizgi.strip();
		sozluk[kelime] = [];
		ilk = False;
		continue;
	#}	

	if cizgi[0] == '\t': #{
		xcizgi = temizle(cizgi.strip(), '[', ']');
		k = latn.findall(xcizgi);
		if k == []: k = [kelime];
		sozluk[kelime].append({'crh': k, 'rus': cyrl.findall(xcizgi)});
	else: #{
		kelime = cizgi.strip();
		sozluk[kelime] = [];
	#}
#}

katilma_o = list(sozluk.keys())
katilma_o.sort();

for katilma in katilma_o: #{
	for kelime in sozluk[katilma]: #{
		if kelime['rus'] == [] or kelime['rus'] == []: #{
			continue;
		#}
		for o in kelime['rus']: #{
			ox = szlk_demek(o);
			for oxo in ox: #{
				sk = skor(katilma, oxo);
				print(sk,'\t',katilma,'\t',kelime['crh'],'\t',o,'\t',oxo);
			#}
		#}
	#}
#}
