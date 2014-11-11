package edu.stanford.nlp.sempre.fbalignment.fbgraph;

import java.io.Serializable;

/**
 * Class representing a Freebase entity
 *
 * @author jonathanberant
 */
public class FbEntity implements Serializable {

  /**
   *
   */
  private static final long serialVersionUID = 7658837122573943533L;
  private String m_id; // Freebase identifier

  public FbEntity(String mid) {
    m_id = mid;
  }

  public String getId() { return m_id; }

  public String toString() {
    return m_id;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((m_id == null) ? 0 : m_id.hashCode());
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
    FbEntity other = (FbEntity) obj;
    if (m_id == null) {
      if (other.m_id != null)
        return false;
    } else if (!m_id.equals(other.m_id))
      return false;
    return true;
  }


}
