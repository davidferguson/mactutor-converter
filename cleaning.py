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
        ['<img src = "../Diagrams/Picontfrac.gif">','<d ../Diagrams/Picontfrac.gif>']
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
    'Enriques': [
        ['<<m Del_Re>Del Re</m>','<m Del_Re>Del Re</m>']
    ],
    'Escher': [
        ['<font size=-1 color=red>','<f-><r>'],
        ['</font>','</r></f>']
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
    'Herstein': [
        ["You can see Herstein's Preface</a>","You can see Herstein's Preface"]
    ],
    'Hirzebruch': [
        ['1996<m>','1996']
    ],
    'Jackson_Frank': [
        ['<img src= ../Diagrams/Jackson_signature.jpeg height=91 align = right>','<d ../Diagrams/Jackson_signature.jpeg>']
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
        ['281-284.</i>','281-284.']
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
    bio = bio.replace('<p align=justify>', '')
    bio = bio.replace('<p align=right>', '')

    # fix line breaks for list items
    bio = bio.replace('\n\n<li', '\n<li')

    return bio
