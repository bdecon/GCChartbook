def value_text(value, style='increase', ptype='percent', adj=None, 
               time_str='', digits=1, threshold=0, num_txt=True,
               casual=False, obj='singular', dollar=False, 
               round_adj=False, trail_zero=True):
    '''
    RETURN TEXT STRING FOR SPECIFIED FLOAT VALUE
    
    OPTIONS
    style: increase, increase_of, contribution, contribution_to,
           contribution_of, contribution_end
    ptype: percent, pp, None, million, etc
    adj: sa, annual, annualized, saa, saar, total, average
    time_str: blank unless specified directly, for example "one-year"
    num_txt: replace round numbers with text, for example: 9.0 -> nine
    casual: replaces certain words: decreased -> fell, for example
    obj: switch to "plural" if the object is plural, e.g. prices
    round_adj: adds "nearly" to values below the rounded value
    trail_zero: allow trailing zero
    
    '''
    text = 'Error, options not available'
    dol = '' if dollar == False else '\\$'
    abv = abs(value)
    val = f'{dol}{abv:,.{digits}f}'
    val2 = f'{dol}{value:,.{digits}f}'
    numbers = {'1.0': 'one', '2.0': 'two', '3.0': 'three', 
               '4.0': 'four', '5.0': 'five', 
               '6.0': 'six', '7.0': 'seven', 
               '8.0': 'eight', '9.0': 'nine',
               '10.0': 'ten'}
    if (num_txt == True) & (val in numbers.keys()):
        val = numbers[val] 
    indef = 'an' if ((val[0] == '8') | (val[0:3] in ['11.', '11,', '18.', '18,'])) else 'a'
    neg = True if value < 0 else False
    insig = True if abv < threshold else False
    plural = 's' if ((abv > 1.045) & (style[-3:] != 'end')) else ''
    ptxtd = {None: '', 'none': '', 'None': '', '': '', 'percent': ' percent', 
             'pp': f' percentage point{plural}', 'point': f' point{plural}',
             'trillion': ' trillion', 'billion': ' billion', 'million': ' million', 
             'thousand': ' thousand', 'units': ' units'}
    ptxt = ptxtd[ptype]
    rnd_adj = ('' if ((round_adj == False) | (abv >= round(abv, digits))) 
    		   else 'nearly ' if casual == False else 'almost ')
    
    if style in ['increase', 'increase_by', 'gain', 'return']:
        atxtd = {None: ' by ', 'sa': ' at a seasonally-adjusted rate of ', 
                 'annual': ' at an annual rate of ', 
                 'annualized': ' at an annualized rate of ', 
                 'average_annualized': ' at an average annualized rate of ',
                 'avg_ann': ' at an average annualized rate of ',
                 'saa': ' at a seasonally-adjusted and annualized rate of ', 
                 'saar': ' at a seasonally-adjusted annualized rate of ', 
                 'total': ' by a total of ', 
                 'inflation': ' the inflation rate by ',
                 'average': ' at an average rate of ',
                 'equivalent': ' by the equivalent of '}
        if style != 'increase_by':
            atxtd[None] = ' '
        if style in ['gain', 'return']:
        	atxtd['total'] = ' a total of '
        atxt = atxtd[adj]
        stxt = 'increased' if neg == False else 'decreased'
        if style == 'gain':
        	stxt = 'gained' if neg == False else 'lost'
        if style == 'return':
        	stxt = 'returned' if neg == False else 'lost'
        if adj == 'inflation':
        	stxt = 'increased' if neg == False else 'reduced'
        ttxt = f' over the {time_str} period' if time_str != '' else ''
        text = f'{stxt}{atxt}{val}{ptxt}{ttxt}'
        if insig == True:
            text = 'was virtually unchanged'
            if obj == 'plural':
                text = 'were unchanged'
            
    if style in ['contribution', 'contribution_to']:
        atxtd = {None: '', 'sa': ' on a seasonally-adjusted basis', 
                 'annual': ' on an annual basis', 
                 'annualized': ' on an annualized-basis', 
                 'average_annualized': ' on an average annualized basis ',
                 'avg_ann': ' on an average and annualized rate basis ',
                 'saa': ' on a seasonally-adjusted and annualized basis', 
                 'saar': ' on a seasonally-adjusted annualized basis', 
                 'total': ' in total',
                 'average': ' on an average basis'}
        atxt = atxtd[adj]
        atxt2 = 'the equivalent of ' if adj == 'equivalent' else ''
        stxt = ('contributed', 'to') if neg == False else ('subtracted', 'from')
        ttxt = f' over the {time_str} period' if time_str != '' else ''
        text = f'{stxt[0]} {atxt2}{val}{ptxt}{atxt}{ttxt}'
        if style == 'contribution_to':
            text = f'{stxt[0]} {atxt2}{val}{ptxt} {stxt[1]}'
        if insig == True:
            text = 'did not contribute'
            if style == 'contribution_to':
                text = 'did not contribute to'
            
    elif style in ['increase_of', 'contribution_of', 'return_of']:
        stxt1 = 'increase' if neg == False else 'decrease'
        stxt2 = 'an increase' if neg == False else 'a decrease'
        if style == 'contribution_of':
            stxt1 = 'contribution' if neg == False else 'subtraction'
            stxt2 = 'a contribution' if neg == False else 'a subtraction'    
        if style == 'return_of':
            stxt1 = 'return' if neg == False else 'loss'
            stxt2 = 'a return' if neg == False else 'a loss'   
        if style == 'gain_of':
            stxt1 = 'gain' if neg == False else 'loss'
            stxt2 = 'a gain' if neg == False else 'a loss'             
        if time_str != '':
            stxt2 = f'a {time_str}{stxt1}'
        atxtd = {None: f'{stxt2} of', 'sa': f'a seasonally-adjusted {time_str}{stxt1} of', 
                 'annual': f'an annual {time_str}{stxt1} of', 
                 'annualized': f'an annualized {time_str}{stxt1} of', 
                 'average_annualized': f' an average annualized {time_str}{stxt1} of',
                 'avg_ann': f' an average annualized {time_str}{stxt1} of',
                 'saa': f'a seasonally-adjusted and annualized {time_str}{stxt1} of', 
                 'saar': f'a seasonally-adjusted annualized {time_str}{stxt1} of', 
                 'total': f'a total {time_str}{stxt1} of',
                 'average': f'an average {time_str}{stxt1} of'}
        atxt = atxtd[adj]
        atxt2 = 'the equivalent of ' if adj == 'equivalent' else ''
        text = f'{atxt} {atxt2}{val}{ptxt}'
        if insig == True:
            text = 'virtually no change'
            if style[:3] == 'con':
                text = 'virtually no contribution'
            
    elif style in ['increase_end', 'contribution_end']:
        stxt = 'increase' if neg == False else 'decrease'
        if style == 'contribution_end':
            stxt = 'contribution' if neg == False else 'subtraction'
        atxtd = {None: f'{indef} ', 'sa': 'a seasonally-adjusted ', 
                 'annual': 'an annual ', 
                 'annualized': 'an annualized ', 
                 'average_annualized': ' an average annualized ',
                 'avg_ann': ' an average and annualized ',
                 'saa': 'a seasonally-adjusted and annualized ', 
                 'saar': 'a seasonally-adjusted annualized ', 
                 'total': 'a total ',
                 'average': 'an average '}
        atxt = atxtd[adj]
        ttxt = f'{time_str} ' if time_str != '' else ''
        text = f'{atxt}{ttxt}{val}{ptxt} {stxt}'
        if insig == True:
            text = 'virtually no change'
            if style[:3] == 'con':
                text = 'virtually no contribution'
                
    elif style == 'above_below':
        stxt = 'above' if neg == False else 'below'
        text = f'{val}{ptxt} {stxt}'
        if insig == True:
            text = 'in line with'
            
    elif style == 'plain':
    	val3 = val
    	pn = '' if neg == False else 'negative '
    	# Handle rounded values
    	num_abv = {k[0]: v for k, v in numbers.items()}
    	if (num_txt == True) & (val in num_abv.keys()):
        	val3 = num_abv[val] 
        	if float(val) > value:
        		rnd_adj = 'nearly ' if casual == False else 'almost '
    	text = f'{rnd_adj}{pn}{val3}{ptxt}'
    
    elif style in ['equivalent', 'eq']:
    	atxt = ' of GDP' if adj in ['gdp', 'GDP'] else ''
    	text = f'equivalent to {val}{ptxt}{atxt}'
    	
    elif style == 'added_lost':
    	stxt = 'added' if neg == False else 'lost'
    	atxtd = {None: '', 'average': 'an average of '}
    	atxt = atxtd[adj]
    	text = f'{stxt} {atxt}{val}{ptxt}'
    	
    elif style == 'added_lost_rev':
    	stxt = 'added' if neg == False else 'lost'
    	text = f'{val}{ptxt} {stxt}'
    
    if casual == True:
        text = (text.replace('added', 'gained')
        		    .replace('decreased', 'fell')
                    .replace('contributed', 'added')
                    .replace('increased', 'grew')
                    .replace('contribute ', 'add ')
                    .replace('subtract ', 'remove ')
                    .replace('a contribution', 'an addition')
                    .replace('contribution', 'addition')
                    .replace('decrease', 'fall')
                    .replace('subtraction', 'reduction')
                    .replace('an increase of', 'growth of')
                    .replace('increase of', 'growth of')
                    .replace('decrease of', 'fall of'))
                    
    if obj == 'plural':
        text = (text.replace('was', 'were'))
        
    if trail_zero == False:
    	text = text.replace('.0 ', ' ')
    
    return(text)
    
