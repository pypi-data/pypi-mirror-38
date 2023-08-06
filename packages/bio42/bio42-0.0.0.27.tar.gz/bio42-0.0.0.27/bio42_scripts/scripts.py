from mhelper import ArgInspector as arg
from bio42 import Application
from neocommand import \
    isEdgeLabel as Edge, \
    isNodeLabel as Node, \
    isNodeUid as Uid, \
    ScriptCommand as script, \
    isDbParam as db_param, \
    isScriptParam as py_param


register = Application.INSTANCE.command( folder = "Bio42 Scripts" )

__DISPLAY_LIMIT = 10
__LIST_LIMIT = 15

register( script( name = "Get edge labels",
                  description = "Lists the relationship types in the database",
                  cypher = "MATCH ()-[r]->() RETURN DISTINCT TYPE(r)" ) )

register( script( name = "Count all nodes",
                  description = "Counts the number of nodes in the database",
                  cypher = "MATCH (n) RETURN COUNT(n)" ) )

register( script( name = "Count all edges",
                  description = "Counts the number of edges in the database",
                  cypher = "MATCH ()-[r]->() RETURN COUNT(r)" ) )

register( script( name = "Count nodes with a specified label",
                  description = "Counts the number of nodes with a specific label",
                  cypher = "MATCH (n:<LABEL>) RETURN COUNT(n)",
                  args = [arg( "label", py_param[Node] )] ) )

register( script( name = "Count edges of type",
                  description = "Counts the number of edges with a specific label",
                  cypher = "MATCH (:<START>)-[r:<EDGE>]->(:<START>) RETURN COUNT(r)",
                  args = [arg( "start", py_param[Edge] ),
                          arg( "edge", py_param[Edge] ),
                          arg( "end", py_param[Edge] )] ) )

register( script( name = "Find non-transitive triplets",
                  description = "Finds non-transitive triplets: A LIKE B LIKE C but NOT A LIKE C",
                  cypher = """MATCH p = (n1:Sequence)-[r1:Blast]-(n2:Sequence)-[r2:Blast]-(n3:Sequence)
                              where (not (n1:Sequence)-[:Blast]-(n3:Sequence))
                              return p limit <LIMIT>""",
                  args = [arg( "limit", py_param[int], __DISPLAY_LIMIT )] ) )

register( script( name = "Find non-transitive chains of 5",
                  description = "Finds non-transitive chains of 5..",
                  cypher = """MATCH p = (n1:Sequence)-[r1:Like]-(n2:Sequence)-[r2:Like]-(n3:Sequence)-[r3:Like]-(n4:Sequence)-[r4:Like]-(n5:Sequence)
                      where (not (n1:Sequence)-[:Like]-(n3:Sequence))
                      and (not (n1:Sequence)-[:Like]-(n4:Sequence))
                      and (not (n1:Sequence)-[:Like]-(n5:Sequence))
                      and (not (n2:Sequence)-[:Like]-(n4:Sequence))
                      and (not (n2:Sequence)-[:Like]-(n5:Sequence))
                      and (not (n3:Sequence)-[:Like]-(n5:Sequence))
                      return p limit 1
                      """ ) )

register( script( name = "Find links between organisms",
                  description = "Given two organisms, for which scientific names should be specified, finds the sequences they share in common",
                  cypher = """MATCH (a:Taxon {scientific_name:{first}}), (b:Taxon {scientific_name:{second}})
                  MATCH path = (a)-->(:Sequence)-[:Like]-(:Sequence)<--(b)
                  RETURN path""",
                  args = [arg( "first", db_param[str] ),
                          arg( "second", db_param[str] )] ) )

register( script( name = "Find organism links between sequences",
                  description = """Given a starting sequence, who's UID should be specified, this query lists the names of the species
                       in which a similar sequence occurs.""",
                  cypher = """MATCH (n:Sequence {uid:{uid}})
                  MATCH (n)-[:Like]-(:Sequence)<-[:Contains]-(o:Taxon)
                  WITH DISTINCT o
                  RETURN DISTINCT o.scientific_name
                  """,
                  args = [arg( "uid", db_param[Uid] )] ) )

register( script( name = "List taxa with sequence data",
                  description = "Returns the names of taxa for which sequence data is present",
                  cypher = """MATCH (taxon:Taxon)
                  WHERE (taxon)-[:Contains]->(:Sequence)
                  RETURN taxon.scientific_name
                  """ ) )

register( script( name = "Find composite genes",
                  description = "A quick and dirty method to find composite genes",
                  cypher = """MATCH (a:Sequence)-[ab:Blast]-(b:Sequence)
                  MATCH (a)-[ac:Blast]-(c:Sequence)
                  WHERE a <> b
                  AND b <> c
                  AND ab.end < ac.start
                  RETURN a, ab, b, ac, c
                  LIMIT <LIMIT>
                  """,
                  args = [arg( "limit", py_param[int], __LIST_LIMIT )] ) )

register( script( name = "Show taxon hierarchy",
                  description = "Given a query taxon, shows how it inherits from the root.",
                  cypher = """MATCH p = (a:Taxon [ uid:[uid] ])<-[:Contains*]-(:Taxon [ uid:"1" ])
                  return p
                  """,
                  args = [arg( "uid", py_param[Uid] )] ) )

register( script( name = "Show taxon MRCA path",
                  description = "Given two taxa, [a] and [b], shows how they are related.",
                  cypher = """MATCH p = shortestpath( (a:Taxon [ uid:[a] ])-[:Contains*]-(b:Taxon [ uid:[b] ]) )
                  return p
                  """,
                  args = [arg( "a", db_param[Uid] ),
                          arg( "b", db_param[Uid] )] ) )
