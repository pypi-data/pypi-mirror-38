# -*- coding: utf-8 -*-
"""This module provides functionality for detecting relations in a pair of
words.

Examples:
    >>> relation_analyzer = ldt.relations.RelationsInPair()
    >>> relation_analyzer.analyze("black", "white")
    {'Hyponyms': True,
     'SharedMorphForm': True,
     'SharedPOS': True,
     'Synonyms': True,
     'Antonyms': True,
     'ShortestPath': 0.058823529411764705,
     'Associations': True,
     'TargetFrequency': 491760,
     'NeighborFrequency': 509267}


Todo:
   - morph form detection (cat, cats)

"""

import functools
import timeout_decorator

from ldt.dicts.dictionary import Dictionary
from ldt.dicts.normalize import Normalization
from ldt.dicts.derivation.meta import DerivationAnalyzer
from ldt.dicts.semantics.metadictionary import MetaDictionary
from ldt.relations.word import Word
from ldt.relations.ontology_path.ontodict import OntoDict
from ldt.load_config import config
from ldt.dicts.resources import AssociationDictionary
from ldt.relations.distribution import DistributionDict

class RelationsInPair(Dictionary):
    """This class implements analyzer for all possible relation types in a word
    pair.

    Args:
        language (str): the language of the dictionaries
        lowercasing (bool): whether output from all resources should be
            lowercased
        derivation_dict (ldt dictionary object): see
            :class:`~ldt.dicts.derivation.meta.DerivationAnalyzer`
        normalizer (ldt dictionary object): see
            :class:`ldt.dicts.normalize.Normalization`
        lex_dict (ldt dictionary object): see
            :class:`ldt.dicts.semantics.metadictionary.MetaDictionary`
        ontodict (ldt dictionary object): see
            :class:`ldt.relations.ontology_path.ontodict.OntoDict`
        association_dict (ldt dictionary object): see
            :class:`ldt.dicts.resources.AssociationDictionary`

        Note:

            If no wordlist is provided, cooccurrence and google
            dependency information will be disabled. The
            wordlist is supplied automatically during large annotation
            experiments on the basis of extracted target:neighbor pairs.
            You can also provide your own.

    """
    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 derivation_dict=None, normalizer=None,
                 lex_dict=None, ontodict=None, association_dict=None):

        super(RelationsInPair, self).__init__(language=language,
                                              lowercasing=lowercasing)
        if not ontodict:
            self.OntoDict = OntoDict(language=language)
        else:
            self.OntoDict = OntoDict

        if not association_dict:
            self.AssociationDictionary = AssociationDictionary(language=language)
        else:
            self.AssociationDictionary = association_dict

        if not normalizer:
            self._normalizer = Normalization(language=self.language, order=(
                "wordnet", "wiktionary"), custom_base="wiktionary")
        else:
            self._normalizer = normalizer


        if not derivation_dict:
            self._derivation_dict = DerivationAnalyzer()
        else:
            self._derivation_dict = derivation_dict


        if not lex_dict:
            self._lex_dict = MetaDictionary()
        else:
            self._lex_dict = lex_dict

        # if distr_dict:
        #     if not isinstance(distr_dict, str):
        #         self._distr_dict = distr_dict
        #
        # else:
        #     if config["corpus"] or gdeps:
        #         self._distr_dict = DistributionDict(language=language,
        #                                             gdeps=gdeps,
        #                                             cooccurrence=cooccurrence,
        #                                             cooccurrence_freq=
        #                                             cooccurrence_freq,
        #                                             wordlist=wordlist,
        #                                             frequencies=frequencies)

    def is_a_word(self, word):
        raise NotImplementedError

    # @timeout_decorator.timeout(config["experiments"]["timeout"], use_signals=False)
    @timeout_decorator.timeout(config["experiments"]["timeout"],
                               use_signals=True)
    @functools.lru_cache(maxsize=config["cache_size"])
    def _analyze(self, target, neighbor, silent=True, distr_data=True):
        """The main function for analyzing the input strings and identifying
        any relations the two words may share.

        Args:file:///mnt/Data/Cloud/pLib/Lab/ldt/corpus_resources/Wiki201308_3grams.json
            target (str): the target word to analyze.
            neighbor (str): the neighbor word to analyze:
            silent (bool): if False, the information retrieved for both words
                is printed for reference.

        Returns:
              (list of str): what the two words have in common.

        Todo:
            Currently associations are established for all the lemmas. That
            could be over-estimating it.
        """

        target = Word(target, self._derivation_dict, self._normalizer,
                      self._lex_dict)
        neighbor = Word(neighbor, self._derivation_dict, self._normalizer,
                        self._lex_dict)
        if not silent:
            print(target.pp_info())
            print(neighbor.pp_info())
        res = {}
        if neighbor.info["Missing"]:
            res["Missing"] = True

        else:

            rels = _binary_rels(target, neighbor)

            for rel in rels:
                res[rel] = True

            paths = []

            for target_lemma in target.info["Lemmas"]:
                for neighbor_lemma in neighbor.info["Lemmas"]:
                        paths.append(self.OntoDict.get_shortest_path(
                            target_lemma, neighbor_lemma))
            if paths:
                res["ShortestPath"] = min(paths)

            for target_lemma in target.info["Lemmas"]:
                for neighbor_lemma in neighbor.info["Lemmas"]:
                    if self.AssociationDictionary.are_related(target_lemma,
                                                              neighbor_lemma):
                        res["Associations"] = True
                        break
        # if distr_data:
        #     if hasattr(self, "_distr_dict"):
        #     # res = self._distributional_data(target, neighbor, res)
        #         distr_res = self._distr_dict.analyze(target=target.info["OriginalForm"], neighbor=neighbor.info["OriginalForm"])
        #         print(distr_res)
        #         res.update(distr_res)
        return res

    # def _distributional_data(self, target, neighbor, res):
    #     """ Helper method for retrieving distributional data, if the corpus
    #     was specified in config file.
    #
    #     Args:
    #         target (ldt Word object): the target word
    #         neighbor (ldt Word object): the neighbor word
    #         res (dict): dictionary with already-discovered relations
    #
    #     Returns:
    #         (dict): dictionary with already-discovered relations, updated
    #         with distributional data.
    #
    #     """
    #     if self._gdeps:
    #         if self._distr_dict.cooccur_in_gdeps(target.info["OriginalForm"],
    #                                              neighbor.info["OriginalForm"]):
    #             res["GDeps"] = True
    #     if not config["corpus"]:
    #         return res
    #     res["TargetFrequency"] = self._distr_dict.frequency_in_corpus(
    #         target.info["OriginalForm"])
    #     res["NeighborFrequency"] = self._distr_dict.frequency_in_corpus(
    #         neighbor.info["OriginalForm"])
    #     if self._cooccurrence:
    #         if not self._distr_dict.cooccur_in_corpus(target.info["OriginalForm"],
    #                                                   neighbor.info["OriginalForm"]):
    #             res["NonCooccurring"] = True
    #     return res


    def analyze(self, target, neighbor, silent=True, debugging=False):
        """Catch-all wrapper for :meth:`_analyze` that ensures that
        large-scale annotation continues even if something breaks on a
        particular pair. The offending data will be logged in experiment
        metadata."""
        if not debugging:
            try:
                return self._analyze(target, neighbor, silent=silent)
            except timeout_decorator.timeout_decorator.TimeoutError:
                if not silent:
                    print("Timed out: " + target + ": " + neighbor)
                return None
            except:
                return None
        else:
            try:
                return self._analyze(target, neighbor, silent=silent)
            except timeout_decorator.timeout_decorator.TimeoutError:
                if not silent:
                    print("Timed out: " + target + ": " + neighbor)
                return None

