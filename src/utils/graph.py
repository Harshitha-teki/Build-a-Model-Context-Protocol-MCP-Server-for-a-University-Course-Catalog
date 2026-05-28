from typing import List, Dict, Any
import networkx as nx

def create_prerequisite_graph(courses: List[Dict[str, Any]], prerequisites: List[Dict[str, Any]]) -> nx.DiGraph:
    graph = nx.DiGraph()

    # Add courses as nodes
    for course in courses:
        graph.add_node(course['course_code'], title=course['title'])

    # Add prerequisites as edges
    for prereq in prerequisites:
        graph.add_edge(prereq['course_code'], prereq['prerequisite_code'])

    return graph

def get_prerequisite_chain(graph: nx.DiGraph, course_code: str) -> List[str]:
    if course_code not in graph:
        return []

    # Find all prerequisites for the given course
    return list(nx.ancestors(graph, course_code))

def export_graph_to_json(graph: nx.DiGraph) -> Dict[str, Any]:
    nodes = [{'id': node} for node in graph.nodes()]
    edges = [{'source': source, 'target': target} for source, target in graph.edges()]

    return {
        'nodes': nodes,
        'edges': edges
    }