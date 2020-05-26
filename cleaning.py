import re

SPECIAL_RULES = {
    'Al-Battani': [
        ['Tetrabiblos.\n<a href=http://www.britannica.com/biography/al-Battani>','</Q>'],
        ['<a href=http://www.britannica.com/biography/al-Battani>','']
    ],
    'Ambartsumian': [
        ['Stages of life and scientific concepts</i> (Russian) (Moscow, 2011).','<i>Stages of life and scientific concepts</i> (Russian) (Moscow, 2011).']
    ],
    'Brahe': [
        ['A picture of his birthplace</a>','A picture of his birthplace']
    ],
    'Brouncker': [
        ['<img src = "../Diagrams/Picontfrac.gif">','<d Picontfrac.gif>']
    ],
    'Catalan': [
        ['<bEug&egrave;ne >Catalan</b>','<b>Eugène Catalan</b>']
    ],
    'Cafiero': [
        ['<Funzioni','Funzioni']
    ],
    'Colson': [
        ['3709286573961472<pre>','3709286573961472</pre>'],
        ['2308726432039468<pre>','2308726432039468</pre>']
    ],
    'Copernicus': [
        ['<r><li 1></r>','<li 1>'],
        ['<r><li 2></r>','<li 2>'],
        ['<r><li 3></r>','<li 3>'],
        ['<r><li 4></r>','<li 4>'],
        ['<r><li 5></r>','<li 5>'],
        ['<r><li 6></r>','<li 6>'],
        ['<r><li 7></r>','<li 7>']
    ],
    'Copson': [
        ['<center>','<k>'],
        ['</center>','</k>']
    ],
    'Cox_Elbert': [
        ['Mathematicians of the African diaspora<','Mathematicians of the African diaspora']
    ],
    'Cunha': [
        ['b>Anast&aacute;cio da Cunha</b>', '<b>Anastácio da Cunha</b>']
    ],
    'De_Morgan': [
        ['A Macfarlane, <i>Lectures on Ten British Mathematicians of the Nineteenth Century</i> (New York, 1916), 19-33. Brr>','A Macfarlane, <i>Lectures on Ten British Mathematicians of the Nineteenth Century</i> (New York, 1916), 19-33. Brr']
    ],
    'Dubickas': [
        ['¬√3  by rational fractions','¬√3 <i>by rational fractions']
    ],
    'Dubreil': [
        ['Noether</m>Noether</m>','Noether</m>']
    ],
    'Durer': [
        ['<a href = "Alberti.html">Alberti</a>','<m>Alberti</m>']
    ],
    'Enriques': [
        ['<<m Del_Re>Del Re</m>','<m Del_Re>Del Re</m>']
    ],
    'Escher': [
        ['<font size=-1 color=red>','<f-><r>'],
        ['</font>','</r></f>'],
        ['<b>Click <g escherpics>here</g> for a list of the pictures available from this page.</b>','''A list of all the pictures available from this page is below:\n<table width=100%><tr valign=top><td width=33%><n>\n<a href="/Diagrams/Escher_puddle.jpeg">Puddle</a>\n<a href="/Diagrams/Escher_st_peter.html">St Peter's</a>\n<a href="/Diagrams/Escher_eight_heads.html">Eight Heads</a>\n<a href="/Diagrams/Escher_alhambra.html">Lions' Court</a>\n<a href="/Diagrams/Escher_alhambra2.html">Alhambra pond</a>\n<a href="/Diagrams/Escher_alhambra3.html">1936 sketch</a>\n<a href="/Diagrams/Escher_fish.html">Fish design</a>\n<td width=33%>\n<a href="/Diagrams/Escher_horsemen.html">Horsemen</a>\n<a href="/Diagrams/Escher_horsemen_2.html">Horsemen 2</a>\n<a href="/Diagrams/Escher_circle_limit_1.html">Circle limit I</a>\n<a href="/Diagrams/Escher_circle_limit_3.html">Circle limit III</a>\n<a href="/Diagrams/Escher_circle_limit_4.html">Circle limit IV</a>\n<a href="/Diagrams/Escher_reptiles.html">Reptiles</a>\n<a href="/Diagrams/Escher_waterfall.html">Waterfall</a>\n<td width=33%>\n<a href="/Diagrams/Escher_up_and_down.html">Up and down</a>\n<a href="/Diagrams/Escher_metamorphosis_1.html">Metamorphosis I</a>\n<a href="/Diagrams/Escher_snakes.html">Snakes</a>\n<a href="/Diagrams/Escher_glass_ball.html">Glass ball</a>\n<a href="/Diagrams/Escher_rind.html">Rind</i>\n</table>''']
    ],
    'Frechet': [
        ['</blockquote>', '</Q>'],
        ['Maurice Fréchet, according to the author', '<Q>\nMaurice Fréchet, according to the author']
    ],
    'Fuchs': [
        ['equations</g>','equations']
    ],
    'Galileo': [
        ['(= Galileo)</b> (16th Arrondissement)','(= Galileo) (16th Arrondissement)']
    ],
    'Galois': [
        ['You can see a map of Paris</i></a>','You can see a map of Paris']
    ],
    'Gregory': [
        ['intellectual gifts ...\n</ind>','intellectual gifts ...\n']
    ],
    'Harlay': [
        ["(The Women's Press, London, 1986).</b>","(The Women's Press, London, 1986)."]
    ],
    'Herbrand': [
        ['<a href="Herbrand_Chevalley.html">','<a href="../Extras/Chevalley_Herbrand.html">']
    ],
    'Herstein': [
        ["You can see Herstein's Preface</a>","You can see Herstein's Preface"]
    ],
    'Hirzebruch': [
        ['1996<m>','1996']
    ],
    'Jackson_Frank': [
        ['<img src= ../Diagrams/Jackson_signature.jpeg height=91 align = right>','<d Jackson_signature.jpeg right,height="91">']
    ],
    'Knott': [
        ['An obituary</a>','An obituary']
    ],
    'Kramp': [
        ['very simple form</i>','very simple form'],
        ['I suggested the notation </i>','I suggested the notation '],
        ['<BigGamma>','<gamma>']
    ],
    'Koch': [
        ['<b>Koch</b> is best known for the fractal Koch curve.\n<p>\n<center><img src = "../Diagrams/Koch_curve.gif"></center>', '<b>Koch</b> is best known for the fractal Koch curve.<br><d Koch_curve.gif>']
    ],
    'Lamy': [
        ['</ind>\n\n</Q>','</Q>\n']
    ],
    'Landau_Lev': [
        ['<i,','<i>']
    ],
    'Laplace': [
        ["Laplace's <i>M&eacute;chanique C&eacute;leste<</i>/a>","Laplace's <i>M&eacute;chanique C&eacute;leste</i>"]
    ],
    'Le_Verrier': [
        ['<i>...','...']
    ],
    'Lewis': [
        ['<<m Peirce_Charles>','<m Peirce_Charles>']
    ],
    'Li_Chunfeng': [
        ['on the Mathematical Art</i>, giving the correct answer 27720','on the <i>Mathematical Art</i>, giving the correct answer 27720']
    ],
    'Li_Shanlan': [
        ['on the Mathematical Art</i>. By their','on the <i>Mathematical Art</i>. By their']
    ],
    'Mahler': [
        ['</ g>','</g>']
    ],
    'Molyneux_Samuel': [
        ['>http://www.europa.com/~telscope/molyneux.txt</a>','']
    ],
    'Molyneux_William': [
        ['>http://www.europa.com/~telscope/molyneux.txt</a>','']
    ],
    'Mansion': [
        ['<T 2375>.  Sur','<T 2375>.  <i>Sur']
    ],
    'Moser_William': [
        ['(> 1)','( > 1)']
    ],
    'Mosharrafa': [
        ['<ac >Royal Society of London</ac>','<ac RS>Royal Society of London</ac>']
    ],
    'Narayana': [
        ['b>Narayana</b> was an Indian','<b>Narayana</b> was an Indian']
    ],
    'Newton': [
        ['Trait<é','Traité']
    ],
    'Obi': [
        ['<ac >Nigerian Academy of Science</ac>','Nigerian Academy of Science']
    ],
    'Pappus': [
        ['the Pappus problem</a>','the Pappus problem']
    ],
    'Peschl': [
        ['</i><T 4801><i>','<T 4801>']
    ],
    'Petryshyn': [
        ['1993).</b>','1993).']
    ],
    'Pinkerton': [
        ['An obituary</a>','An obituary']
    ],
    'Plancherel': [
        ['supérieur.</i>','supérieur.'],
        ['281-284.</i>','281-284.'],
        ['available <a href="#extra">below</a>','available at <E 1>'],
        ['list <a href="#extra">below</a>','list at <E 3>']
    ],
    'Qin_Jiushao': [
        ['the Mathematical Art</i>','the <i>Mathematical Art</i>']
    ],
    'Rahn': [
        ['<img src= "../Symbolgifs/divide.gif" alt = "divide">','<s divide>']
    ],
    'Reinher': [
        ['<etiam>','']
    ],
    'Rejewski': [
        ['that the winning project "','that the winning project\n<Q>']
    ],
    'Rios': [
        ['<E2>','<E 2>']
    ],
    'Rogers_James': [
        ['<i>800</i>','800']
    ],
    'Russell': [
        ['<I>','<i>'],
        ['</I>','</i>']
    ],
    'Rutherford': [
        ['Church of the Holy Rude</a>','Church of the Holy Rude']
    ],
    'Saint-Vincent': [
        ['Geometric work on the mesolabium  </i>','Geometric work on the mesolabium ']
    ],
    'Savile': [
        ['<a Savilian','Savilian']
    ],
    'Schmidt_F-K': [
        ['paper.\n</Q>','paper.\n']
    ],
    'Scorza': [
        ['</i>3° ordine</i>','3° ordine</i>'],
        ['</i>4° ordine</i>','4° ordine</i>']
    ],
    'Scot': [
        ['<font size=-1>','<f->'],
        ['</font>','</f>']
    ],
    'Sherif': [
        ['navigation.</i>','navigation.'],
        ['<i>With the assistance','With the assistance']
    ],
    'Slebarski': [
        ['Tadeusz <S/>lebarski</b>','<b>Tadeusz <S/>lebarski</b>']
    ],
    'Snell': [
        ['</i>(Typhus','(Typhus']
    ],
    'Steinhaus': [
        ['<m><m>Edmund Landau</m> Landau</m>','<m>Edmund Landau</m>']
    ],
    'Study': [
        ['</i <T 136> >','</i> <T 136>']
    ],
    'Sun_Zi': [
        ['the Mathematical Art</i>.','the <i>Mathematical Art</i>.']
    ],
    'Szele': [
        [' >http://tudosnaptar.kfki.hu/s/z/szele/szelepant.html</a>','']
    ],
    'Tweedie': [
        ['an obituary</a>','an obituary']
    ],
    'Valiron': [
        ['</i <T 3891>>','</i> <T 3891>']
    ],
    'Wiles': [
        ['<dt>','']
    ],
    'Wilson_Bertram': [
        ['His obituary</a>','His obituary']
    ],
    'Zehfuss': [
        ['blockquote', 'Q']
    ],
    'Zenodorus': [
        ['And when Zenodorus</a>','And when Zenodorus']
    ],
    'Zhang_Heng': [
        ['Mathematical Art:-</i>','<i>Mathematical Art:-</i>']
    ],
    'Zhang_Qiujian': [
        ['Mathematical Art</i>','<i>Mathematical Art</i>']
    ],
    'Zygmund': [
        ['</i> Sur la',' <i>Sur la'],
        ['trigonométrique<i>','trigonométrique</i>'],
        ['trigonométriques<i>','trigonométriques</i>'],
    ],
    # extras
    'Adams_Leverrier': [
        ['<k><font color="blue"><h3>Searching for Neptune</h3></font>\n\n<img src="../Diagrams/Adams_Leverrier.jpeg">\n</k>','<k><bl><h3>Searching for Neptune</h3></bl>\n\n<d Adams_Leverrier.jpeg>\n</k>']
    ],
    'Aerofoil': [
        ['<img src="../Diagrams/Aerofoil.gif" align=center>','<d Aerofoil.gif center>']
    ],
    'Ahrens_publications': [
        ['<li 36.<i> ','<li 36> <i>'],
        ['<li 54.<i> ','<li 54> <i>']
    ],
    'Aleksandrov_mathematics': [
        ['\n</a>', '</a>']
    ],
    'Art_Mathematics_Music': [
        ['\n</a>', '</a>']
    ],
    'Bartlett_reviews': [
        ['</b>R Coleman, Review', 'R Coleman, Review']
    ],
    'Bolyai_house_grave': [
        ['<d ../BigPictures/Bolyai_6.jpeg>','<img src=/BigPictures/Bolyai_6.jpeg>']
    ],
    'Bolyai_letter': [
        ['''<a href="javascript:win0('Diagrams/Bolyai_letter_1.jpeg','Bolyai letter:page 1',620,820,1,1,'<br>Bolyai letter page 1')">''','<a href="/Diagrams/Bolyai_letter_1.jpeg">'],
        ['''<a href="javascript:win0('Diagrams/Bolyai_letter_2.jpeg','Bolyai letter:page 2',620,820,1,1,'<br>Bolyai letter page 2')">''','<a href="/Diagrams/Bolyai_letter_2.jpeg">']
    ],
    'Byrne_Euclid': [
        ['<Bigdelta>', '<bigdelta>']
    ],
    'Cafaro_abstracts': [
        ['<umberto.lucia@polito.it>','(umberto.lucia@polito.it)']
    ],
    'Cafaro_publications': [
        ['<umberto.lucia@polito.it>','(umberto.lucia@polito.it)']
    ],
    'Cariolaro_papers': [
        ["Un'estensione del concetto di integrale sfumato rispetto a misure compositive</i>", "Un'estensione del concetto di integrale sfumato rispetto a misure compositive"],
        ['Congressus Numerantium</i>','Congressus Numerantium'],
        ['</b>A theorem in edge colouring','A theorem in edge colouring']
    ],
    'Catalan_retirement': [
        ['1886).','1886).</f>'],
        [' (**) Following','<f->(**) Following']
    ],
    'Catalan_retirement_f': [
        ['1886.)','1886.)</f>'],
        [' (*) Par','<f->(*) Par']
    ],
    'Cayley_poem': [
        ["<a href=\"javascript:win0('BigPictures/Cayley_10.jpeg','Cayley portrait',307,430,1,1,'<br>by L C Dickenson')\">THIS LINK</a>",'<a href="../BigPictures/Cayley_10.jpeg">THIS LINK</a>']
    ],
    'De_Morgan_1859_Preface': [
        ['<Bigdelta>', '<bigdelta>']
    ],
    'De_Rham_mountaineering': [
        ['</b>Finally,','Finally,']
    ],
    'Everitt_BVP': [
        ['[<!]>','[']
    ],
    'Fields_letter': [
        ["<font color=\"blue\"><h3>Fields' Letter setting out his proposals</h3></font></center>","<bl><h3>Fields' Letter setting out his proposals</h3></bl>"]
    ],
    'Glendaruel': [
        ['<font size=-1>Photograph by Richard Cormack</font>','<f->Photograph by Richard Cormack</f>']
    ],
    'Hardy_USA': [
        ['<word?>', '']
    ],
    'Hardy_Veblen_Newman': [
        ['<word?>', '']
    ],
    'Herschel_Museum': [
        ['</a>', '']
    ],
    'Kalman_response': [
        ['>>', '> >']
    ],
    'Kelvin_sun_1': [
        ['<Li 1>', '<li 1>']
    ],
    'Kline_books': [
        ['''[<a href="javascript:ref('   C B Boyer, Review: Mathematics in Western Culture by Morris Kline, <i>Isis</i> <b>45</b> (4) (1954), 385-387.',8)">8</a>]''', '[8]'],
        ['''[<a href="javascript:ref('   J M Barbour, Review: Mathematics in Western Culture by Morris Kline, <i>Notes, Second Series</i> <b>12</b> (1) (1954), 108-109.',4)">4</a>]''','[4]'],
        ['''[<a href="javascript:ref('  W B Carver, Review: Mathematics in Western Culture by Morris Kline, <i>The American Mathematical Monthly</i> <b>62</b> (6) (1955), 460-461.',12)">12</a>]''','[12]'],
        ['''[<a href="javascript:ref('  G M Merriman, Review: Mathematics in Western Culture by Morris Kline, <i>The Scientific Monthly</i> <b>79</b> (1) (1954), 63-64.',26)">26</a>]''','[26]'],
        ['''[<a href="javascript:ref('  H F Montague, Review: Mathematics in Western Culture by Morris Kline, <i>Philosophy and Phenomenological Research</i> <b>15</b> (3) (1955), 434-436.',27)">27</a>]''','[27]'],
        ['''[<a href="javascript:ref('   T A A Broadbent, Review: Mathematics and the Physical World by Morris Kline, <i>The Mathematical Gazette</i> <b>45</b> (354) (1961), 343.',9)">9</a>]''','[9]'],
        ['''[<a href="javascript:ref('  E J Cogan, Review: Mathematics; A Cultural Approach by Morris Kline, <i>The American Mathematical Monthly</i> <b>69</b> (8) (1962), 817-818.',13)">13</a>]''','[13]'],
        ['''[<a href="javascript:ref('  W G Kellaway, Review: Calculus by Morris Kline, <i>The Mathematical Gazette</i> <b>52</b> (380) (1968), 171-172.',24)">24</a>]''','[24]'],
        ['''[<a href="javascript:ref('  R W Cowan, Review: Calculus Part One by Morris Kline, <i>Mathematics Magazine</i> <b>40</b> (5) (1967), 277.',14)">14</a>]''','[14]'],
        ['''[<a href="javascript:ref('  R W Cowan, Review: Calculus Part Two by Morris Kline, <i>Mathematics Magazine</i> <b>40</b> (5) (1967), 277.',15)">15</a>]''','[15]'],
        ['''[<a href="javascript:ref('  T A A Broadbent, Review: Mathematics in the Modern World edited by Morris Kline, <i>The Mathematical Gazette</i> <b>54</b> (387) (1970), 68.',10)">10</a>]''','[10]'],
        ['''[<a href="javascript:ref('  H Pollard, Review: Mathematical Thought from Ancient to Modern Times by Morris Kline, <i>Mathematics Magazine</i> <b>46</b> (5) (1973), 282-284.',30)">30</a>]''','[30]'],
        ['''[<a href="javascript:ref('  I Grattan-Guinness, Review: Mathematical Thought from Ancient to Modern Times by Morris Kline, <i>Science, New Series</i> <b>180</b> (4086) (1973), 627-628.',19)">19</a>]''','[19]'],
        ['''[<a href="javascript:ref('  A G Howson, Review: Mathematical Thought from Ancient to Modern Times by Morris Kline, <i>The Mathematical Gazette</i> <b>58</b> (403) (1974), 58-59.',22)">22</a>]''','[22]'],
        ['''[<a href="javascript:ref('   C B Boyer, Review: Mathematical Thought from Ancient to Modern Times by Morris Kline, <i>Isis</i> <b>65</b> (1) (1974), 104-106.',7)">7</a>]''','[7]'],
        ['''[<a href="javascript:ref('  J Niman, Review: Why Johnny Cant Add: The Failure of the New Math by Morris Kline, <i>Mathematics Magazine</i> <b>46</b> (4) (1973), 228-229.',28)">28</a>]''','[28]'],
        ['''[<a href="javascript:ref('  L Gillman, Review: Why Johnny Cant Add: The Failure of the New Math by Morris Kline, <i>The American Mathematical Monthly</i> <b>81</b> (5) (1974), 531-532.',18)">18</a>]''','[18]']
    ],
    'Konigsberg': [
        ['<img src="../Diagrams/Konigsberg.jpeg">', '<d Konigsberg.jpeg>'],
        ['<img src="../Diagrams/Konigsberg_colour.jpeg">', '<d Konigsberg_colour.jpeg>'],
        ['<img src="../Diagrams/Kaliningrad_now.jpeg">', '<d Kaliningrad_now.jpeg>']
    ],
    'Kuku_Representation_Theory': [
        ['ul>', 'ol>']
    ],
    'Levitzki_papers': [
        ['</cp>\n</Q>', '</Q>\n</cp>']
    ],
    'lion_hunting': [
        ['Aug.-Sept. 1938, pp. 446-447.</I>','Aug.-Sept. 1938, pp. 446-447.'],
        ['<A','<a'],
        ['NAME=','name='],
        ['href=','name='],
        ['</A','</a'],
        ['I>','i>'],
        ['OL>','ol>'],
        ['<Li','<li'],
        ['<LI','<li'],
        ['BR>','br>'],
        ['<HR>','\n'],
        ['<H2 ALIGN="CENTER">H. PÉTARD, Princeton, New Jersey</H2>','<k><h2>H. PÉTARD, Princeton, New Jersey</h2></k>'],
        ['<H3 ALIGN="center">2. Methods from theoretical physics</H3>','<k><h3>2. Methods from theoretical physics</h3></k>'],
        ['<H3 ALIGN="center">3. Methods from experimental physics</H3>','<k><h3>3. Methods from experimental physics</h3></k>'],
        ['<img src= "../Symbolgifs/lionint.gif" align=middle height=50>','<latex>{1\over2\pi i} \int _c{ {f(z)}\over{z-\\zeta}}dz</latex>']
    ],
    'Lusztig_citation': [
        ['(Lie groups), </i>','(Lie groups), ']
    ],
    'Milnor_books': [
        ['<Biglambda>','<biglambda>']
    ],
    'Montmort_essai': [
        ['</blockquote>',''],
        ['<i>  + etc.',' + etc.'],
        ['of series</i>','of series']
    ],
    'Muskhelishvili_President': [
        ['</Q>\nThe solution','\nThe solution']
    ],
    'NAS_founders': [
        ['Miers Fisher Longstreth, 1819-1891</b>','<b>Miers Fisher Longstreth, 1819-1891</b>']
    ],
    'Obada_publications': [
        ['(>1)','( > 1)'],
        ['>>', '> >']
    ],
    'Papers_about_Lewis': [
        ['224-23<li 3>','224-23']
    ],
    'Peirce_publications': [
        ['\\J¬0 </i>(X)','\\J¬0 (X)'],
        ['\\J¬1 </i>(X)','\\J¬1 (X)']
    ],
    'Petit_thesis': [
        ['<li 6.<i>','<li 6><i>']
    ],
    'Prandtl_publications': [
        ['<li 21.<i>','<li 21><i>'],
        ['<li 51.<i>','<li 51><i>'],
        ['<li 76.<i>','<li 76><i>'],
        ['<li 85.<i>','<li 85><i>']
    ],
    'Raffy_publications': [
        [' <ol>','</ol>']
    ],
    'Rota_Snapshots': [
        ['<Sigma>','<sigma>']
    ],
    'Rudio_Euler': [
        ['in my lifetime.','in my lifetime.</f>'],
        ['<a name="2"></a>^2','<a name="2"></a><f->^2']
    ],
    'Rudio_talk': [
        ['<t>',''],
        ['in 1523.','in 1523.</f>'],
        ['^2  Given the context and the time of writing, Rudio probably means philosophy.','<f->^2  Given the context and the time of writing, Rudio probably means philosophy.</f>'],
        ['^3  We have used the modern transcriptions of Arabic names here.','<f->^3  We have used the modern transcriptions of Arabic names here.</f>'],
        ['^4  Morgen -- unit of measurement used in Germany and some other states, used until the 20^th  century. The size of a morgen varied across the regions, from <half> acre to 2<half> acres.','<f->^4  Morgen -- unit of measurement used in Germany and some other states, used until the 20^th  century. The size of a morgen varied across the regions, from <half> acre to 2<half> acres.</f>'],
        ['^5  Published in 1766.','<f->^5  Published in 1766.</f>'],
        ['^6  "Historic news','<f->^6  "Historic news']
    ],
    'Santalo_honorary_doctorate': [
        ['</i> and the calculation <i>',' and the calculation '],
        ['</i>, instead of <i>',', instead of ']
    ],
    'Scott_publications': [
        ['217-22<li 3>','217-22']
    ],
    'Shafarevich_books': [
        ['<a href=http://www.maa.org/publications/maa-reviews/discourses-on-algebra>http://www.maa.org/publications/maa-reviews/discourses-on-algebra\n</a>','<a href=http://www.maa.org/publications/maa-reviews/discourses-on-algebra>http://www.maa.org/publications/maa-reviews/discourses-on-algebra</a>']
    ],
    'SmithHistoryPapers': [
        ['<b></b><r>The First Great Commercial Arithmetic.</r></b>','<b><r>The First Great Commercial Arithmetic.</r></b>']
    ],
    'SmithTeachingBooks': [
        ['<b><r>Oral arithmetic</r></b> (1910).</b>','<b><r>Oral arithmetic</r></b> (1910).']
    ],
    'Somerville_House': [
        ['<img src ="../Diagrams/Somerville_plaque.jpeg" border=1 >','<d Somerville_plaque.jpeg ,border="1">'],
        ['<img src ="../Diagrams/Somerville_house1.jpeg" border=1 >','<d Somerville_house1.jpeg ,border="1">'],
        ['<img src ="../Diagrams/Somerville_house2.jpeg" border=1 >','<d Somerville_house2.jpeg ,border="1">'],
        ['<img src ="../Diagrams/Burntisland.jpeg" border=1 >','<d Burntisland.jpeg ,border="1">'],
        ['<font size=-1>Photograph by Richard Cormack</font>','<f->Photograph by Richard Cormack</f>']
    ],
    'Stackel_teaching': [
        ['</f>', '</font>']
    ],
    'Stringham_address': [
        ['<d lineOP.gif >','<d lineOP.gif>']
    ],
    'Taylor_continental': [
        ['</ind>Brook Taylor','Brook Taylor'],
        ['<i>...','<Q>\n...'],
        ['Taylor.</i>\n</ind>','Taylor.\n</Q>']
    ],
    'Todhunter_Euclid_Intro': [
        ['<r><h3><k>INTRODUCTORY REMARKS</k></h3></r>','<k><h3><r>INTRODUCTORY REMARKS</r></h3></k>']
    ],
    'Truesdell_books': [
        ['</ol','</ol>']
    ],
    'Turnbull_Maclaurin_2': [
        ["friends'.","friends'.</i>"],
        ["</i> Cotes' theorem","Cotes' theorem"],
        ['<Sigma>','<sigma>']
    ],
    'Vidav_bibliography': [
        ['enacb</i>','enacb']
    ],
    'Zariski_Samuel': [
        ['<k><h3>Commutative Algebra</h3><n>','<k><h3>Commutative Algebra</h3></k>']
    ],
    'Zehfuss_publications': [
        [''' onclick="javascript:win1('../Diagrams/det_note.html',500,400); return false;"''','']
    ],
    # history topics
    'Abstract_linear_spaces': [
        ['engraving</a>','engraving'],
        ['and the common','<i>and the common'],
        ['We suppose that','<i>We suppose that']
    ],
    'African_men_1': [
        ['<ac >International Astronomical Union</ac>','<ac IAU>International Astronomical Union</ac>'],
        ['<ac >Society Industrial and Applied Mathematics</ac>','Society Industrial and Applied Mathematics'],
        ['<ac >South African Mathematics Society</ac>','South African Mathematics Society'],
        ['<X>',''],
        ['An <b>alphabetical</b> list of African men PhDs is at <a href=../Indexes/African_men_alph.html>THIS LINK</a>.','']
    ],
    'African_men_2': [
        ['<a href=African_men_1.html#Van-Der-walt>A. P. J. van der Walt</m>','<a href=African_men_1.html#Van-Der-walt>A. P. J. van der Walt</a>'],
        ['<a href=African_men_1.html#Moori>Jamshid Moori</m>.','<a href=African_men_1.html#Moori>Jamshid Moori</a>.'],
        ['An <b>alphabetical</b> list of African men PhDs is at <a href=../Indexes/African_men_alph.html>THIS LINK</a>.','']
    ],
    'African_women_1': [
        ['An <b>alphabetical</b> list of African women PhDs is at <a href=../Indexes/African_women_alph.html>THIS LINK</a>.','']
    ],
    'African_women_2': [
        ['An <b>alphabetical</b> list of African women PhDs is at <a href=../Indexes/African_women_alph.html>THIS LINK</a>.','']
    ],
    'Alcuin_book': [
        ['<b><b>Solution</b>.\n</b>','<b>Solution</b>.\n']
    ],
    'Art': [
        ['<font size=-1 color=red>','<f-><r>'],
        ['</font>','</r></f>']
    ],
    'Chinese_numerals': [
        ['<d  counting_board.gif right>','<d counting_board.gif right>'],
        ['<d  abacus.gif right>','<d abacus.gif right>']
    ],
    'crimea': [
        ['<ind><f->','<f->'],
        ['</f></k>','</f>']
    ],
    'Doubling_the_cube': [
        ['<gt>','>'],
        ['</a>(2)','(2)'],
        ['</a>(3)','(3)'],
        ['<m Wantzel><m Wantzel>Wantzel</m></m>','<m Wantzel>Wantzel</m>']
    ],
    'fair_book': [
        ['\n<f->Click it to see a larger version</f></ind></k>','<ind><f->Click it to see a larger version</f></ind></k>'],
        ['<ind><f->Click it to see a larger version</f></k>','<ind><f->Click it to see a larger version</f></ind></k>'],
        ['<i> feet. Required tonnage by common rule.\n','<i> feet. Required tonnage by common rule.</i>\n'],
        ['\nIf the length of the keel of tonnage be','\n<i>If the length of the keel of tonnage be'],
        ['6>','6 >'],
    ],
    'fractals': [
        ['Fatou biography.  <http://www-history.mcs.st-andrews.ac.uk/Biographies/Fatou.html>','<m>Fatou</m> biography.']
    ],
    'Greek_numbers': [
        ['<d greek_numbers_19.gif >','<d greek_numbers_19.gif>']
    ],
    'Greek_sources_1': [
        ['<img src= ../Diagrams/Palimpsest_small.jpeg>','<d Palimpsest_small.jpeg>']
    ],
    'Gregory_observatory': [
        [''' onclick="javascript:win1('../Extras/Gregory_commission.html',600,1000);return false;"''',''],
        [''' onclick="javascript:win1('../Extras/Gregory_Flamsteed.html',600,1000);return false;"''',''],
        [''' onclick="javascript:win1('../Extras/Gregory_Observatory.html',600,1000);return false;"''','']
    ],
    'insert': [
        ['<ind><f->Click it to see a larger version</f></k>','<f->Click it to see a larger version</f></k>']
    ],
    'Kinematic_planetary_motion': [
        ['ul>','ol>']
    ],
    'Ledermann_interview': [
        ['<font size=+1 color=red> We interviewed Walter Ledermann in St Andrews in September 2000.</font>','<f+><r>We interviewed Walter Ledermann in St Andrews in September 2000.</r></f>']
    ],
    'Light_2': [
        ['<i>Molecular','Molecular']
    ],
    'Longitude1': [
        ['History of the Académie Royale des Sciences</a>','History of the Académie Royale des Sciences'],
        ['</a>You can','You can']
    ],
    'Mathematical_games': [
        ['<E 6></a>.','<E 6>.'],
        ['15 puzzle</a>','15 puzzle'],
        ['Smullyan</a>','<m>Smullyan</m>']
    ],
    'Prime_numbers': [
        ['<a name="28">','<a name="28"></a>'],
        ['<a name="62">','<a name="62"></a>'],
        ['<li></a>','<li>']
    ],
    'Quadratic_etc_equations': [
        ['R.90</pre>','R.90']
    ],
    # honours
    'AMShistory': [
        ['<i><m>Forsyth</m></i>','<m>Forsyth</m>'],
        ['<i><m Richmond>Dr H W Richmond</m></i>','<m Richmond>Dr H W Richmond</m>'],
        ['<i><m>Dr Glaisher</m></i>','<m>Dr Glaisher</m>']
    ],
    'Chern_Medal': [
        ['<img src=../Diagrams/Chern-medal.jpeg>','<d Chern-medal.jpeg>']
    ],
    'Hirst_Prize': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'ICM': [
        ['</b></a>', '</b>'],
        ['><b>', '></a><b>'],
        [' </i>>', '</i> >'],
        ['<Maurice Auslander>','<m>Maurice Auslander</m>']
    ],
    'LMSFrolichPrize': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'LMSAddresses': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'LMShistory': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'LMSHonorary': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'LMSNaylorPrize': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'LMSPolyaPrize': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'LMSPresidents': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'LMSSeniorWhiteheadPrize': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'LMSWhiteheadPrize': [
        ['Addresses</m>','Addresses</a>'],
        ['Members</m>','Members</a>'],
        ['Prize</m>', 'Prize</a>']
    ],
    'Molyneux_Samuel': [
        ['txt\n>http://www.europa.com/~telscope/molyneux.txt</a>', 'txt']
    ],
    'Molyneux_William': [
        ['txt\n>http://www.europa.com/~telscope/molyneux.txt</a>', 'txt']
    ],
    'Noether_Lecture': [
        ['<img src=../Diagrams/Noether_award_2.jpg height=200 align=right>','<d Noether_award_2.jpg right,height="200">'],
        ['<img src=../Diagrams/Noether_award_1.jpg height=200 align=right>','<d Noether_award_1.jpg right,height="200">']
    ],
    'RShistory': [
        ['<i>About the','About the'],
        ['there...</i>','there...']
    ],
    'Sadosky_Prize': [
        ['<acWomen_in_Math>','<ac Women_in_Math>']
    ],
    'Times__obits': [
        ['</m>','</a>']
    ],
    # societies
    'Chinese_Academy': [
        ['journals.</i>','journals.']
    ],
    'EMS': [
        ['THIS LINK','THIS LINK</a>']
    ],
    'Finnish': [
        ['<m> Lindelof>','<m>Lindelof'],
        ['</i>1950<i>','1950']
    ],
    'Gottingen_Academy': [
        ['publications.</i>','publications.']
    ],
    'Indonesian': [
        ['<a name=></a>','']
    ],
    'Plato': [
        ['<i>All the evidence','All the evidence'],
        ['science.</i>','science.']
    ],
    # quotations
    'Quotations/Babbage': [
        ['blockquote>','Q>']
    ],
    'Quotations/Bers': [
        ['<img src="../Diagrams/Bers1.gif">','<d Bers1.gif>'],
        ['<img src="../Diagrams/Bers2.gif" align=center>','<d Bers2.gif center>']
    ],
    'Quotations/De_Morgan': [
        ['<font size=-1>','<f->'],
        ['</font>','</f>']
    ],
    'Quotations/Eddington': [
        ['blockquote>','Q>']
    ],
    'Quotations/Lagrange': [
        ['</i>[said','[said']
    ],
    'Quotations/Newton': [
        ['I>','i>']
    ],
    'Quotations/Planck': [
        ['<Scientific','<i>Scientific']
    ],
    'Quotations/Scott': [
        ['<pte Angas Scott>','']
    ],
    'Obits2@Baker_obituary.html': [
        ['<br>', '<ind>'],
        ['</i>Legendre<i>','<i>Legendre</i>']
    ],
    'Obits2@Fowler_David_Guardian.html': [
        ['<p>','']
    ],
    'Obits2@Gibson_obituary.html': [
        ['265- 267</i>','265- 267']
    ],
    'Obits2@Griffiths_Brian_Guardian.html': [
        ['<p>','']
    ],
    'Obits2@Hobbes_Aubrey.html': [
        ['</body></html>','']
    ],
    'Obits2@Ince_obituary.html': [
        ['<S Sigma>','<sigma>'],
        ['264.</i>','264.']
    ],
    'Obits2@Knott_obituary.html': [
        ['50-51.','50-51.</cp>']
    ],
    'Obits2@Lehmer_Emma_Berkeley.html': [
        ['at the age of 100.','at the age of 100.</b>'],
        ['She passed away','<b>She passed away']
    ],
    'Obits2@Mackay_obituary.html': [
        ['151-159.','151-159.</cp>']
    ],
    'Obits2@Mandelbrot_STelegraph.html': [
        ['<i>(</i>Mis<i>)</i>','(Mis)']
    ],
    'Obits2@Moser_Jurgen_Guardian.html': [
        ['<p>','']
    ],
    'Obits2@Munn_RSE.html': [
        ['<i>Walter Douglas Munn MA, DSc </i>(<i>Glasgow</i>)<i>, PhD <i>(</i>Cantab<i>)</i>. Born</i> 24<i>th April, </i>1929<i>, Elected FRSE </i>1<i> March</i> 1965, <i>died</i> 26th <i>October</i>, 2008.','<i>Walter Douglas Munn MA, DSc (Glasgow), PhD (Cantab). Born 24th April, 1929, Elected FRSE 1 March 1965, died 26th October, 2008.</i>']
    ],
    'Obits2@Sommerville_obituary.html': [
        ['57-60</i>','57-60']
    ],
    'Obits2@Turnbull_LMS_obituary.html': [
        ['Tram. Roy. Soc.</i>','Tram. Roy. Soc.']
    ],
    'Obits2@Tutte_Scotsman.html': [
        ['©William Tutte</b>','<b>William Tutte</b>']
    ],
    'Obits2@Whittaker_EMS_Obituary.html': [
        ['1-10.</i>','1-10.']
    ],
    'Obits2@Wren_Aubrey.html': [
        ['<p align =justify>','']
    ],
    # curves
    'Ellipse': [
        ['</a> </a>','</a>']
    ],
    'Hyperbola': [
        ['</a></a>','</a>']
    ],
    # ems
    'EMS-SCM': [
        ['dd>', 'ind>']
    ],
    'EMS_125': [
        ['center>', 'k>'],
        ['<p>', ''],
        ['<font size=-1>', '<f->'],
        ['</font>', '</f>']
    ],
    'EMS_125_Dinner': [
        ['ul>', 'ol>']
    ],
    'Zagier/Problems': [
        ['</body></html>', ''],
        ['Solution1.1','Solution11'],
        ['Solution1.2','Solution12'],
        ['Solution1.3','Solution13'],
        ['Solution2.1','Solution21'],
        ['Solution2.2','Solution22'],
        ['Solution2.3','Solution23'],
        ['Solution3.1','Solution31'],
        ['Solution3.2','Solution32'],
        ['Solution3.3','Solution33'],
        ['Solution4.1','Solution41'],
        ['Solution4.2','Solution42'],
        ['Solution4.3','Solution43'],
        ['Solution5.1','Solution51'],
        ['Solution5.2','Solution52'],
        ['Solution5.3','Solution53']
    ],
    # glossary
    'gelfonds_conjecture': [
        ['blockquote>', 'Q>']
    ],
    # astronomy
    'Astronomy/universe': [
        ['<img src=../Diagrams/universe.gif>', '<d universe.gif>']
    ],
    # alphabetical index
    'AlphaIndex/D': [
        ['de Valera, &Eacute;amon</w>', 'de Valera, &Eacute;amon']
    ],
    'AlphaIndex/M': [
        ['Moldovan, Elena Popoviciu</w>','Moldovan, Elena Popoviciu']
    ],
    'AlphaIndex/T': [
        ['Thiêm</b>, Lê V<acup>n','Thiêm, Lê V<acup>n']
    ],
    # projects
    '../datasheets/Projects/Brunk/01': [
        ['<d ch1_1.gif>','<d Projects-Brunk-Diagrams-ch1_1.gif>'],
        ['<d ch1_2.gif>','<d Projects-Brunk-Diagrams-ch1_2.gif>']
    ],
    # chronology
    '303': [
        ['\\','']
    ],
    # files
    'Strick/': [
        ["<h1><r>Heinz Klaus Strick's histories</r></h1><n>\n\n",'']
    ],
    'Tait/': [
        ['<h1>Index of material on P G Tait</h1>\n\n','']
    ],
    'Wallace/': [
        ['<k><h1><font color=red>Collection of manuscripts once belonging to William Wallace</font></h1></k>\n\n','']
    ],
    'Wallace/butterfly': [
        ['''<h2><r>William Wallace's proof of the "butterfly theorem"</r></h2>\n\n''','']
    ],
    'Miscellaneous/Popular': [
        ['<k><r><h1>Most popular biographies</h1></r></k><n>',''],
        ['<hr><n>\n<center><n>\n<table border=0 cellpadding=4 cellspacing=0 bgcolor="cyan"><n>\n<tr><td><a href="../index.html">Main Index</a><n>\n<td align=right><a href="../BiogIndex.html">Biographical Index</a>\n</table></center><hr><n>', '']
    ],
    'Miscellaneous/Popular_2009': [
        ['<k><r><h1>Most popular biographies</h1></r></k><n>',''],
        ['<hr>\n<center><n>\n<table border=0 cellpadding=4 cellspacing=0 bgcolor="cyan"><n>\n<tr><td><a href="../index.html">Main Index</a><n>\n<td align=right><a href="../BiogIndex.html">Biographical Index</a>\n</table></center><hr><n>','']
    ],
    'Darcy/darcy': [
        ['<a href="http://www-groups.dcs.st-and.ac.uk/~history/Mathematicians/Dürer.html"> ',' <a href="/Mathematicians/Durer.html">']
    ]
}


