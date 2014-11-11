package edu.stanford.nlp.sempre.fbalignment.bipartite.filters;

import edu.stanford.nlp.sempre.fbalignment.bipartite.rep.BipartiteNode;

public interface BipartiteNodeFilter {

  public boolean filterNode(BipartiteNode node);

}
