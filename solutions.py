# Solution 1 (building the ngram dataset) [required]
        for i in range(1,4):                        
            for char_sequence in subsequences(characters, i):                
                if ''.join(char_sequence) in ngram[i]:
                    ngram[i][''.join(char_sequence)] += 1
                else:
                    ngram[i][''.join(char_sequence)] = 1        

ngram[0] = np.sum(list(ngram[1].values()))                

# Solution 2 (getProbability) [required]
def getProbability(character, context, ngram):
	model_order  = len(context) + 1
    sequence = ''.join(context + [character])
    numerator = ngram[model_order][sequence]
    if model_order == 1:
        denominator = ngram[model_order-1]
    else:    
        denominator = ngram[model_order-1][''.join(context)] 
    return(float(numerator) / float(denominator))
        

# Solution 3 (getGuessCount) [optional]
def getGuessCount(sh_chars, ngram, order):	
	counts =[]
    output = []
    for char_index in range(len(sh_chars)):          
        preceding_context = output[max(0, char_index-(order -1)):char_index]
        
        cds = ngram[len(preceding_context)+1].keys() #cds = candidates
        #but not all of these are consistent with the preceding context
        filtered_cds = [x for x in cds if list(x)[0:len(preceding_context)] == preceding_context]
        
        filtered_counts = np.array([ngram[len(preceding_context)+1][x] for x in filtered_cds])
        if len(preceding_context) == 0:
            normalizer = float(ngram[0])
        else:
            normalizer = float(np.sum(filtered_counts))
            
        filtered_probs = filtered_counts / normalizer
        
        #reorder the candidates by their probabilities
        descending_order = np.argsort(filtered_probs)[::-1]        
        ordered_candidates = np.array(filtered_cds)[descending_order]
        
        num_guesses = np.argwhere(np.array([list(x)[-1] for x in ordered_candidates]) == sh_chars[char_index])[0][0]+1        
        # add one b/c first item is at index 0
        output.append(sh_chars[char_index])
        counts.append(num_guesses) 
	return (counts)

# Solution 4 (rmse) [required]
def rmse(array1, array2):
    return(np.sqrt(np.sum((array1 - array2)** 2.) / len(array1)))

# Solution 5 [optional]
def plotModelsForTrial(trial_index):
    df = web_expt[web_expt.trial == trial_index]
    df.sort_values(by='position')
    char_seq = list(sentences[trial_index])
    df['character'] = char_seq
    df['unigram'] = getGuessCount(char_seq, ngram, 1)
    df['bigram'] = getGuessCount(char_seq, ngram, 2)
    df['trigram'] = getGuessCount(char_seq, ngram, 3)
    
    mdf = pd.melt(df, id_vars=['position'], value_vars=['count','unigram','bigram','trigram'])

    print(ggplot.ggplot(mdf, ggplot.aes(x='position', y='value', colour='variable')) +\
    ggplot.geom_line() + ggplot.theme_bw() + ggplot.ylab('Number of Guesses'))


# Solution 6 (computing the probability of a corpus) [optional]
def computeProbTestSet(filename, order, ngram):	
	probs_store = [] 
    with open(filename,'r') as f:
        for x in f:
            words = x.replace('\n','').split(' ')
            characters = [x.lower() for x in list(x.replace('\n',''))]        
            sequences = subsequences(characters,order)
            sentence_prob = []
            for sequence in sequences:
                sentence_prob.append(np.log(getProbability(sequence[order-1], list(sequence)[0:order-1], ngram)))
            probs_store.append(np.sum(sentence_prob))    
    return(np.sum(probs_store))


# Solution 7 (generateString) [optional]
def generateString(charlength, ngram, order):    
    output = []
    for char_index in range(charlength):  
        #print('New Letter')
        #print(str(max(char_index-(order -1), 0))+' - ' +str(char_index))
        preceding_context = output[max(0, char_index-(order -1)):char_index]
        #print('preceding_context: ' + ''.join(preceding_context))
        
        cds = ngram[len(preceding_context)+1].keys()
        #but not all of these are consistent with the preceding context
        filtered_cds = [x for x in cds if list(x)[0:len(preceding_context)] == preceding_context]
        #print(filtered_cds)
        
        filtered_counts = np.array([ngram[len(preceding_context)+1][x] for x in filtered_cds])
        if len(preceding_context) == 0:
            normalizer = float(ngram[0])
        else:
            normalizer = float(np.sum(filtered_counts))
            
        filtered_probs = filtered_counts / normalizer
        #print(np.sum(filtered_probs))
        
        choice = list(np.random.choice(filtered_cds, p = filtered_probs))[-1]
        #print('Choice: '+choice)
        output.append(choice)
        
    return (''.join(output))
