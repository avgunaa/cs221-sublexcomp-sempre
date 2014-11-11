package edu.stanford.nlp.sempre.fbalignment.fbgraph;

import edu.stanford.nlp.sempre.fbalignment.utils.ShortContainer;
import edu.uci.ics.jung.graph.DirectedSparseMultigraph;

import java.io.IOException;

public interface FbGraphBuilder<V, E> {

  public DirectedSparseMultigraph<FbEntity, ShortContainer> constructFbGraph() throws IOException;
  public void saveGraph(DirectedSparseMultigraph<FbEntity, ShortContainer> graph, String graphFile) throws IOException;
}
