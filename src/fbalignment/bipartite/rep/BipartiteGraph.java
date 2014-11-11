package edu.stanford.nlp.sempre.fbalignment.bipartite.rep;

import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.stats.ClassicCounter;
import edu.stanford.nlp.util.CollectionUtils;
import edu.uci.ics.jung.graph.UndirectedSparseGraph;
import fig.basic.LogInfo;

import java.io.IOException;
import java.io.Serializable;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

/**
 * Contains a bi-partite graph from Natrual language predicate to Freebase
 * relations. Allows to put various stats about the graph and sample from it.
 *
 * @author jonathanberant
 */
public class BipartiteGraph implements Serializable {


  private static final long serialVersionUID = 6386130890563548472L;
  private UndirectedSparseGraph<BipartiteNode, BipartiteEdge> m_graph;
  Set<NlBipartiteNode> m_nlNodes;
  Set<FbBipartiteNode> m_fbNodes;


  public BipartiteGraph(String fileName) throws IOException, ClassNotFoundException {
    m_graph = IOUtils.readObjectFromFile(fileName);
    m_nlNodes = new HashSet<NlBipartiteNode>();
    m_fbNodes = new HashSet<FbBipartiteNode>();
    for (BipartiteNode node : m_graph.getVertices()) {

      if (node instanceof NlBipartiteNode) {
        NlBipartiteNode nlNode = (NlBipartiteNode) node;
        m_nlNodes.add(nlNode);
      } else if (node instanceof FbBipartiteNode) {
        FbBipartiteNode fbNode = (FbBipartiteNode) node;
        m_fbNodes.add(fbNode);
      } else
        throw new RuntimeException("Node must be either NlBipartiteNode or FbBipartiteNode. It is: " + node.getClass().toString());
    }
  }

  public BipartiteGraph(UndirectedSparseGraph<BipartiteNode, BipartiteEdge> graph) {
    m_graph = graph;
    m_nlNodes = new HashSet<NlBipartiteNode>();
    m_fbNodes = new HashSet<FbBipartiteNode>();
    for (BipartiteNode node : m_graph.getVertices()) {

      if (node instanceof NlBipartiteNode) {
        NlBipartiteNode nlNode = (NlBipartiteNode) node;
        m_nlNodes.add(nlNode);
      } else if (node instanceof FbBipartiteNode) {
        FbBipartiteNode fbNode = (FbBipartiteNode) node;
        m_fbNodes.add(fbNode);
      } else
        throw new RuntimeException("Node must be either NlBipartiteNode or FbBipartiteNode. It is: " + node.getClass().toString());
    }
  }

  public Set<NlBipartiteNode> getNlNodes() { return m_nlNodes; }
  public Set<FbBipartiteNode> getFbNodes() {return m_fbNodes; }

  public int getNlNodeCount() {
    return m_nlNodes.size();
  }

  public int getFbNodeCount() {
    return m_fbNodes.size();
  }

  /** Counts the number of matches between predicates and relations */
  public int totalMatchesCount() {

    int sum = 0;
    for (BipartiteEdge edge : m_graph.getEdges()) {
      sum += edge.value();
    }
    return sum;
  }

  public ClassicCounter<Integer> getNlDegreeDistribution() {

    ClassicCounter<Integer> res = new ClassicCounter<Integer>();
    for (NlBipartiteNode nlNode : m_nlNodes) {
      res.incrementCount(m_graph.getNeighborCount(nlNode));
    }
    return res;
  }

  public ClassicCounter<Integer> getFbDegreeDistribution() {

    ClassicCounter<Integer> res = new ClassicCounter<Integer>();
    for (FbBipartiteNode fbNode : m_fbNodes) {
      res.incrementCount(m_graph.getNeighborCount(fbNode));
    }
    return res;
  }

  public Collection<NlBipartiteNode> sampleNlNodes(int numOfSamples) {

    return CollectionUtils.sampleWithoutReplacement(m_nlNodes, numOfSamples);
  }

  public Collection<FbBipartiteNode> sampleFbNodes(int numOfSamples) {

    return CollectionUtils.sampleWithoutReplacement(m_fbNodes, numOfSamples);
  }

  public UndirectedSparseGraph<BipartiteNode, BipartiteEdge> getGraph() {
    return m_graph;
  }

  public void logEdgesByCount(int strength) {

    for (NlBipartiteNode nlNode : m_nlNodes) {

      Collection<BipartiteNode> neighbors = m_graph.getNeighbors(nlNode);
      for (BipartiteNode neighbor : neighbors) {

        BipartiteEdge edge = m_graph.findEdge(nlNode, neighbor);
        if (edge.value() >= strength) {
          LogInfo.log(nlNode + "\t" + neighbor + "\t" + edge);
        }
      }
    }
  }


}
