# -*- coding: utf-8 -*-

# converts symbols to unicode

import regex as re


def symbols_to_unicode(text):
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

    symbols = ['comp','curlybigD','divide','equiv','perp','Recipe','squareshape','Harriotequal','Rudolff3rt','Rudolff4rt','intR','integral']
    translation = ['˳','𝒟','÷','≡','⟂','℞','⸋','≖','![rudolff-third-root-symbol](/symbols/rudolff3rd.gif)','![rudolff-third-root-symbol](/symbols/rudolff4rd.gif)','[math]\\int_{-\\infty}^\\infty[/math]','∫']

    # format all the symbol tags the same way
    regex = re.compile(r'<s (\S+).*?>', re.MULTILINE | re.DOTALL)
    text = re.sub(regex, r'<s \1>', text)

    for symbol, translation in zip(symbols, translation):
        text = text.replace('<s %s>' % symbol, translation)

    return text


def tags_to_unicode(text):
    # web browsers can now understand unicode fine, so there is no reason to use
    # the custom tages that get converted into symbols any more.
    # instead we can just plop in the unicode characters
    greek_tags = ['<a>','<be>','<g>','<gamma>','<d>','<e>','<th>','<theta>','<lambda>','<l>','<mu>','<nu>','<rho>','<sigma>','<psi>','<tau>','<phi>','<chi>','<omega>','<xi>','<zeta>','<eta>']
    greek_unicode = ['α','β','γ','γ','δ','ε','θ','θ','λ','λ','μ','ν','ρ','σ','ψ','τ','φ','χ','ω','ξ','ζ','η']

    math_tags = ['<bigdelta>','<bigsigma>','<sum>','<biglambda>','<bigpi>','<prod>','<bigomega>','<biggamma>','<degrees>','<curlyd>','<divide>','<pounds>','<angle>','<integral>','<intersect>','<inter>','<union>','<infinity>','<section>','<rarrow>','<cross>','<aleph>','<vec>','<wedge>','<isin>','<notin>','<half>','<isomorphic>','<forall>','<thereexists>','<subset>','<psubset>','<not>','<planck>','<tensor>']
    math_unicode = ['Δ','Σ','∑','Λ','Π','∏','Ω','Γ','°','∂','÷','£','∠','∫','∩','∩','∪','∞','§','→','×','ℵ','∧','∨','∈','∉','½','≅','∀','∃','⊆','⊂','¬','ℏ','⊗']

    other_tags = ['<scomma>','<tcomma>','<Tcomma>','<acup>','<L/>','<l/>','<o//>','<O/>','<o/>','<Zdot>','<zdot>','<ao>','<Ccup>','<z/>','<s/>','<n/>','<Scup>','<edot>','<scup>','<ccup>','<ecedil>','<ehook>','<S/>','<laplacian>','<Ao>','<dot>','<curlytheta>','<angle>','<ahook>','<scedil>','<Acup>','<atilde>','<c/>','<gcup>','<Zcup>','<zcup>','<ubar>','<u//>','<ss>','<uhook>','<ecup>','<rcup>','<uring>','<d/>']
    other_unicode = ['ș','ț','Ț','ă','Ł','ł','ő','Ø','ø','Ż','ż','å','Č','ź','ś','ń','Š','ė','š','č','ȩ','ę','Ś','∇','Å','·','ϑ','∠','ą','ş','Ǎ','ã','ć','ğ','Ž','ž','ū','ű','ß','ų','ě','ř','ů','ð']

    math_codes = ['==>','<==','<=>','|->','<-->','-->']
    math_codes_unicode = ['⇒','⇐','⇔','↦','⟷','→']

    all_tags = greek_tags + math_tags + other_tags + math_codes
    all_unicode = greek_unicode + math_unicode + other_unicode + math_codes_unicode

    for tag, unicode in zip(all_tags, all_unicode):
        text = text.replace(tag, unicode)

    return text
