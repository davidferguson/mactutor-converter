import regex as re

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
        ['<img src = "../Diagrams/Picontfrac.gif">','<d /Diagrams/Picontfrac.gif>']
    ],
    'Cafiero': [
        ['<Funzioni','Funzioni']
    ],
    'Carleman': [
        ['positive numbers, then\n<ind>\n\\<s','positive numbers, then\n\n\\<s'],
        ['a¬n \\\\ \n</ind>\nand the constant','a¬n \\\\ \nand the constant']
    ],
    'Colson': [
        ['3709286573961472<pre>','3709286573961472</pre>'],
        ['2308726432039468<pre>','2308726432039468</pre>']
    ],
    'Copson': [
        ['<center>','<k>'],
        ['</center>','</k>']
    ],
    'Cox_Elbert': [
        ['Mathematicians of the African diaspora<','Mathematicians of the African diaspora']
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
        ['</font>','</r></f>']
    ],
    'Forsythe': [
        ['<i><ol type=a><li>','<ol type=a><li>'],
        ['</ol></i>', '</ol>']
    ],
    'Frechet': [
        ['</blockquote>', '</Q>'],
        ['Maurice Fréchet, according to the author', '<Q>\nMaurice Fréchet, according to the author']
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
        ['<img src= ../Diagrams/Jackson_signature.jpeg height=91 align = right>','<d /Diagrams/Jackson_signature.jpeg>']
    ],
    'Knott': [
        ['An obituary</a>','An obituary']
    ],
    'Kramp': [
        ['very simple form</i>','very simple form'],
        ['I suggested the notation </i>','I suggested the notation '],
        ['<BigGamma>','<gamma>']
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
    'Machin': [
        ['<font face=symbol>p</font>','p']
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
    'Netto': [
        [' <!T 5722>', ''],
        [' <!T 5723>',''],
        [' <!T 5724>','']
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
        ["<i>Sur les valeurs asymptotiques des polynomes d'Hermite H<sub>n</sub>(x)=(-1)<sup>n</sup> e<sup>x<sup>2</sup>/2</sup>d<sup>n</sup>/dx<sup>n</sup>(e<sup>-x<sup>2</sup>/2</sup>).</i>","<i>Sur les valeurs asymptotiques des polynomes d'Hermite H<sub>n</sub>(x)=(-1)<sup>n</sup> e<sup>x2/2</sup>d<sup>n</sup>/dx<sup>n</sup>(e<sup>-x2/2</sup>).</i>"],
        ['supérieur.</i>','supérieur.'],
        ['281-284.</i>','281-284.'],
        ['available <a href="#extra">below</a>','available at <E 1>'],
        ['list <a href="#extra">below</a>','list at <E 3>']
    ],
    'Qin_Jiushao': [
        ['the Mathematical Art</i>','the <i>Mathematical Art</i>']
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
    'Sachs': [
        ['<! For the contents of these books, see  ...>','']
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
    'Schutzenberger': [
        ['<!  One topic which we have not mention so far is one which Schützenberger held very strong views - the theory of evolution. A short quote from [ 3] in given at this link: Schützenberger on Darwinism -- >','']
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
        ['<k><font color="blue"><h3>Searching for Neptune</h3></font>\n\n<img src="../Diagrams/Adams_Leverrier.jpeg">\n</k>','<h3>Searching for Neptune</h3>\n\n<k><d /Diagrams/Adams_Leverrier.jpeg>\n</k>']
    ],
    'Aerofoil': [
        ['<img src="../Diagrams/Aerofoil.gif" align=center>','<d /Diagrams/Aerofoil.gif>']
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
    'Byrne_Euclid': [
        ['<Bigdelta>', '<bigdelta>']
    ],
    'Cafaro_abstracts': [
        ['<umberto.lucia@polito.it>','(umberto.lucia@polito.it)']
    ],
    'Cafaro_publications': [
        ['<umberto.lucia@polito.it>','(umberto.lucia@polito.it)']
    ],
    'Cajori_history': [
        ['<k><r><h3>by Florian Cajori </h3> </r></k>','<h3><r>by Florian Cajori</r></h3>']
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
    'Cheney_books': [
        ['<ind>\n<b>1.1. From the Preface.</b>','<b>1.1. From the Preface.</b>'],
        ['</ind></ind>', '</ind>'],
        ['<ind>\n<b>2.1. From the Preface.</b>','<b>2.1. From the Preface.</b>'],
        ['<ind>\n<b>3.1. From the Preface.</b>','<b>3.1. From the Preface.</b>'],
        ['<ind>\n<b>4.1. From the Preface.</b>','<b>4.1. From the Preface.</b>'],
        ['<ind>\n<b>5.1. From the Preface.</b>','<b>5.1. From the Preface.</b>'],
        ['<ind>\n<b>6.1. From the Preface.</b>','<b>6.1. From the Preface.</b>'],
        ['<ind>\n<b>7.1. From the Preface.</b>','<b>7.1. From the Preface.</b>']
    ],
    'Combinatorial_algorithms': [
        ['</ind></ind>', '</ind>'],
        ['<ind>\n<b>1.1 From the Preface.</b>','<b>1.1 From the Preface.</b>'],
        ['<ind>\n<b>2.1. From the Preface.</b>','<b>2.1. From the Preface.</b>'],
        ['<ind>\n<b>3.1. Review by: Peter Eades.</b>','<b>3.1. Review by: Peter Eades.</b>']
    ],
    'Dahlin_Extracts': [
        ['also in Sweden. \n</ind>','also in Sweden.']
    ],
    'De_Morgan_1859_Preface': [
        ['<Bigdelta>', '<bigdelta>'],
        ['<ind>\n\\(x','\n\\(x'],
        ['\\\\\n</ind>','\\\\\n']
    ],
    'De_Rham_mountaineering': [
        ['</b>Finally,','Finally,']
    ],
    'Everitt_BVP': [
        ['[<!]>','[']
    ],
    'Fields_letter': [
        ["<font color=\"blue\"><h3>Fields' Letter setting out his proposals</h3></font></center>","<h3><bl>Fields' Letter setting out his proposals</bl></h3>"]
    ],
    'Finkel_solution': [
        ['<b><k>','<k>'],
        ['</k></b>','</k>']
    ],
    'Fisher_Statistical_Methods': [
        ['<b>1.<ind> The Scope of Statistics</ind></b>','<ind><b>1. The Scope of Statistics</b></ind>'],
        ['<b>2. <ind>General Method, Calculation of Statistics</ind></b>','<ind><b>2. General Method, Calculation of Statistics</b></ind>'],
        ['<b>3. <ind>The Qualifications of Satisfactory Statistics</ind></b>','<ind><b>3. The Qualifications of Satisfactory Statistics</b></ind>']
    ],
    'Gauss_Disquisitiones': [
        ['<k><r><h2>Dedication</h2></r></k><n>','<h2><r>Dedication</r></h2>'],
        ["<k><r><h3>AUTHOR'S PREFACE</h3></r></k>","<h3><r>AUTHOR'S PREFACE</r></h3>"]
    ],
    'Glendaruel': [
        ['<font size=-1>Photograph by Richard Cormack</font>','<f->Photograph by Richard Cormack</f>']
    ],
    'Hardy_USA': [
        ['<word?>', '']
    ],
    'Hardy_USA_lectures': [
        ['<b>University of Pennsylvania','University of Pennsylvania'],
        ['March, 1928</b>', 'March, 1928'],
        ['<b>University of Iowa, December', 'University of Iowa, December'],
        ['30 March, 1929</b>', '30 March, 1929'],
        ['<b>Harvard University', 'Harvard University'],
        ['July-10 August, 1929</b>','July-10 August, 1929']
    ],
    'Hardy_Veblen_Newman': [
        ['<word?>', '']
    ],
    'Harvey_obituaries': [
        ['</ol>\n</ind>', '</ol>']
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
        ['<img src="../Diagrams/Konigsberg.jpeg">', '<d ../Diagrams/Konigsberg.jpeg>'],
        ['<img src="../Diagrams/Konigsberg_colour.jpeg">', '<d ../Diagrams/Konigsberg_colour.jpeg>'],
        ['<img src="../Diagrams/Kaliningrad_now.jpeg">', '<d ../Diagrams/Kaliningrad_now.jpeg>']
    ],
    'Kuku_Representation_Theory': [
        ['ul>', 'ol>']
    ],
    'Landau_Contents': [
        ['<k><h2>FOUNDATIONS OF ANALYSIS</h2></k><n>','<h2>FOUNDATIONS OF ANALYSIS</h2>'],
        ['<k><h3>THE ARITHMETIC OF\nWHOLE, RATIONAL, IRRATIONAL AND COMPLEX NUMBERS</h3></k><n>','<h3>THE ARITHMETIC OF\nWHOLE, RATIONAL, IRRATIONAL AND COMPLEX NUMBERS</h3>'],
        ['<k>BY','BY'],
        ['<h3>EDMUND LANDAU</h3></k><n>','<h3>EDMUND LANDAU</h3>'],
        ['<k><gr><h3><r>TABLE OF CONTENTS</r></h3></gr></k>','<h3><r>TABLE OF CONTENTS</r></h3>']
    ],
    'Levitzki_papers': [
        ['</cp>\n</Q>', '</Q>\n</cp>']
    ],
    'lion_hunting': [
        ['Aug.-Sept. 1938, pp. 446-447.</I>','Aug.-Sept. 1938, pp. 446-447.'],

        ['<A HREF="#fn1" NAME="f1"><f->(1)</f></A>','<a name="f1"></a><a href="#fn1"><f->(1)</f></a>'],
        ['<A HREF="#fn2" NAME="f2"><f->(2)</f></A>','<a name="f2"></a><a href="#fn2"><f->(2)</f></a>'],
        ['<A HREF="#fn3" NAME="f3"><f->(3)</f></A>','<a name="f3"></a><a href="#fn3"><f->(3)</f></a>'],
        ['<A HREF="#fn4" NAME="f4"><f->(4)</f></A>','<a name="f4"></a><a href="#fn4"><f->(4)</f></a>'],
        ['<A HREF="#fn5" NAME="f5"><f->(5)</f></A>','<a name="f5"></a><a href="#fn5"><f->(5)</f></a>'],
        ['<A HREF="#fn6" NAME="f6"><f->(6)</f></A>','<a name="f6"></a><a href="#fn6"><f->(6)</f></a>'],
        ['<A HREF="#fn7" NAME="f7"><f->(7)</f></A>','<a name="f7"></a><a href="#fn7"><f->(7)</f></a>'],
        ['''<A HREF="#f1"><f->(1)</f></A> <A NAME="fn1">By Hilbert. See E. W. Hobson, <i>The Theory of Functions of a Real Variable and the Theory of Fourier's Series</i>, 1927, vol. 1, pp. 456-457.</A>''','''<a href="#f1"><f->(1)</f></a> <a name="fn1"></a>By Hilbert. See E. W. Hobson, <i>The Theory of Functions of a Real Variable and the Theory of Fourier's Series</i>, 1927, vol. 1, pp. 456-457.'''],
        ['''<A HREF="#f2"><f->(2)</f></A> <A NAME="fn2">H. Seifert and W. Threlfall, <i>Lehrbuch der Topologie</i>, 1934, pp. 2-3.</A>''','''<a href="#f2"><f->(2)</f></a> <a name="fn2"></a>H. Seifert and W. Threlfall, <i>Lehrbuch der Topologie</i>, 1934, pp. 2-3.'''],
        ['''<A HREF="#f3"><f->(3)</f></A> <A NAME="fn3"><I>N.B.</I> By Picard's Theorem (W. F. Osgood, <i>Lehrbuch der Funktionentheorie</i>, vol. 1, 1928, p.748), we can catch every lion with at most one exception.</A>''','''<a href="#f3"><f->(3)</f></a> <a name="fn3"></a><I>N.B.</I> By Picard's Theorem (W. F. Osgood, <i>Lehrbuch der Funktionentheorie</i>, vol. 1, 1928, p.748), we can catch every lion with at most one exception.'''],
        ['''<A HREF="#f4"><f->(4)</f></A> <A NAME="fn4">N. Wiener, <I>l. c.</I>, p. 89.</A>''','''<a href="#f4"><f->(4)</f></a> <a name="fn4"></a>N. Wiener, <I>l. c.</I>, p. 89.'''],
        ['''<A HREF="#f5"><f->(5)</f></A> <A NAME="fn5">N. Wiener, <i>The Fourier Integral and Certain of its Applications</i>, 1933, pp. 73-74.</A>''','''<a href="#f5"><f->(5)</f></a> <a name="fn5"></a>N. Wiener, <i>The Fourier Integral and Certain of its Applications</i>, 1933, pp. 73-74.'''],
        ['''<A HREF="#f6"><f->(6)</f></A> <A NAME="fn6">See, for example, H. A. Bethe and\nR. F. Bacher, Reviews of Modern Physics, vol. 8, 1936, pp. 82-229; especially pp. 106-107.</A>''','''<a href="#f6"><f->(6)</f></a> <a name="fn6"></a>See, for example, H. A. Bethe and R. F. Bacher, Reviews of Modern Physics, vol. 8, 1936, pp. 82-229; especially pp. 106-107.'''],
        ['''<A HREF="#f7"><f->(7)</f></A> <A NAME="fn7"><I>Ibid</I>.</A>''','''<a href="#f7"><f->(7)</f></a> <a name="fn7"></a><I>Ibid</I>.'''],

        ['<H2 ALIGN="CENTER">H. PÉTARD, Princeton, New Jersey</H2>','<h2>H. PÉTARD, Princeton, New Jersey</h2>'],
        ['I>','i>'],
        ['OL>','ol>'],
        ['<Li','<li'],
        ['<LI','<li'],
        ['BR>','br>'],
        ['<HR>','\n'],
        ['<H3 ALIGN="center">2. Methods from theoretical physics</H3>','<h3>2. Methods from theoretical physics</h3>'],
        ['<H3 ALIGN="center">3. Methods from experimental physics</H3>','<h3>3. Methods from experimental physics</h3>'],
        ['<img src= "../Symbolgifs/lionint.gif" align=middle height=50>','<d ../Symbolgifs/lionint.gif>']
    ],
    'Lonie_education': [
        ['<r><h2>Education Scotland, Session 1867-68</h2></r>','<h2><r>Education Scotland, Session 1867-68</r></h2>'],
        ['<r><h2>Letter to the Commissioners, Education Scotland</h2></r>','<h2><r>Letter to the Commissioners, Education Scotland</r></h2>'],
        ['<r><h2>Lonie honoured at dinner in 1881</h2></r>','<h2><r>Lonie honoured at dinner in 1881</r></h2>']
    ],
    'Lusztig_citation': [
        ['(Lie groups), </i>','(Lie groups), ']
    ],
    'Maclaurin_publications': [
        ['<li 5>Publications in the <i>Philosophical Transactions</i> -\n<ol type=a>','</ol>\nPublications in the <i>Philosophical Transactions</i> -\n<ol>'],
        ['<li 6>Publications in the Physical and Literary Society, Edinburgh, Vol. I.\n<ol type=a>','Publications in the Physical and Literary Society, Edinburgh, Vol. I.\n<ol>'],
        ['</ol></ol><n>','</ol>']
    ],
    'May_papers': [
        ['<ol><li>A student run colloquium.\n<li>A student run publication.\n<li>A student mathematics club that supports these activities and engages in others appropriate to the local situation.\n<li>A faculty member who keeps a friendly eye on things and helps as needed.\n<li>Some link of these activities with the curriculum.\nIdeally, research-like activity should be part of every course (the quantity and quality varying with the context) and should be officially recognised by graduation honours, special courses, and the like. In short, undergraduate research should become a normal part of the curricular and extra-curricular educational process.\n</ol>', '1. A student run colloquium.\n2. A student run publication.\n3. A student mathematics club that supports these activities and engages in others appropriate to the local situation.\n4. A faculty member who keeps a friendly eye on things and helps as needed.\n5. Some link of these activities with the curriculum. Ideally, research-like activity should be part of every course (the quantity and quality varying with the context) and should be officially recognised by graduation honours, special courses, and the like. In short, undergraduate research should become a normal part of the curricular and extra-curricular educational process.'],
        ['<ol><li>There should be a purpose, stated or implicitly clear, and this purpose should be achieved.\n<li>Assertions should be supported by evidence and argument. This requirement corresponds to insistence on proof in mathematics. In learned articles it involves careful citation and close reasoning. In popularizations it is sufficient to indicate where the missing evidence can be found.\n<li>There should be clarity and complete disclosure. This corresponds to the mathematical requirement of rigour. ...\n</ol>','1. There should be a purpose, stated or implicitly clear, and this purpose should be achieved.\n2. Assertions should be supported by evidence and argument. This requirement corresponds to insistence on proof in mathematics. In learned articles it involves careful citation and close reasoning. In popularizations it is sufficient to indicate where the missing evidence can be found.\n3. There should be clarity and complete disclosure. This corresponds to the mathematical requirement of rigour. ...']
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
        ['<a name="2"></a>^2','<f-><a name="2"></a>^2']
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
    'Sassoon_Alcuin': [
        ['<r><h3>Awareness of Alcuin</h3></r>','<h3><r>Awareness of Alcuin</r></h3>']
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
        ['<img src ="../Diagrams/Somerville_plaque.jpeg" border=1 >','<d ../Diagrams/Somerville_plaque.jpeg>'],
        ['<img src ="../Diagrams/Somerville_house1.jpeg" border=1 >','<d ../Diagrams/Somerville_house1.jpeg>'],
        ['<img src ="../Diagrams/Somerville_house2.jpeg" border=1 >','<d ../Diagrams/Somerville_house2.jpeg>'],
        ['<img src ="../Diagrams/Burntisland.jpeg" border=1 >','<d ../Diagrams/Burntisland.jpeg>'],
        ['<font size=-1>Photograph by Richard Cormack</font>','<f->Photograph by Richard Cormack</f>']
    ],
    'Stackel_teaching': [
        ['<font color=magenta>Article by: Vicky Ryan (University of St Andrews)</f>','<font color=purple>Article by: Vicky Ryan (University of St Andrews)</font>']
    ],
    'Stringham_address': [
        ['<img src=../Curvepics/Parabola/Parabola1.gif height=250 align=right>','<d ../Curvepics/Parabola/Parabola1.gif>'],
        ['<d lineOP.gif >','<d lineOP.gif>']
    ],
    'Stuart_vanity': [
        ['<img src= ../BigPictures/Stuart_3.jpeg>','<d ../BigPictures/Stuart_3.jpeg>']
    ],
    'Taylor_continental': [
        ['</ind>Brook Taylor','Brook Taylor'],
        ['<i>...','<Q>\n...'],
        ['Taylor.</i>\n</ind>','Taylor.\n</Q>']
    ],
    'Todhunter_Euclid_Intro': [
        ['<r><h3><k>INTRODUCTORY REMARKS</k></h3></r>','<h3><r>INTRODUCTORY REMARKS</r></h3>']
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
    'Wilson_depression': [
        ['<font color=magenta>','<font color=purple>']
    ],
    'Zariski_Samuel': [
        ['<k><h3>Commutative Algebra</h3><n>','<h3>Commutative Algebra</h3>']
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
        ['<X>','']
    ],
    'African_men_2': [
        ['<a href=African_men_1.html#Van-Der-walt>A. P. J. van der Walt</m>','<a href=African_men_1.html#Van-Der-walt>A. P. J. van der Walt</a>'],
        ['<a href=African_men_1.html#Moori>Jamshid Moori</m>.','<a href=African_men_1.html#Moori>Jamshid Moori</a>.']
    ],
    'Alcuin_book': [
        ['<b><b>Solution</b>.\n</b>','<b>Solution</b>.\n']
    ],
    'Art': [
        ['<font size=-1 color=red>','<f-><r>'],
        ['</font>','</r></f>']
    ],
    'Chinese_numerals': [
        ['<d  counting_board.gif right>','<d counting_board.gif>'],
        ['<d  abacus.gif right>','<d abacus.gif>']
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
        ['6>','6 >']
    ],
    'fractals': [
        ['Fatou biography.  <http://www-history.mcs.st-andrews.ac.uk/Biographies/Fatou.html>','<m>Fatou</m> biography.']
    ],
    'Greek_numbers': [
        ['<d greek_numbers_19.gif >','<d greek_numbers_19.gif>']
    ],
    'Greek_sources_1': [
        ['<img src= ../Diagrams/Palimpsest_small.jpeg>','<d ../Diagrams/Palimpsest_small.jpeg>']
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
    'Maxwell_House': [
        ['<img align=right src="../Miscellaneous/JCMBhouse/Diagram.gif" >','<d ../Miscellaneous/JCMBhouse/Diagram.gif>']
    ],
    'Prime_numbers': [
        ['<a name="28">','<a name="28"></a>'],
        ['<a name="62">','<a name="62"></a>'],
        ['<li></a>','<li>']
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

    # remove these as they have no BBCode equivalent
    bio = bio.replace('<br clear=right>', '')
    bio = bio.replace('<br clear = right>','')
    bio = bio.replace('<br clear="right">','')
    bio = bio.replace('<br clear="right" right>','')
    bio = bio.replace('<p align=justify>', '')
    bio = bio.replace('<p align=right>', '')
    bio = bio.replace('<p align="right">','')
    bio = bio.replace('<hr>', '\n')

    # not sure what these are. don't seem to be converted anywhere, and they're
    # not a standard HTML tag...
    bio = bio.replace('</pr>','')
    bio = bio.replace('<pr>', '')

    # fix line breaks for list items
    bio = bio.replace('\n\n<li', '\n<li')

    return bio
