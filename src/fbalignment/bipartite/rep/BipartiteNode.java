package edu.stanford.nlp.sempre.fbalignment.bipartite.rep;

import edu.stanford.nlp.util.Pair;

import java.io.Serializable;
import java.util.*;

public abstract class BipartiteNode implements Serializable {

  private static final long serialVersionUID = 8382340391207284957L;
  protected String description;
  protected BipartiteNodeType m_nodeType;

  protected Set<Pair<Integer, Integer>> m_midIdPairSet; // pairs of mid-ids that occur with this node
  protected Map<Integer, TypeIdPairs> m_arg1TypeIdToPairsMap; // mapping from type-id to pairs of mid-ids whose arg1 is of the type-id
  protected Map<Integer, TypeIdPairs> m_arg2TypeIdToPairsMap; // mapping from type-id to pairs of mid-ids whose arg2 is of the type-id

  //// abstract methods

  public abstract BipartiteNodeType getType();

  //// non-abstract methods

  public BipartiteNode() {
    m_midIdPairSet = new TreeSet<Pair<Integer, Integer>>();
    m_arg1TypeIdToPairsMap = new HashMap<Integer, TypeIdPairs>();
    m_arg2TypeIdToPairsMap = new HashMap<Integer, TypeIdPairs>();
  }

  public Set<Pair<Integer, Integer>> getMidIdPairSet() {
    return m_midIdPairSet;
  }

  public int getMidIdPairsCount() { return m_midIdPairSet.size(); }

  public void sortTypeMapsBySetSize() {

    // sort
    List<TypeIdPairs> arg1IdPairs = new LinkedList<TypeIdPairs>();
    arg1IdPairs.addAll(m_arg1TypeIdToPairsMap.values());
    Collections.sort(arg1IdPairs);
    // re-insert
    m_arg1TypeIdToPairsMap = new LinkedHashMap<Integer, BipartiteNode.TypeIdPairs>();
    for (TypeIdPairs typeIdPairs : arg1IdPairs) {
      m_arg1TypeIdToPairsMap.put(typeIdPairs.getTypeId(), typeIdPairs);
    }

    // sort
    List<TypeIdPairs> arg2IdPairs = new LinkedList<TypeIdPairs>();
    arg2IdPairs.addAll(m_arg2TypeIdToPairsMap.values());
    Collections.sort(arg2IdPairs);
    // re-insert
    m_arg2TypeIdToPairsMap = new LinkedHashMap<Integer, BipartiteNode.TypeIdPairs>();
    for (TypeIdPairs typeIdPairs : arg2IdPairs) {
      m_arg2TypeIdToPairsMap.put(typeIdPairs.getTypeId(), typeIdPairs);
    }
  }


  public Map<Integer, TypeIdPairs> getArg1TypeMap() {
    return m_arg1TypeIdToPairsMap;
  }
  public Map<Integer, TypeIdPairs> getArg2TypeMap() {
    return m_arg2TypeIdToPairsMap;
  }

  public void addIdPairToArg1TypeMap(int type, Pair<Integer, Integer> idPair) {

    TypeIdPairs typeIdPairs = m_arg1TypeIdToPairsMap.get(type);
    if (typeIdPairs == null) {
      Set<Pair<Integer, Integer>> idPairs = new TreeSet<Pair<Integer, Integer>>();
      typeIdPairs = new TypeIdPairs(type, idPairs);
      m_arg1TypeIdToPairsMap.put(type, typeIdPairs);
    }
    typeIdPairs.addPair(idPair);
  }

  public void addIdPairToArg2TypeMap(int type, Pair<Integer, Integer> idPair) {

    TypeIdPairs typeIdPairs = m_arg2TypeIdToPairsMap.get(type);
    if (typeIdPairs == null) {
      Set<Pair<Integer, Integer>> idPairs = new TreeSet<Pair<Integer, Integer>>();
      typeIdPairs = new TypeIdPairs(type, idPairs);
      m_arg2TypeIdToPairsMap.put(type, typeIdPairs);
    }
    typeIdPairs.addPair(idPair);
  }

  public Set<Pair<Integer, Integer>> getArg1IdPairs(int type) {
    if (type == -1)
      return m_midIdPairSet;
    if (!m_arg1TypeIdToPairsMap.containsKey(type))
      return new HashSet<Pair<Integer, Integer>>();
    return m_arg1TypeIdToPairsMap.get(type).getIdPairs();
  }

