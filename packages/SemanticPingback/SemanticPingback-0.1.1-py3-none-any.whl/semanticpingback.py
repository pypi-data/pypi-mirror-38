import rdflib
import urllib.parse
import logging

logger = logging.getLogger(__name__)

class SemanticPingbackReceiver():
    def __init__(self, baseuri=None, target_allow_external=True, pingback_callback=None,
                 del_pingback_callback=None):
        self.baseuri = baseuri
        self.target_allow_external = target_allow_external
        self.pingback_callback = pingback_callback
        self.del_pingback_callback = del_pingback_callback
        logger.debug("Init SemanticPingback")

    def receivePing(self, source=None, target=None, comment=None, request=None):
        if request:
            source = request.values.get("source", None)
            target = request.values.get("target", None)
            comment = request.values.get("comment", None)
        if not source:
            raise PingException("No source resource given")
        if not target:
            raise PingException("No source resource given")
        try:
            sourceIri = rdflib.term.URIRef(source)
            targetIri = rdflib.term.URIRef(target)
        except Exception as e:
            raise PingException("Given target resource is not a valid URI.")

        if not self.target_allow_external:
            if urllib.parse.urlparse(self.baseuri).netloc != urllib.parse.urlparse(targetIri).netloc:
                raise PingException("Given target is not from this server (disallowed by config).")

        links = self.getLinkFromSource(sourceIri, targetIri)
        if not len(links):
            if self.del_pingback_callback:
                self.del_pingback_callback(sourceIri, targetIri, comment)
        else:
            if self.pingback_callback:
                self.pingback_callback(sourceIri, targetIri, links, comment)
        return links

    def getLinkFromSource(self, source, target):
        graph = rdflib.Graph()
        linkGraph = rdflib.Graph()
        try:
            self._load(graph, source)
            links = graph.triples((source, None, target))
            linkGraph += links
            if len(linkGraph):
                return linkGraph
        except Exception as e:
            logger.debug(e)
            pass
        # TODO if graph is empty try loading RDFa
        # TODO if graph is still empty load html and try to extract hyperlinks
        #   for each found html link to the target create a triple:
        #   source http://rdfs.org/sioc/ns#links_to target

        raise PingException("No links in source document.")

    def _load(self, graph, source):
        """from https://rdflib.readthedocs.io/en/stable/_modules/rdflib/plugins/sparql/sparql.html"""
        try:
            return graph.load(source)
        except:
            pass
        try:
            return graph.load(source, format='n3')
        except:
            pass
        try:
            return graph.load(source, format='nt')
        except:
            raise Exception("Could not load {} as either RDF/XML, N3 or NTriples".format(source))


class PingException(Exception):
    pass

class ConfigException(Exception):
    pass
