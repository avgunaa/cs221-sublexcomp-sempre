package edu.stanford.nlp.sempre.fbalignment.bipartite.filters;

import edu.stanford.nlp.sempre.fbalignment.bipartite.rep.BipartiteNode;

public class NodeFrequencyOrFbRelationFilter implements BipartiteNodeFilter {

  NodeFrequencyFilter m_nodeFreqFilter;
  FbRelationFilter m_fbRelFilter;

  public NodeFrequencyOrFbRelationFilter() {
    m_nodeFreqFilter = new NodeFrequencyFilter();
    m_fbRelFilter = new FbRelationFilter();
  }

  @Override
  public boolean filterNode(BipartiteNode node) {
    return m_nodeFreqFilter.filterNode(node) || m_fbRelFilter.filterNode(node);
  }

}
