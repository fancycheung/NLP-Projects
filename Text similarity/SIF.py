# smooth inverse frequency
# Two steps:
# [1] Compute the weighted average of the word vectors in the sentence.
# [2] Common component removal: remove the projections of the average vectors on their first principal component.
# From A simple but tough-to-beat baseline for sentence embeddings, https://openreview.net/pdf?id=SyK00v5xx
# Official implementation: https://github.com/PrincetonML/SIF

def SIF_embedding(self, x, w):
    """
    x: word ids of each sample, shape of [n_sample, vocab_size]
    w: weights of each word ids, shape of [n_sample, vocab_size]
    """
    
    # step 1: weighted averages
    n_samples = x.shape[0]
    emb = np.zeros((n_samples, self.word_vectors.shape[1]))
    for i in range(n_samples):
        emb[i, :] = w[i, :].dot(self.word_vectors[x[i, :], :]) / np.count_nonzero(w[i, :])
    # step 2: removing the projection on the first principal component
    svd = TruncatedSVD(n_components=self.SIF_npc, n_iter=7, random_state=0)
    svd.fit(emb)
    pc = svd.components_
    if self.SIF_npc == 1:
        # pc.transpose().shape : embedding_size * 1
        # emb.dot(pc.transpose()).shape: num_sample * 1
        # (emb.dot(pc.transpose()) * pc ).shape: num_sample * embedding_size
        common_component_removal = emb - emb.dot(pc.transpose()) * pc
    else:
        common_component_removal = emb - emb.dot(pc.transpose()).dot(pc)
    return common_component_removal