  public Set<Pair<Integer, Integer>> getArg2IdPairs(int type) {
    if (type == -1)
      return m_midIdPairSet;
    if (!m_arg2TypeIdToPairsMap.containsKey(type))
      return new HashSet<Pair<Integer, Integer>>();
    return m_arg2TypeIdToPairsMap.get(type).getIdPairs();
  }

  public boolean addPair(int mid1, int mid2) {
    return m_midIdPairSet.add(new Pair<Integer, Integer>(mid1, mid2));
  }

  public boolean addPair(Pair<Integer, Integer> pair) {
    return m_midIdPairSet.add(pair);
  }

  public void addAllPairs(Set<Pair<Integer, Integer>> pairs) {
    for (Pair<Integer, Integer> pair : pairs) {
      m_midIdPairSet.add(pair);
    }
  }

  public String getDescription() {return description; }

  public String toString() {return description + "\t" + m_midIdPairSet;}
  public String toShortString() {return description; }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result
        + ((description == null) ? 0 : description.hashCode());
    result = prime * result
        + ((m_nodeType == null) ? 0 : m_nodeType.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    BipartiteNode other = (BipartiteNode) obj;
    if (description == null) {
      if (other.description != null)
        return false;
    } else if (!description.equals(other.description))
      return false;
    if (m_nodeType != other.m_nodeType)
      return false;
    return true;
  }

  public static BipartiteNode copyNode(BipartiteNode otherNode) {

    BipartiteNode res;
    if (otherNode instanceof NlBipartiteNode) {
      res = new NlBipartiteNode(otherNode.description);
    } else if (otherNode instanceof FbBipartiteNode) { // it is an FbBipartiteNode
      FbBipartiteNode fbOriginal = (FbBipartiteNode) otherNode;
      res = new FbBipartiteNode(fbOriginal.getCompositePredicate(), fbOriginal.reversed);
    } else
      throw new RuntimeException("The node being cloned has an illegal type: " + otherNode.getClass());
    // copy pairs of IDs
    for (Pair<Integer, Integer> pair : otherNode.m_midIdPairSet) {
      res.addPair(new Pair<Integer, Integer>(pair.first, pair.second));
    }
    // copy mapping of types to pairs with arg1 of that type
    for (int typeId : otherNode.m_arg1TypeIdToPairsMap.keySet()) {
      for (Pair<Integer, Integer> pair : otherNode.getArg1IdPairs(typeId)) {
        res.addIdPairToArg1TypeMap(typeId, new Pair<Integer, Integer>(pair.first, pair.second));
      }
    }
    // copy mapping of types to pairs with args2 of that type
    for (int typeId : otherNode.m_arg2TypeIdToPairsMap.keySet()) {
      for (Pair<Integer, Integer> pair : otherNode.getArg2IdPairs(typeId)) {
        res.addIdPairToArg2TypeMap(typeId, new Pair<Integer, Integer>(pair.first, pair.second));
      }
    }
    return res;
  }

  public class TypeIdPairs implements Comparable<TypeIdPairs>, Serializable {


    private static final long serialVersionUID = -4002959569790723021L;
    private int m_typeId;
    private Set<Pair<Integer, Integer>> m_idPairs;

    public TypeIdPairs(int typeId, Set<Pair<Integer, Integer>> idPairs) {
      m_typeId = typeId;
      m_idPairs = idPairs;
    }

    public TypeIdPairs(TypeIdPairs other) {

      m_typeId = other.m_typeId;
      for (Pair<Integer, Integer> pair : other.m_idPairs) {
        // no need to copy the integers since they are immutable
        m_idPairs.add(new Pair<Integer, Integer>(pair.first, pair.second));
      }
    }

    public void addPair(Pair<Integer, Integer> pair) {
      m_idPairs.add(pair);
    }

    public Set<Pair<Integer, Integer>> getIdPairs() {
      return m_idPairs;
    }

    public int getTypeId() {
      return m_typeId;
    }

    public String toString() {
      return m_typeId + "\t" + m_idPairs;
    }

    @Override
    public int compareTo(TypeIdPairs other) {
      return (new Integer(other.m_idPairs.size())).compareTo(m_idPairs.size());
    }
  }
}