def _binary_rels(target, neighbor):
    """Helper function for identifying intersections in the property lists
    of the target and neighbor word.

    Args:
        target (ldt Word object): the object holding the data for the
            target word.
        neighbor (ldt Word object): the object holding the data for the
            neighbor word.

    Returns:
          (list of str): what the two words have in common.
    """
    res = []
    for wordclass in ["Numbers", "ProperNouns", "Noise", "URLs",
                      "Filenames", "ForeignWords", "Hashtags", "Misspellings"]:
        if target.info[wordclass] == neighbor.info[wordclass] == True:
            res.append(wordclass)
    if target.info["POS"].intersection(neighbor.info["POS"]):
        res.append("SharedPOS")
    if target.info["IsLemma"] == neighbor.info["IsLemma"] == True:
        res.append("SharedMorphForm")
    for pattern in ["Stems", "Prefixes", "Suffixes", "OtherDerivation"]:
        if pattern in target.info and pattern in neighbor.info:
            if target.info[pattern].intersection(neighbor.info[pattern]):
                res.append("SharedDerivation")
    shared_lex = are_related_as(target, neighbor)
    res += shared_lex
    return list(set(res))


def get_candidate_words(dictionary):
    res = [dictionary["OriginalForm"]]
    for f in ["Lemmas", "Stems"]:
        try:
            res += list(dictionary[f])
        except KeyError:
            pass
    return res

def are_related_as(target, neighbor):
    """Helper function for identifying matches in lexicgraphic relations.

    All relations except hyponymy and hypernymy are treated as symmetrical;
    hyponymy and hypernymy are identified in the target:neighbor direction.

    Args:
        target: the ldt word object for the target word.
        neighbor: the ldt word object for the neighbor word.

    Returns:
        (list of str): the lexicographic relations that the two words are
        related as.

    Todo:

        * antonymy by derivation
    """

    res = []
    neighbor_candidates = get_candidate_words(neighbor.info)
    target_candidates = get_candidate_words(target.info)

    for rel in ["Hyponyms", "Hypernyms"]:
        if rel in target.info:
            for word in neighbor_candidates:
                if word in target.info[rel]:
                    res.append(rel)
            # for word in [neighbor.info["OriginalForm"]] + list(neighbor.info["Lemmas"]) + list(neighbor.info["Stems"]):
            #     if word in target.info[rel]:
            #         res.append(rel)

    rels = ["Synonyms", "Antonyms", "Meronyms", "OtherRelations"]
    for rel in rels:
        if rel in neighbor.info and rel in target.info:
            # for word in [target.info["OriginalForm"]] + list(
            #         target.info["Lemmas"]) + list(target.info["Stems"]):
            for word in target_candidates:
                if word in neighbor.info[rel]:
                    res.append(rel)
        if rel not in res:
            if rel in neighbor.info and rel in target.info:
                for word in neighbor_candidates:
                # for word in [neighbor.info["OriginalForm"]] + list(
                #         neighbor.info["Lemmas"]) + list(neighbor.info["Stems"]):
                    if word in target.info[rel]:
                        res.append(rel)
    return list(set(res))



if __name__ == '__main__':
    relation_analyzer = RelationsInPair()
    print(relation_analyzer.analyze("cat", "dog"))
