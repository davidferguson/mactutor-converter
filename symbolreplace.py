# -*- coding: utf-8 -*-

# converts symbols to unicode

import regex as re


def symbols_to_unicode(text, katex=False):
    # the symbols we have to deal with are the following:
    # Harriotequal
    # Recipe
    # Rudolff3rt
    # Rudolff4rt
    # comp
    # curlybigD
    # divide
    # equiv
    # perp
    # squareshape

    # there is an issue that there are no unicode equivalents for:
    # ~~Harriotequal~~, Rudolff3rt and Rudolff4rt
    # as these are specialist symbols not found anywhere else. For these, fall
    # back to pictures, but proper pictures done by Lektor attachments

    symbols = ['comp','curlybigD','divide','equiv','perp','Recipe','squareshape','Harriotequal','Rudolff3rt','Rudolff4rt','intR','integral','sigman1inf','intat','sigmak1n','int0inf','int0x']
    translation = ['˳','𝒟','÷','≡','⟂','℞','⸋','≖','![rudolff-third-root-symbol](/symbols/rudolff3rd.gif)','![rudolff-third-root-symbol](/symbols/rudolff4rd.gif)','[math]\\int_{-\\infty}^\\infty[/math]','∫','[math]\\sum_{n=1}^\\infty[/math]','[math]\\int_t^a[/math]','[math]\\sum^n_{k=1}[/math]','[math]\\int^\\infin_0[/math]','[math]\\int^x_0[/math]']
    katex = ['_\\circ','\\mathcal{D}','\\div','\\equiv','\\perp','℞','^\\square','≖','\\sf{character not supported}','\\sf{character not supported}','\\sf{character not supported}','\\int_{-\\infty}^\\infty','\\sum_{n=1}^\\infty','\\int_t^a','\\sum^n_{k=1}','\\int^\\infin_0','\\int^x_0']

    # format all the symbol tags the same way
    regex = re.compile(r'<s (\S+)( center| middle| top)?>', re.MULTILINE | re.DOTALL)
    text = re.sub(regex, r'<s \1>', text)

    if katex:
        translation = katex

    for symbol, translation in zip(symbols, translation):
        text = text.replace('<s %s>' % symbol, translation)

    return text


def tags_to_unicode(text, katex=False):
    # web browsers can now understand unicode fine, so there is no reason to use
    # the custom tages that get converted into symbols any more.
    # instead we can just plop in the unicode characters
    greek_tags = ['<a>','<beta>','<be>','<g>','<gamma>','<d>','<e>','<th>','<theta>','<lambda>','<l>','<mu>','<nu>','<rho>','<sigma>','<psi>','<tau>','<phi>','<chi>','<omega>','<xi>','<zeta>','<eta>']
    greek_unicode = ['α','β','β','γ','γ','δ','ε','θ','θ','λ','λ','μ','ν','ρ','σ','ψ','τ','φ','χ','ω','ξ','ζ','η']
    greek_katex = ['\\alpha','\\beta','\\beta','\\gamma','\\gamma','\\delta','\\epsilon','\\theta','\\theta','\\lambda','\\lambda','\\mu','\\nu','\\rho','\\sigma','\\psi','\\tau','\\phi','\\chi','\\omega','\\xi','\\zeta','\\eta']

    math_tags = ['<bigdelta>','<bigsigma>','<sum>','<biglambda>','<bigpi>','<prod>','<bigomega>','<biggamma>','<degrees>','<curlyd>','<divide>','<pounds>','<angle>','<integral>','<intersect>','<inter>','<union>','<infinity>','<section>','<rarrow>','<cross>','<aleph>','<vec>','<wedge>','<isin>','<notin>','<half>','<isomorphic>','<forall>','<thereexists>','<subset>','<psubset>','<not>','<planck>','<tensor>']
    math_unicode = ['Δ','Σ','∑','Λ','Π','∏','Ω','Γ','°','∂','÷','£','∠','∫','∩','∩','∪','∞','§','→','×','ℵ','∧','∨','∈','∉','½','≅','∀','∃','⊆','⊂','¬','ℏ','⊗']
    math_katex = ['\\Delta','\\Sigma','\\sum','\\Lambda','\\Pi','\\prod','\\Omega','\\Gamma','\\degree','\\partial','\\div','\\pounds','\\angle','\\int','\\cap','\\cap','\\cup','\\infty','\\text{\\sect}','\\rightarrow','\\times','\\aleph','\\land','\\lor','\\isin','\\notin','1\\over2','\\approxeq','\\forall','\\exists','\\subseteq','\\subset','\\neg','\\hbar','\\otimes']

    other_tags = ['<scomma>','<tcomma>','<Tcomma>','<acup>','<L/>','<l/>','<o//>','<O/>','<o/>','<Zdot>','<zdot>','<ao>','<Ccup>','<z/>','<s/>','<n/>','<Scup>','<edot>','<scup>','<ccup>','<ecedil>','<ehook>','<S/>','<laplacian>','<Ao>','<dot>','<curlytheta>','<angle>','<ahook>','<scedil>','<Acup>','<atilde>','<c/>','<gcup>','<Zcup>','<zcup>','<ubar>','<u//>','<ss>','<uhook>','<ecup>','<rcup>','<uring>','<d/>']
    other_unicode = ['ș','ț','Ț','ă','Ł','ł','ő','Ø','ø','Ż','ż','å','Č','ź','ś','ń','Š','ė','š','č','ȩ','ę','Ś','∇','Å','·','ϑ','∠','ą','ş','Ǎ','ã','ć','ğ','Ž','ž','ū','ű','ß','ų','ě','ř','ů','ð']
    other_katex = ['ș','ț','Ț','\\check{a}','Ł','ł','\\text{\H{o}}','\\text{\\O}','\\text{\\o}','\\dot{Z}','\\dot{z}','\\text{\\r{a}}','\\check{C}','\\acute{z}','\\acute{s}','\\acute{n}','\\check{S}','\\dot{e}','\\check{s}','\\check{c}','ȩ','ę','\\acute{S}','\\nabla','\\mathring{A}','\\cdot','\\vartheta','\\angle','ą','ş','\\check{A}','\\tilde{a}','\\acute{c}','\\check{g}','\\check{~}','\\check{z}','\\bar{u}','\\text{\\H{u}}','\\text{\\ss}','ų','\\check{e}','\\check{r}','\\mathring{u}','ð']

    math_codes = ['==>','<==','<=>','|->','<-->','-->']
    math_codes_unicode = ['⇒','⇐','⇔','↦','⟷','→']
    math_codes_katex = ['\\Rightarrow','\\Leftarrow','\\Leftrightarrow','\\mapsto','\\leftrightarrow','\\rarr']

    all_tags = greek_tags + math_tags + other_tags + math_codes
    all_unicode = greek_unicode + math_unicode + other_unicode + math_codes_unicode

    if katex:
        all_unicode = greek_katex + math_katex + other_katex + math_codes_katex

    for tag, unicode in zip(all_tags, all_unicode):
        text = text.replace(tag, unicode)

    return text