def clean(bio, name):
    # special case for the common issue
    if bio == "Papers in the Proceedings of the EMS</i>":
        return "Papers in the Proceedings of the EMS"
    if bio == "Papers in the Proceedings and Notes of the EMS</i>":
        return "Papers in the Proceedings and Notes of the EMS"

    bio = bio.replace('</i><ol><i><n>','<ol>')
    bio = bio.replace('</i><ol><i><li>','<ol><li>')

    # run all the special rules
    if name in SPECIAL_RULES:
        rules = SPECIAL_RULES[name]
        for rule in rules:
            bio = bio.replace(rule[0], rule[1])

    # John's reference hack
    bio = bio.replace('<!>', '')

    # convert strong to b
    bio = bio.replace('<strong>','<b>')
    bio = bio.replace('</strong>','</b>')

    return bio


def project_cleaning(text):
    text = text.replace('blockquote>', 'Q>')
    text = text.replace('center>', 'k>')

    # special case for project images
    #text = re.sub(r'<img src= ? (../Diagrams/\S+?)(?:>|(?:\s.+?>))', r'\n\n<allow_img \1>\n\n', text)

    regex = re.compile(r'<font size=\+1>(.*?)</font>', re.MULTILINE | re.DOTALL)
    text = re.sub(regex, r'<f+>\1</f>', text)
    regex = re.compile(r'<font size=-1>(.*?)</font>', re.MULTILINE | re.DOTALL)
    text = re.sub(regex, r'<f->\1</f>', text)

    text = text.replace('<s curlyd>', '<curlyd>')
    text = text.replace('<s phi>', '<phi>')
    text = text.replace('<s theta>', '<theta>')
    text = text.replace('<s xi>', '<xi>')
    text = text.replace('<s beta>', '<beta>')
    text = text.replace('<s zeta>', '<zeta>')
    text = text.replace('<s eta>', '<eta>')
    text = text.replace('<s gamma>', '<gamma>')
    text = text.replace('<s cross>', '<cross>')
    text = text.replace('<s gte>', '<gte>')
    text = text.replace('<s delta>', '<d>')

    text = text.replace('<gte>', '≥')
    text = text.replace('<s gte>', '≥')
    text = text.replace('<lte>', '≤')
    text = text.replace('<s lte>', '≤')
    text = text.replace('<noteq>', '≠')
    text = text.replace('<s noteq>', '≠')
    text = text.replace('<s sqrt>', '√')
    text = text.replace('<sqrt>', '√')
    text = text.replace('<s plusminus>', '±')
    text = text.replace('<plusminus>', '±')
    text = text.replace('<s approx>', '≈')



    return text
